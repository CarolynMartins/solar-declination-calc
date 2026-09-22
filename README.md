# Solar Declination Calc

Computes the solar declination angle for any day of the year using the Cooper approximation.

```python
from datetime import date
from solar_declination_calc import declination

print(declination(date(2023, 6, 21)))  # ~23.45
```

The library exposes a single function, `declination(day)`, which takes a `datetime.date` or `datetime.datetime` and returns the declination angle in degrees as a float.

## Why this exists

Solar declination is needed for calculating sunrise, sunset, and solar position. This package provides a dependency-free implementation of a simple, well-known approximation that is adequate for many engineering and educational purposes. The trade-off is accuracy: the Cooper formula can differ from the true declination by up to about 0.5 degrees.

## Edge case

The approximation treats the year as having 365 days in the sine argument, which causes a slight shift in leap years. The implementation uses the actual day-of-year, so the result on a given calendar date is consistent, but the declination on March 1 in a leap year will be about 0.4 degrees less than in a non-leap year.
