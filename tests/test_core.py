import datetime

import dateint as di


def test_today():
    today_dt = datetime.date.today()
    today_int = di.today()

    assert int(today_dt.strftime('%Y%m%d')) == today_int
