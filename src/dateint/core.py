"""Core module of dateint."""

import datetime
from typing import Union

import pandas as pd
from dateutil.relativedelta import relativedelta

from .config import get_date_format
from .convert import _from_date, _to_datetime, conversion


def today() -> int:
    """
    Return current date as an integer, formatted as %Y%m%d.

    Returns:
        (int): Current date as an integer, formatted as %Y%m%d.
    """
    return _from_date(datetime.date.today(), get_date_format(), int)  # type:ignore


def weekday(date: Union[str, float, int]) -> Union[pd.Series, int]:
    """
    Return day of week as returned by datetime.datetime.weekday() method.

    Return the day of week as an integer, where Monday is 0 and Sunday is 6.

    Args:
        date (Union[pd.Series, int, str, float]): a series of formatted dates/datetimes,
            or a single formatted date/datetime.

    Returns:
        (Union[pandas.Series, int]): day of week (from 0 to 6)
    """
    dt_obj = _to_datetime(date, get_date_format())
    if isinstance(dt_obj, pd.Series):
        return dt_obj.dt.weekday
    return dt_obj.weekday()


def isoweekday(date: Union[str, float, int]) -> Union[pd.Series, int]:
    """
    Return day of week as returned by datetime.datetime.isoweekday() method.

    Return the day of week as an integer, where Monday is 1 and Sunday is 7.

    Args:
        date (Union[pd.Series, int, str, float]): a series of formatted dates/datetimes,
            or a single formatted date/datetime.

    Returns:
        (Union[pandas.Series, int]): day of week (from 1 to 7)
    """
    dt_obj = _to_datetime(date, get_date_format())

    if isinstance(dt_obj, pd.Series):
        return dt_obj.apply(datetime.date.isoweekday)
    return dt_obj.isoweekday()


def add(
    date: Union[pd.Series, int, str, float],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0,
):
    """Add some time interval to a formatted date/datetime.

    Args:
        date (Union[pd.Series, int, str, float]): a series of
            formatted dates/datetimes, or a single formatted date/datetime.
        years (int, optional): number of years to add. Defaults to 0.
        months (int, optional): number of months to add. Defaults to 0.
        days (int, optional): number of days to add. Defaults to 0.

    Examples:
        ```py
        import dateint as di
        import pandas as pd

        di.add(20220510, days=15)
        # 20220525

        dates = pd.Series([202201, 202202, 202203])
        di.add(dates, months=2)
        '''
        0    202203
        1    202204
        2    202205
        dtype: int64
        '''
        ```

    Returns:
        (Union[pd.Series, int, str, float]): a series of formatted dates/datetimes, or a
            single formatted date/datetime.
    """
    return conversion(_add)(date, years=years, months=months, days=days)


def _add(
    date: Union[pd.Series, datetime.date, datetime.datetime],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0,
) -> Union[pd.Series, datetime.date, datetime.datetime]:
    if isinstance(date, pd.Series):
        return date + pd.offsets.DateOffset(years=years, months=months, days=days)
    else:
        return date + relativedelta(years=years, months=months, days=days)


def sub(
    date: Union[pd.Series, int, str, float],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0,
):
    """Subtract some time interval from a formatted date/datetime.

    Args:
        date (Union[pd.Series, int, str, float]): a series of
            formatted dates/datetimes, or a single formatted date/datetime.
        years (int, optional): number of years to subtract. Defaults to 0.
        months (int, optional): number of months to subtract. Defaults to 0.
        days (int, optional): number of days to subtract. Defaults to 0.

    Examples:
        ```py
        import dateint as di
        import pandas as pd

        di.sub(20220510, days=8)
        # 20220502

        dates = pd.Series([202201, 202202, 202203])
        di.sub(dates, years=1)
        '''
        0    202101
        1    202102
        2    202103
        dtype: int64
        '''
        ```

    Returns:
        (Union[pd.Series, int, str, float]): a series of formatted dates/datetimes, or a
            single formatted date/datetime.
    """
    return conversion(_sub)(date, years=years, months=months, days=days)


def _sub(
    date: Union[pd.Series, datetime.date, datetime.datetime],
    *,
    years: int = 0,
    months: int = 0,
    days: int = 0,
) -> Union[pd.Series, datetime.date, datetime.datetime]:
    if isinstance(date, pd.Series):
        return date - pd.offsets.DateOffset(years=years, months=months, days=days)
    else:
        return date - relativedelta(years=years, months=months, days=days)
