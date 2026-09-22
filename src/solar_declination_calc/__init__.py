"""Solar declination calculation library.

Exposes a single function, declination, for computing the solar
declination angle on a given day of the year.
"""

from .core import declination

__all__ = ["declination"]
