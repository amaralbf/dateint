"""Module for date/datetime conversion."""

import datetime
from math import isclose
from typing import Union

import pandas as pd

from .config import get_format_candidates
from .exception import FloatFormatError, FormatError

DateRepresentationType = Union[float, int, str, pd.Series]


def _from_date(
    dt: Union[datetime.date, datetime.datetime, pd.Series], fmt: str, return_type: type
) -> DateRepresentationType:
    if isinstance(dt, pd.Series):
        fmtted = dt.dt.strftime(fmt)
        return fmtted.astype(return_type)
    elif isinstance(dt, (datetime.date, datetime.datetime)):
        fmtted = dt.strftime(fmt)
        return return_type(fmtted)
    raise TypeError(
        f'Type ({type(dt)}) of value ({dt}) is not valid for conversion from date'
    )


def _to_datetime(value: DateRepresentationType, fmt: str) -> datetime.datetime:
    if isinstance(value, pd.Series):
        return pd.Series(pd.to_datetime(value, format=fmt))
    if isinstance(value, float):
        value = int(value)
    value_str = str(value)
    dt = datetime.datetime.strptime(value_str, fmt)
    return dt


def _first_matching_format(value: DateRepresentationType) -> str:
    if isinstance(value, pd.Series):
        first_value = value.iloc[0]
        original_value = first_value
        if isinstance(first_value, float):
            frac = first_value % 1
            if not isclose(frac, 0):
                raise FloatFormatError(
                    'Float values with a non-zero decimal part are not accepted '
                    f'(first element of series: "{original_value}").'
                )
            first_value = int(first_value)
        first_value = str(first_value)

        value_length = len(first_value)
        candidates = get_format_candidates()
        for fmt, expected_length in candidates:
            try:
                if value_length != expected_length:
                    continue
                datetime.datetime.strptime(first_value, fmt)
                return fmt
            except ValueError:
                pass
        raise FormatError(
            f'First value "{original_value}" does not match any of configured formats: '
            f'{[c[0] for c in candidates]}.\n'
            'Hint: to prevent ambiguity issues, if no format is explicitly specified by'
            ' the user, all values (year, month, day, ...) must be zero-padded.'
        )
    else:
        original_value = value
        if isinstance(value, float):
            frac = value % 1
            if not isclose(frac, 0):
                raise FloatFormatError(
                    'Float values with a non-zero decimal part are not accepted '
                    f'({original_value}).'
                )
            value = int(value)
        value = str(value)

        value_length = len(value)
        candidates = get_format_candidates()
        for fmt, expected_length in candidates:
            try:
                if value_length != expected_length:
                    continue
                datetime.datetime.strptime(value, fmt)
                return fmt
            except ValueError:
                pass
        raise FormatError(
            f'First value "{original_value}" does not match any of configured formats: '
            f'{[c[0] for c in candidates]}.\n'
            'Hint: to prevent ambiguity issues, if no format is explicitly specified by'
            ' the user, all values (year, month, day, ...) must be zero-padded.'
        )


def _get_return_type(value):
    if isinstance(value, pd.Series):
        return value.dtype
    else:
        return type(value)
