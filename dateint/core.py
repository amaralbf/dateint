import datetime


def today() -> int:
    today_dt = datetime.date.today()
    today_int = int(today_dt.strftime('%Y%m%d'))

    return today_int
