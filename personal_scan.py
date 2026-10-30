#!/usr/bin/env python3

from Parameter_Card_Generator import run_output_file
import os

# Parameter space
mdp_values = [0.05, 0.10, 0.15, 0.20]      # GeV
eps_values = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3]

alpha_D = 0.5

# Template parameter card
template_card = "parameter.dat"

for mdp in mdp_values:

    # Example model relation
    mdm = mdp / 3.0

    for eps in eps_values:

        tag = f"mAp_{mdp:.3f}_eps_{eps:.1e}"

        output_event_file = f"Events/batch/events_{tag}.dat"
        output_param_card = f"Cards/parameter_{tag}.dat"

        params = {
            "epsilon": eps,
            "alpha_D": alpha_D,
            "dark_photon_mass": mdp,
            "dark_matter_mass": mdm,
            "output_file": output_event_file
        }

        print(f"Running {tag}")

        run_output_file(
            template_card,
            output_param_card,
            params,
            run=True
        )

print("Scan complete.")