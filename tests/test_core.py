"""Tests for the solar declination calculation library."""

import math
import unittest
from datetime import date, datetime, timedelta

from solar_declination_calc import declination


class DeclinationTests(unittest.TestCase):
    def test_equinox_approximate_zero(self):
        """Around the equinoxes the declination crosses zero.

        The Cooper approximation puts the crossing on day 81 (March 22
        in a non-leap year), so we test a small tolerance.
        """
        self.assertAlmostEqual(declination(date(2023, 3, 22)), 0.0, places=1)

    def test_june_solstice_positive_max(self):
        """The June solstice should be close to +23.45 degrees."""
        self.assertAlmostEqual(declination(date(2023, 6, 21)), 23.45, places=1)

    def test_december_solstice_negative_max(self):
        """The December solstice should be close to -23.45 degrees."""
        self.assertAlmostEqual(declination(date(2023, 12, 21)), -23.45, places=1)

    def test_symmetric_around_solstices(self):
        """Days equidistant from a solstice have approximately equal declinations."""
        d1 = declination(date(2023, 6, 21) - timedelta(days=10))
        d2 = declination(date(2023, 6, 21) + timedelta(days=10))
        self.assertAlmostEqual(d1, d2, delta=1.0)

    def test_accepts_datetime(self):
        """datetime is a subclass of date and should be accepted."""
        self.assertAlmostEqual(
            declination(datetime(2023, 1, 1, 12, 30)),
            declination(date(2023, 1, 1)),
            places=12,
        )

    def test_rejects_non_date(self):
        """Non-date objects must raise TypeError."""
        with self.assertRaises(TypeError):
            declination("2023-01-01")
        with self.assertRaises(TypeError):
            declination(2023)

    def test_year_boundary_continuity(self):
        """December 31 and January 1 are adjacent days in the cycle."""
        d_dec = declination(date(2022, 12, 31))
        d_jan = declination(date(2023, 1, 1))
        # Difference should be small because the day-of-year goes from
        # 365 to 1; the 284+N formula wraps smoothly.
        self.assertLess(abs(d_dec - d_jan), 1.0)

    def test_leap_year_day_count(self):
        """Leap years use 366 days, shifting day numbers after February."""
        d_non_leap = declination(date(2023, 3, 1))
        d_leap = declination(date(2024, 3, 1))
        # The leap year value should be one day ahead of the non-leap
        # value, so the difference is approximately one day's change.
        self.assertAlmostEqual(
            d_leap - d_non_leap,
            0.4,
            delta=0.1,
        )

    def test_result_range(self):
        """The declination must remain within the expected bounds."""
        for day_offset in range(0, 365):
            d = declination(date(2023, 1, 1) + timedelta(days=day_offset))
            self.assertGreaterEqual(d, -23.45)
            self.assertLessEqual(d, 23.45)

    def test_known_value_mid_year(self):
        """Value for a specific day computed from the formula directly."""
        # Day 100 of 2023 is April 10.
        n = 100
        expected = 23.45 * math.sin(math.radians(360 * (284 + n) / 365))
        self.assertAlmostEqual(declination(date(2023, 4, 10)), expected, places=12)


if __name__ == "__main__":
    unittest.main()
