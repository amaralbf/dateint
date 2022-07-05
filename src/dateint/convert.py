"""Module for date/datetime conversion."""

import datetime
from typing import Union

import pandas as pd

DateRepresentationType = Union[float, int, str]


def _guess_format(value: Union[int, str, float]):
    """Try to infer date/datetime format from value."""
    date_str = str(int(value))
    if len(date_str) == 6:
        return '%Y%m'
    elif len(date_str) == 8:
        return '%Y%m%d'


def _from_date(
    dt: Union[datetime.date, datetime.datetime, pd.Series], fmt: str, return_type: type
) -> DateRepresentationType:
    if isinstance(dt, pd.Series):
        fmtted = dt.dt.strftime(fmt)
        return fmtted.astype(return_type)
    elif isinstance(dt, (datetime.date, datetime.datetime)):
        fmtted = dt.strftime(fmt)
        return return_type(fmtted)
    raise ValueError()


def _to_datetime(value: DateRepresentationType, fmt: str) -> datetime.datetime:
    if isinstance(value, float):
        value = int(value)
    value_str = str(value)
    dt = datetime.datetime.strptime(value_str, fmt)
    return dt
