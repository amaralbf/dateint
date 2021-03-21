import datetime
from typing import Tuple, TypeVar

from dateutil.relativedelta import relativedelta

T = TypeVar('T', int, str)


def today() -> int:
    today_dt = datetime.date.today()
    today_int = int(today_dt.strftime('%Y%m%d'))

    return today_int


def add_months(date: T, months: int) -> int:
    dt, fmt = get_date_obj_and_format(date)
    dt_after_add = dt + relativedelta(months=months)
    date_int = to_int(dt_after_add, fmt)

    return date_int


def get_date_obj_and_format(date: T) -> Tuple[datetime.datetime, str]:
    if not isinstance(date, (int, str)):
        raise TypeError("'date' argument must be of type 'int' or 'str'")

    date_str = str(date)
    if len(date_str) == 6:
        fmt = '%Y%m'
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt, fmt
        except ValueError:
            pass
    elif len(date_str) == 8:
        fmt = '%Y%m%d'
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt, fmt
        except ValueError:
            pass

    raise ValueError("expected one of the following formats for 'date': %Y%m or %Y%m%d")


def to_int(date: datetime.datetime, fmt: str) -> int:
    return int(date.strftime(fmt))
