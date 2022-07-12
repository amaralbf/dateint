import datetime

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.pandas import range_indexes, series

import dateint as di
from dateint.config import get_date_format

# from dateint.exception import FormatError


def test_today():
    today_dt = datetime.date.today()
    today_int = di.today()

    fmt = get_date_format()
    assert int(today_dt.strftime(fmt)) == today_int


@pytest.mark.parametrize(
    ['date'],
    [
        (20220627,),
        (20220628,),
        (20220629,),
        (20220630,),
        (20220701,),
        (20220702,),
        (20220703,),
        (20220710,),
        (20220710,),
    ],
)
def test_weekday(date):
    assert di.weekday(date) == datetime.date.weekday(
        datetime.datetime.strptime(str(date), get_date_format())
    )


def test_weekday_with_pandas():
    dates = pd.Series(
        [
            20220103,
            20220104,
            20220105,
            20220106,
            20220107,
            20220108,
            20220109,
        ]
    )
    assert all(di.weekday(dates) == pd.Series([0, 1, 2, 3, 4, 5, 6]))


@pytest.mark.parametrize(
    ['date', 'exp_isoweekday'],
    [
        (20220627, 1),
        (20220628, 2),
        (20220629, 3),
        (20220630, 4),
        (20220701, 5),
        (20220702, 6),
        (20220703, 7),
        (20220710, 7),
    ],
)
def test_isoweekday(date, exp_isoweekday):
    assert di.isoweekday(date) == exp_isoweekday


def test_isoweekday_with_pandas():
    dates = pd.Series(
        [
            20220103,
            20220104,
            20220105,
            20220106,
            20220107,
            20220108,
            20220109,
        ]
    )
    assert all(di.isoweekday(dates) == pd.Series([1, 2, 3, 4, 5, 6, 7]))


@pytest.mark.parametrize(
    ['value', 'years', 'months', 'days', 'exp_result'],
    [
        (
            pd.Series([20220705, 20220801]),
            1,
            1,
            1,
            pd.Series([20230806, 20230902]),
        ),
        (
            pd.Series([202207, 202208]),
            1,
            1,
            0,
            pd.Series([202308, 202309]),
        ),
        (
            pd.Series([202207, 202208]),
            1,
            1,
            1,
            pd.Series([202308, 202309]),
        ),
        (
            pd.Series([202207, 202208]),
            1,
            1,
            32,
            pd.Series([202309, 202310]),
        ),
    ],
)
def test_add_with_pandas(value, years, months, days, exp_result):
    assert di.add(value, years=years, months=months, days=days).equals(exp_result)


@pytest.mark.parametrize(
    ['value', 'years', 'months', 'days', 'exp_result'],
    [
        (20220705, 1, 1, 1, 20230806),
        (202207, 1, 1, 0, 202308),
        (202207, 1, 1, 1, 202308),
        (202207, 1, 1, 32, 202309),
    ],
)
def test_add_with_scalar(value, years, months, days, exp_result):
    result = di.add(value, years=years, months=months, days=days)
    assert result == exp_result
    assert type(result) == type(exp_result)


@given(
    st.dates(min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1)),
    st.integers(-100, 100),
    st.integers(-100, 100),
    st.integers(-1000, 1000),
)
def test_sub_is_inverse_add_with_scalar(date, years, months, days):
    fmt = '%Y%m%d'
    date_as_str = date.strftime(fmt)

    kwargs = {'years': years, 'months': months, 'days': days}
    negative_kwargs = {'years': -years, 'months': -months, 'days': -days}

    add_result = di.add(date_as_str, **kwargs)
    sub_result = di.sub(date_as_str, **negative_kwargs)
    assert add_result == sub_result
    assert type(add_result) == type(sub_result)


@given(
    series(
        elements=st.dates(
            min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1)
        ),
        index=range_indexes(1, 10),
    ),
    st.integers(-100, 100),
    st.integers(-100, 100),
    st.integers(-1000, 1000),
)
def test_sub_is_inverse_add_with_pandas(dates, years, months, days):
    fmt = '%Y%m%d'
    date_as_str = pd.to_datetime(dates).dt.strftime(fmt)

    kwargs = {'years': years, 'months': months, 'days': days}
    negative_kwargs = {'years': -years, 'months': -months, 'days': -days}

    add_result = di.add(date_as_str, **kwargs)
    sub_result = di.sub(date_as_str, **negative_kwargs)
    assert add_result.equals(sub_result)
