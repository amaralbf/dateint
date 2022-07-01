import datetime

import pytest

import dateint as di


def test_today():
    today_dt = datetime.date.today()
    today_int = di.today()

    assert int(today_dt.strftime('%Y%m%d')) == today_int


@pytest.mark.parametrize(
    ['date', 'exp_weekday'],
    [
        (20220627, 0),
        (20220628, 1),
        (20220629, 2),
        (20220630, 3),
        (20220701, 4),
        (20220702, 5),
        (20220703, 6),
        (20220710, 6),
    ],
)
def test_weekday(date, exp_weekday):
    assert di.weekday(date) == exp_weekday
