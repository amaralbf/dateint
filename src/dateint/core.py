"""Core module of dateint."""

import datetime


def today() -> int:
    """
    Return current date as an integer, formatted as %Y%m%d.

    Returns:
        today: Current date as an integer, formatted as %Y%m%d.
    """
    today_dt = datetime.date.today()
    today_int = int(today_dt.strftime('%Y%m%d'))

    return today_int
