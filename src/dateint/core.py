"""Core module of dateint."""
import datetime
from functools import wraps
from typing import Union

import pandas as pd
from dateutil.relativedelta import relativedelta

from .config import get_date_format
from .convert import _first_matching_format, _from_date, _get_return_type, _to_datetime


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


def conversion(f):
    """Decorator that wraps the date/datetime operation."""

    @wraps(f)
    def wrapper(value, *args, **kwargs):
        fmt = _first_matching_format(value)
        dt_obj = _to_datetime(value, fmt)
        dt_result = f(dt_obj, *args, **kwargs)
        return_type = _get_return_type(value)
        return _from_date(dt_result, fmt, return_type)

    return wrapper


@conversion
def add(
    value: Union[pd.Series, datetime.date, datetime.datetime],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0
):
    """Add some time interval (years, months, days, ...) to a datetime-like value."""
    if isinstance(value, pd.Series):
        return value + pd.offsets.DateOffset(years=years, months=months, days=days)
    else:
        return value + relativedelta(years=years, months=months, days=days)


@conversion
def sub(
    value: Union[pd.Series, datetime.date, datetime.datetime],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0
):
    """
    Subtract some time interval (years, months, days, ...) to a datetime-like value.

    Args:
        value (Union[pd.Series, datetime.date, datetime.datetime]): _description_
        years (int, optional): _description_. Defaults to 0.
        months (int, optional): _description_. Defaults to 0.
        days (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    if isinstance(value, pd.Series):
        return value - pd.offsets.DateOffset(years=years, months=months, days=days)
    else:
        return value - relativedelta(years=years, months=months, days=days)
