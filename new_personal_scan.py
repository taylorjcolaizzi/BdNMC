#!/usr/bin/env python3

from Parameter_Card_Generator import run_output_file

# Parameter space
m_DM_values = [i / 1000 for i in range(10, 101, 10)]  # 0.01 to 0.10 GeV

# Parent meson masses in GeV
M_PI0 = 0.1349766
M_ETA = 0.547862

# Template parameter card
template_card = "parameter_mass.dat"


def allowed_production_channels(m_dm):
    channels = []
    if 2.0 * m_dm <= M_PI0:
        channels.append(("pi0_decay", "pi0_sanfordwang"))
    if 2.0 * m_dm <= M_ETA:
        channels.append(("eta_decay", "bmpt", {"meson_per_pi0": 0.0333}))
    return channels


def main():
    for m_DM in m_DM_values:
        # The mediator is off-shell for DM-pair production at this mass ratio.
        m_DP = m_DM / 3.0
        production_channels = allowed_production_channels(m_DM)
        tag = f"electron_scatter_mdm_{m_DM:.3f}"

        output_event_file = f"Events/batch/events_{tag}.dat"
        output_param_card = f"Cards/parameter_{tag}.dat"

        params = {
            "dark_photon_mass": m_DP,
            "dark_matter_mass": m_DM,
            "signal_channel": "NCE_electron",
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

    print("Electron-scattering scan complete.")


if __name__ == "__main__":
    main()
