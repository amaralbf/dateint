"""Module for options and configuration."""

from typing import List, Tuple

DEFAULT_FORMAT = "%Y%m%d"

DEFAULT_FORMAT_CANDIDATES = [
    ("%Y%m", 6),
    ("%Y%m%d", 8),
    ("%Y%m%d%H%M%S", 14),
    ("%Y%m%d %H%M%S", 15),
]


def get_date_format() -> str:
    """Return the date format according to configuration value.

    Returns:
        str: date format
    """
    return DEFAULT_FORMAT


def get_format_candidates() -> List[Tuple[str, int]]:
    """Return a sequence of date format candidates to try parsing the input value.

    Returns:
        List[Tuple[str, int]]: sequence of date format candidates, begin the first
            element of the tuple the format string, and the second the expected length
            of the input value.
    """
    return DEFAULT_FORMAT_CANDIDATES
