#!/usr/bin/env python3

# Generates a bunch of parameter cards that you can then send to Slurm. That
# way, the program runs parallel on a bunch of CPUs. You don't need to wait
# for them to go in order on one CPU.

from Parameter_Card_Generator import run_output_file
import os

# Parameter space
# do linspace, no numpy
mdp_values = [i / 100 for i in range(1, 101)]      # GeV
# mpd_values = [0.05, 0.10, 0.15, 0.20]
# do logspace, no numpy
start, stop, num, base = -5, -3, 5, 10
eps_values = [base ** (start + i * (stop - start) / (num - 1)) for i in range(num)]
# eps_values = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3]

alpha_D = 0.5

# Template parameter card
template_card = "parameter.dat"

i = 0 # start counter
for mdp in mdp_values:

    # Example model relation
    mdm = mdp / 3.0

    tag = i

    output_event_file = f"Events/batch/events_{tag:03d}.dat"
    output_param_card = f"Cards/parameter_{tag:03d}.dat"

    params = {
        "dark_photon_mass": mdp,
        "dark_matter_mass": mdm,
        "output_file": output_event_file
    }

    print(f"Running {tag}")

    run_output_file(
        template_card,
        output_param_card,
        params,
        run=False
    )
    i += 1

print("Scan complete.")