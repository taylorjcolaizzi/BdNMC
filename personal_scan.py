#!/usr/bin/env python3

from Parameter_Card_Generator import run_output_file

# Parameter space
m_DM_values = [i / 1000 for i in range(10, 101, 10)]  # 0.01 to 0.10 GeV

# Parent meson masses in GeV
M_PI0 = 0.1349766
M_ETA = 0.547862

# Template parameter card
template_card = "parameter_mass.dat"

def allowed_production_channels(m_dm, m_dp):
    if m_dp <= 2 * m_dm:
        raise ValueError(
            f"dark_photon_mass ({m_dp} GeV) must be greater than "
            f"2 * dark_matter_mass ({2 * m_dm} GeV) for V -> DM DM."
        )

    channels = []
    if m_dp <= M_PI0:
        channels.append(("pi0_decay", "pi0_sanfordwang"))
    if m_dp <= M_ETA:
        channels.append(("eta_decay", "bmpt"))
    channels.append(("V_decay", "proton_brem"))
    return channels

def main():
    for m_DM in m_DM_values:

        # Example model relation
        m_DP = m_DM * 3.0
        production_channels = allowed_production_channels(m_DM, m_DP)
        tag = f"mdm_{m_DM:.3f}"

        output_event_file = f"Events/batch/events_{tag}.dat"
        output_param_card = f"Cards/parameter_{tag}.dat"

        params = {
            "dark_photon_mass": m_DP,
            "dark_matter_mass": m_DM,
            "output_file": output_event_file
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