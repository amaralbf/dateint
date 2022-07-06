import datetime

import pytest
from dateutil.relativedelta import relativedelta
from hypothesis import given, settings
from hypothesis import strategies as st

import dateint as di
from dateint.config import get_date_format
from dateint.exception import UnknownFormatError


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
def test_weekday_of_date(date):
    assert di.weekday(date) == datetime.date.weekday(
        datetime.datetime.strptime(str(date), get_date_format())
    )


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


@pytest.mark.parametrize(
    ['date', 'months', 'exp_date'],
    [
        (202207, 5, 202212),
        (20220702, 5, 20221202),
        (20220731, 4, 20221130),
        (20200229, 4, 20200629),
    ],
)
def test_add_months(date, months, exp_date):
    assert date + di.months(months) == exp_date


def test_add_months_to_invalid_value():
    with pytest.raises(UnknownFormatError):
        '2022/07/22' + di.months(1)


@given(st.dates(min_value=datetime.date(1000, 1, 1)))
@settings(max_examples=1000)
def test_timedelta(date):
    fmt = '%Y%m%d'
    kwargs = {'years': 1, 'months': 1, 'days': 1}

    print(date)
    from_dateutil = (date + relativedelta(**kwargs)).strftime(fmt)
    from_dateint = date.strftime(fmt) + di.timedelta(**kwargs)

    assert from_dateutil == from_dateint
