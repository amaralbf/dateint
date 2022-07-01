"""Core module of dateint."""

import datetime
from typing import Union


def today() -> int:
    """
    Return current date as an integer, formatted as %Y%m%d.

    Returns:
        today (int): Current date as an integer, formatted as %Y%m%d.
    """
    today_dt = datetime.date.today()
    today_int = int(today_dt.strftime('%Y%m%d'))

    return today_int


def weekday(date: Union[str, float, int]) -> int:
    """
    Return day of week as returned by datetime.datetime.strptime() method.

    Return the day of week as an integer, where Monday is 0 and Sunday is 6.

    Args:
        date (Union[str, float, int]): date formatted as %Y%m%d

    Returns:
        weekday (int): day of week (from 0 to 6)
    """
    date = str(int(date))
    dt_obj = datetime.datetime.strptime(date, '%Y%m%d')
    return dt_obj.weekday()
