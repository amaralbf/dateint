"""Core module of dateint."""

import datetime
from typing import Union

from dateutil.relativedelta import relativedelta

from .config import get_date_format
from .convert import _first_matching_format, _from_date, _to_datetime


def today() -> int:
    """
    Return current date as an integer, formatted as %Y%m%d.

    Returns:
        today (int): Current date as an integer, formatted as %Y%m%d.
    """
    return _from_date(datetime.date.today(), get_date_format(), int)  # type:ignore


def weekday(date: Union[str, float, int]) -> int:
    """
    Return day of week as returned by datetime.datetime.weekday() method.

    Return the day of week as an integer, where Monday is 0 and Sunday is 6.

    Args:
        date (Union[str, float, int]): date formatted as %Y%m%d

    Returns:
        weekday (int): day of week (from 0 to 6)
    """  # noqa: D402
    dt_obj = _to_datetime(date, get_date_format())
    return dt_obj.weekday()


def isoweekday(date: Union[str, float, int]) -> int:
    """
    Return day of week as returned by datetime.datetime.isoweekday() method.

    Return the day of week as an integer, where Monday is 1 and Sunday is 7.

    Args:
        date (Union[str, float, int]): date formatted as %Y%m%d

    Returns:
        weekday (int): day of week (from 1 to 7)
    """  # noqa: D402
    dt_obj = _to_datetime(date, get_date_format())
    return dt_obj.isoweekday()


class TimeDelta:
    """TimeDelta class."""

    def __init__(self, years=0, months=0, days=0):
        """Construct TimeDelta object."""
        self.years = years
        self.months = months
        self.days = days

    def __add__(self, other):
        """Add TimeDelta object to date/datetime-like value."""
        fmt = _first_matching_format(other)
        dt_obj = _to_datetime(other, fmt)
        dt_result = dt_obj + relativedelta(
            years=self.years, months=self.months, days=self.days
        )
        return _from_date(dt_result, fmt, type(other))

    def __radd__(self, other):
        """Add TimeDelta object to date/datetime-like value."""
        return self + other


def months(months):
    """Return number of months to add to/subtract from date/datetime-like value."""
    return TimeDelta(months=months)


def years(years):
    """Return number of years to add to/subtract from date/datetime-like value."""
    return TimeDelta(years=years)


def days(days):
    """Return number of days to add to/subtract from date/datetime-like value."""
    return TimeDelta(days=days)


def timedelta(*, years=0, months=0, days=0):
    """Return TimeDelta object to add to/subtract from date/datetime-like value."""
    return TimeDelta(years=years, months=months, days=days)
