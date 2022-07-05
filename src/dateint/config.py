"""Module for options and configuration."""

DEFAULT_FORMAT = '%Y%m%d'

DEFAULT_FORMAT_CANDIDATES = ['%Y%m%d', '%Y%m', '%Y%m%d%H%M%S', '%Y%m%d %H%M%S']


def get_date_format() -> str:
    """Return the date format according to configuration value.

    Returns:
        str: date format
    """
    return DEFAULT_FORMAT


def get_format_candidates() -> list[str]:
    return DEFAULT_FORMAT_CANDIDATES
