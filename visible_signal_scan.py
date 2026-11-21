#!/usr/bin/env python3

import argparse
import csv
import math
import os
import re
import subprocess
import tempfile
from pathlib import Path

from Parameter_Card_Generator import update_param, update_production_channels


ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "parameter_template_visible_signal.dat"
MASS_PI0 = 0.1349766
MASS_ETA = 0.547862
DEFAULT_MASSES_MEV = tuple(range(100, 1001, 25))
DEFAULT_EPSILON_SQUARED = tuple(10 ** (-12 - 0.5 * i) for i in range(9))
RESULT_FIELDS = (
    "mass_dp_mev",
    "mass_dm_mev",
    "epsilon_squared",
    "epsilon",
    "predicted_events",
)


def production_channels(mass_dp_gev):
    channels = []
    if mass_dp_gev <= MASS_PI0:
        channels.append(("pi0_decay", "bmpt"))
    if mass_dp_gev <= MASS_ETA:
        channels.append(("eta_decay", "bmpt"))
    channels.append(
        ("V_decay", "proton_brem", {"ptmax": 1, "zmin": 0.1, "zmax": 0.9})
    )
    return channels


def dark_matter_mass(mass_dp_gev):
    return 0.6 * mass_dp_gev


def parse_predicted_events(output):
    match = re.search(
        r"^Predicted number of signal events =\s*([^\s]+)",
        output,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError("Simulation output did not include a predicted event count.")
    return float(match.group(1))


def result_key(mass_dp_mev, epsilon_squared):
    return (format(float(mass_dp_mev), ".12g"), format(float(epsilon_squared), ".12g"))


def load_results(path):
    if not path.exists():
        return {}
    with path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != list(RESULT_FIELDS):
            raise ValueError(f"{path} has an unexpected CSV header.")
        return {
            result_key(row["mass_dp_mev"], row["epsilon_squared"]): row
            for row in reader
        }


def save_results(path, rows):
    with path.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(
            sorted(
                rows,
                key=lambda row: (
                    float(row["mass_dp_mev"]),
                    float(row["epsilon_squared"]),
                ),
            )
        )


def run_point(mass_dp_mev, epsilon_squared, output_dir, samplesize, max_trials):
    mass_dp_gev = mass_dp_mev / 1000.0
    mass_dm_gev = dark_matter_mass(mass_dp_gev)
    epsilon = math.sqrt(epsilon_squared)
    output_dir.mkdir(parents=True, exist_ok=True)

    params = {
        "dark_photon_mass": mass_dp_gev,
        "dark_matter_mass": mass_dm_gev,
        "epsilon": epsilon,
        "output_file": str(output_dir / "events.dat"),
        "summary_file": str(output_dir / "summary.dat"),
    }
    if samplesize is not None:
        params["samplesize"] = samplesize
    if max_trials is not None:
        params["max_trials"] = max_trials

    with TEMPLATE.open() as template_file:
        lines = update_param(template_file.readlines(), params)
    lines = update_production_channels(lines, production_channels(mass_dp_gev))

    card_directory = ROOT / "Cards"
    card_directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".dat",
        prefix=".visible_signal_scan_",
        dir=card_directory,
        delete=False,
    ) as card_file:
        card_path = Path(card_file.name)
        card_file.writelines(lines)

    try:
        relative_card = card_path.relative_to(ROOT)
        executable = os.environ.get(
            "BDNMC_EXECUTABLE",
            str(ROOT / "bin" / "BDNMC"),
        )
        process = subprocess.run(
            [executable, str(relative_card)],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Simulation failed for mDP={mass_dp_mev:g} MeV, "
            f"epsilon^2={epsilon_squared:g}:\n{error.stdout}{error.stderr}"
        ) from error
    finally:
        try:
            card_path.unlink()
        except FileNotFoundError:
            pass

    events = parse_predicted_events(process.stdout)
    return {
        "mass_dp_mev": format(mass_dp_mev, ".12g"),
        "mass_dm_mev": format(mass_dm_gev * 1000.0, ".12g"),
        "epsilon_squared": format(epsilon_squared, ".12g"),
        "epsilon": format(epsilon, ".12g"),
        "predicted_events": format(events, ".12g"),
    }


def cell_edges(values, logarithmic=False, single_step=None):
    if len(values) == 1:
        value = values[0]
        if logarithmic:
            return [value / 10 ** (single_step / 2), value * 10 ** (single_step / 2)]
        return [value - single_step / 2, value + single_step / 2]

    if logarithmic:
        transformed = [math.log10(value) for value in values]
        boundaries = [
            transformed[0] - (transformed[1] - transformed[0]) / 2,
            *(
                (left + right) / 2
                for left, right in zip(transformed, transformed[1:])
            ),
            transformed[-1] + (transformed[-1] - transformed[-2]) / 2,
        ]
        return [10**value for value in boundaries]

    midpoints = [(left + right) / 2 for left, right in zip(values, values[1:])]
    return [
        values[0] - (midpoints[0] - values[0]),
        *midpoints,
        values[-1] + (values[-1] - midpoints[-1]),
    ]


def plot_results(rows, path):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import LogNorm
    except ImportError as error:
        raise RuntimeError(
            "Plotting requires matplotlib and numpy; install matplotlib to create the figure."
        ) from error

    masses = sorted(
        set(DEFAULT_MASSES_MEV)
        | {float(row["mass_dp_mev"]) for row in rows}
    )
    epsilon_squared = sorted({float(row["epsilon_squared"]) for row in rows})
    lookup = {
        result_key(row["mass_dp_mev"], row["epsilon_squared"]): float(
            row["predicted_events"]
        )
        for row in rows
    }
    grid = np.ma.masked_all((len(epsilon_squared), len(masses)))
    for yi, eps2 in enumerate(epsilon_squared):
        for xi, mass in enumerate(masses):
            key = result_key(mass, eps2)
            if key in lookup and lookup[key] > 0:
                grid[yi, xi] = lookup[key]

    positive = grid.compressed()
    if not positive.size:
        raise ValueError("No positive event counts are available to plot.")
    vmin = float(positive.min())
    vmax = float(positive.max())
    if vmin == vmax:
        vmax = vmin * 10
    norm = LogNorm(vmin=vmin, vmax=vmax)

    x_edges = cell_edges(masses, single_step=25)
    y_edges = cell_edges(epsilon_squared, logarithmic=True, single_step=0.5)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    mesh = None
    for axis, (lower, upper), title in zip(
        axes,
        ((100, 500), (500, 1000)),
        ("100–500 MeV", "500–1000 MeV"),
    ):
        selected = [
            index
            for index, mass in enumerate(masses)
            if lower <= mass < upper or (upper == 1000 and mass == upper)
        ]
        if selected:
            start, end = selected[0], selected[-1] + 1
            mesh = axis.pcolormesh(
                x_edges[start : end + 1],
                y_edges,
                grid[:, start:end],
                norm=norm,
                shading="flat",
                cmap="viridis",
            )
        axis.set_xlim(lower, upper)
        axis.set_yscale("log")
        axis.set_xlabel("Mass of DP (MeV)")
        axis.set_title(title)

    axes[0].set_ylabel("ε²")
    if mesh is not None:
        fig.subplots_adjust(left=0.08, right=0.9, bottom=0.14, top=0.86, wspace=0.15)
        colorbar_axis = fig.add_axes((0.92, 0.17, 0.02, 0.68))
        fig.colorbar(mesh, cax=colorbar_axis, label="Signal Events")
    fig.suptitle("Distribution of Signal Events (4 · 10²¹ POT)")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan visible dark-photon decays over mDP and epsilon squared."
    )
    parser.add_argument(
        "--masses-mev",
        type=float,
        nargs="+",
        default=DEFAULT_MASSES_MEV,
        help="Dark-photon masses in MeV (default: 100–1000 in 25 MeV steps).",
    )
    parser.add_argument(
        "--epsilon-squared",
        type=float,
        nargs="+",
        default=DEFAULT_EPSILON_SQUARED,
        help="epsilon-squared scan values (default: 1e-12 to 1e-16, half-decade steps).",
    )
    parser.add_argument(
        "--point",
        type=float,
        nargs=2,
        action="append",
        metavar=("MASS_MEV", "EPSILON_SQUARED"),
        help="Run one mass/coupling pair; may be supplied multiple times.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "Events" / "visible_signal_scan",
        help="Directory for CSV, summary, and plot outputs.",
    )
    parser.add_argument("--samplesize", type=int, help="Override the template sample size.")
    parser.add_argument("--max-trials", type=int, help="Override the template trial limit.")
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Write scan data without creating the plot.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not TEMPLATE.is_file():
        raise FileNotFoundError(f"Signal-decay template not found: {TEMPLATE}")
    args.output_dir = args.output_dir.resolve()
    points = (
        sorted(set(map(tuple, args.point)))
        if args.point
        else [
            (mass, eps2)
            for mass in sorted(set(args.masses_mev))
            for eps2 in sorted(set(args.epsilon_squared))
        ]
    )
    if any(mass <= 0 for mass, _ in points):
        raise ValueError("All dark-photon masses must be positive.")
    if any(eps2 <= 0 for _, eps2 in points):
        raise ValueError("All epsilon-squared values must be positive.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "signal_events.csv"
    rows_by_key = load_results(csv_path)
    total = len(points)
    completed = 0
    for mass, eps2 in points:
        key = result_key(mass, eps2)
        if key in rows_by_key:
            print(f"Skipping existing point: mDP={mass:g} MeV, epsilon^2={eps2:g}")
            completed += 1
            continue
        row = run_point(
            mass,
            eps2,
            args.output_dir,
            args.samplesize,
            args.max_trials,
        )
        rows_by_key[key] = row
        save_results(csv_path, rows_by_key.values())
        completed += 1
        print(
            f"[{completed}/{total}] mDP={mass:g} MeV, "
            f"epsilon^2={eps2:g}: {row['predicted_events']} events"
        )

    if not args.no_plot:
        plot_path = args.output_dir / "signal_events.png"
        plot_results(list(rows_by_key.values()), plot_path)
        print(f"Plot written to {plot_path}")
    print(f"Scan data written to {csv_path}")


if __name__ == "__main__":
    main()
