#!/usr/bin/env python3

from Parameter_Card_Generator import run_output_file

# Parameter space
m_DM_values = [i / 1000 for i in range(10, 101, 10)]  # 0.01 to 0.10 GeV

# Template parameter card
template_card = "parameter_mass.dat"


def allowed_production_channels(m_dm):
    # Match the final channel schedule described in Jack's eta-decay slides.
    if m_dm <= 0.04:
        channels = [("pi0_decay", "bmpt"), ("eta_decay", "bmpt")]
    else:
        channels = [("eta_decay", "bmpt")]

    channels.append(
        ("V_decay", "proton_brem", {"ptmax": 1, "zmin": 0.1, "zmax": 0.9})
    )
    return channels


def main():
    for m_DM in m_DM_values:

        # Match the visible-decay benchmark mass relation in Jack's template.
        m_DP = m_DM / 2.0
        production_channels = allowed_production_channels(m_DM)
        tag = f"mdm_{m_DM:.3f}"

        output_event_file = f"Events/batch/events_{tag}.dat"
        output_summary_file = f"Events/batch/summary_{tag}.dat"
        output_param_card = f"Cards/parameter_{tag}.dat"

        params = {
            "dark_photon_mass": m_DP,
            "dark_matter_mass": m_DM,
            "output_file": output_event_file,
            "summary_file": output_summary_file,
        }

        print(f"Running {tag}")

        run_output_file(
            template_card,
            output_param_card,
            params,
            run=True,
            production_channels=production_channels
        )

    print("Scan complete.")


if __name__ == "__main__":
    main()