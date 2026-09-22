"""Core solar declination computation.

The declination angle is the angle between the rays of the Sun and the
plane of the Earth's equator. It varies between approximately +23.44
and -23.44 degrees over the course of a year.

This module uses a widely accepted approximation based on the day of
the year. The formula chosen is from Cooper (1969), which is simple,
reasonably accurate for most applications, and requires no external
data. The trade-off is a maximum error of about 0.5 degrees compared
with more precise astronomical calculations.
"""

from __future__ import annotations

import math
from datetime import date, datetime


def _day_of_year(day: date) -> int:
    """Return the 1-based day-of-year for a date.

    This deliberately uses a 1-based index so that January 1 is day 1,
    which matches the convention in the Cooper formula and avoids an
    off-by-one error at the start of the year.
    """
    return day.timetuple().tm_yday


def declination(day: date) -> float:
    """Return the solar declination angle for the given date in degrees.

    Positive values indicate the Sun is north of the celestial equator;
    negative values indicate south.

    The argument must be a ``datetime.date`` (or a ``datetime.datetime``,
    which is a subclass). A ``TypeError`` is raised for other types.

    Uses the Cooper approximation:
        declination = 23.45 * sin(360 * (284 + N) / 365)
    where N is the day of year. The result is given to full float
    precision.
    """
    if not isinstance(day, date):
        raise TypeError(f"Expected datetime.date, got {type(day).__name__}")

    # datetime is a subclass of date; using isinstance accepts it.
    # The time-of-day is irrelevant to declination.
    n = _day_of_year(day)
    angle_deg = 360.0 * (284 + n) / 365.0
    radians = math.radians(angle_deg)
    return 23.45 * math.sin(radians)
