"""Module for date/datetime conversion."""

import datetime
from typing import Union


def date_to_int(date: Union[datetime.date, datetime.datetime], fmt: str) -> int:
    """Convert date/datetime value to int."""
    return int(date.strftime(fmt))


def to_valid_str(value: Union[int, str, float]):
    """Ensure string value can be converted to int without changes."""
    return str(int(value))


def parse_to_date(value: Union[int, str, float], fmt) -> datetime.datetime:
    """Parse a literal value to date/datetime."""
    return datetime.datetime.strptime(to_valid_str(value), fmt)


def guess_format(value: Union[int, str, float]):
    """Try to infer date/datetime format from value."""
    date_str = to_valid_str(value)
    if len(date_str) == 6:
        return '%Y%m'
    elif len(date_str) == 8:
        return '%Y%m%d'
