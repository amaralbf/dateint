import datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

import dateint as di
from dateint.core import get_date_obj_and_format, to_int


def test_today():
    today_dt = datetime.date.today()
    today_int = di.today()

    assert int(today_dt.strftime('%Y%m%d')) == today_int


def test_add_months_same_resulting_day():
    assert di.add_months(20210127, 1) == 20210227
    assert di.add_months(20210127, -1) == 20201227

    assert di.add_months(20210131, 2) == 20210331
    assert di.add_months(20210131, -1) == 20201231

    assert di.add_months(20210131, 6) == 20210731
    assert di.add_months(20210131, -6) == 20200731

    assert di.add_months(20210101, 12) == 20220101
    assert di.add_months(20210101, -12) == 20200101

    assert di.add_months(20200229, 48) == 20240229
    assert di.add_months(20200229, -48) == 20160229


def test_add_months_different_resulting_day():
    assert di.add_months(20210131, 1) == 20210228
    assert di.add_months(20210131, -1) == 20201231

    assert di.add_months(20210131, -3) == 20201031
    assert di.add_months(20210131, 3) == 20210430

    assert di.add_months(20210531, 11) == 20220430
    assert di.add_months(20210531, -11) == 20200630

    assert di.add_months(20200229, 12) == 20210228
    assert di.add_months(20200229, -12) == 20190228


def test_add_months_yyyymm_format_int():
    assert di.add_months(202101, 1) == 202102
    assert di.add_months(202101, -1) == 202012
    assert di.add_months(202101, 12) == 202201
    assert di.add_months(202101, -12) == 202001


def test_get_date_obj_and_format_with_invalid_type():
    pytest.raises(TypeError, get_date_obj_and_format, datetime.datetime(2019, 1, 1))
    pytest.raises(TypeError, get_date_obj_and_format, None)
    pytest.raises(TypeError, get_date_obj_and_format, 20210321.0)
    pytest.raises(TypeError, get_date_obj_and_format, 202103.0)


def test_get_date_obj_and_format_with_invalid_value():
    pytest.raises(ValueError, get_date_obj_and_format, 2021030)
    pytest.raises(ValueError, get_date_obj_and_format, 20210229)

    # although single digit month/day is a valid format for datetime.datetime.strptime,
    # here, we only accept the '%Y%m%d' and '%Y%m' formats with double digits month/day
    pytest.raises(ValueError, get_date_obj_and_format, 202113)


@given(st.dates(min_value=datetime.date(2000, 1, 1)), st.integers(-360, 360))
def test_sub_months_equals_add_neg_months(date, months):
    date_int = to_int(date=date, fmt='%Y%m%d')
    assert di.sub_months(date_int, months) == di.add_months(date_int, -months)

    date_int = to_int(date=date, fmt='%Y%m')
    assert di.sub_months(date_int, months) == di.add_months(date_int, -months)
