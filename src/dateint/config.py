"""Module for options and configuration."""

_date_format = '%Y%m%d'
_datetime_format = '%Y%m%d%H%M%S'


def get_date_format() -> str:
    """Return the date format according to configuration value.

    Returns:
        str: date format
    """
    return _date_format


def get_datetime_format():
    """Return the datetime format according to configuration value.

    Returns:
        str: datetime format
    """
    return _datetime_format
