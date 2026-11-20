import unittest

from visible_signal_scan import (
    dark_matter_mass,
    parse_predicted_events,
    production_channels,
)


class VisibleSignalScanTests(unittest.TestCase):
    def test_production_channels_follow_meson_mass_thresholds(self):
        self.assertEqual(
            [channel[0] for channel in production_channels(0.1)],
            ["pi0_decay", "eta_decay", "V_decay"],
        )
        self.assertEqual(
            [channel[0] for channel in production_channels(0.35)],
            ["eta_decay", "V_decay"],
        )
        self.assertEqual(
            [channel[0] for channel in production_channels(0.78)],
            ["V_decay"],
        )

    def test_provisional_dm_mass_closes_invisible_decay_channel(self):
        for mass_dp_gev in (0.1, 0.35, 0.78, 1.0):
            self.assertGreaterEqual(
                2 * dark_matter_mass(mass_dp_gev),
                mass_dp_gev,
            )

    def test_predicted_event_count_is_read_from_simulator_output(self):
        self.assertEqual(
            parse_predicted_events(
                "Predicted number of signal events = 42.5965\n"
            ),
            42.5965,
        )
        with self.assertRaises(ValueError):
            parse_predicted_events("Simulation finished without a count.")


if __name__ == "__main__":
    unittest.main()
