import datetime

import pandas as pd
import pytest

from dateint.convert import _from_date, _to_datetime


@pytest.mark.parametrize(
    ['dt', 'fmt', 'return_type', 'exp_result'],
    [
        (datetime.date(2022, 1, 10), '%Y%m%d', str, '20220110'),
        (datetime.date(2022, 1, 10), '%Y%m%d', int, 20220110),
        (datetime.date(2022, 1, 10), '%Y%m%d', float, 20220110.0),
        (datetime.datetime(2022, 1, 10, 5, 10, 25), '%Y%m%d', str, '20220110'),
        (
            datetime.datetime(2022, 1, 10, 5, 10, 25),
            '%Y%m%d %H%M%S',
            str,
            '20220110 051025',
        ),
        (
            datetime.datetime(2020, 2, 29, 23, 59, 59),
            '%Y%m%d%H%M%S',
            int,
            20200229235959,
        ),
        (
            datetime.datetime(2020, 2, 29, 23, 59, 59),
            '%Y%m%d%H%M%S',
            float,
            20200229235959.0,
        ),
    ],
)
def test_from_date(dt, fmt, return_type, exp_result):
    assert _from_date(dt, fmt, return_type) == exp_result


@pytest.mark.parametrize(
    ['dt', 'fmt', 'return_type', 'exp_result'],
    [
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            '%Y%m%d',
            int,
            pd.Series([20200229, 20210228]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            '%Y%m%d',
            float,
            pd.Series([20200229.0, 20210228.0]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            '%Y/%m/%d',
            str,
            pd.Series(['2020/02/29', '2021/02/28']),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [
                        datetime.datetime(2020, 2, 29, 23, 59, 59),
                        datetime.datetime(2021, 2, 28, 0, 1, 2),
                    ],
                )
            ),
            '%Y%m%d%H%M%S',
            int,
            pd.Series([20200229235959, 20210228000102]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [
                        datetime.datetime(2020, 2, 29, 23, 59, 59),
                        datetime.datetime(2021, 2, 28, 0, 1, 2),
                    ],
                )
            ),
            '%Y%m%d%H%M%S',
            float,
            pd.Series([20200229235959.0, 20210228000102.0]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [
                        datetime.datetime(2020, 2, 29, 23, 59, 59),
                        datetime.datetime(2021, 2, 28, 0, 1, 2),
                    ],
                )
            ),
            '%Y-%m-%d %H:%M:%S',
            str,
            pd.Series(['2020-02-29 23:59:59', '2021-02-28 00:01:02']),
        ),
    ],
)
def test_from_date_with_pandas(dt, fmt, return_type, exp_result):
    assert all(_from_date(dt, fmt, return_type) == exp_result)


@pytest.mark.parametrize(
    ['value', 'fmt', 'exp_result'],
    [
        (20220101, '%Y%m%d', datetime.datetime(2022, 1, 1)),
        (220101, '%y%m%d', datetime.datetime(2022, 1, 1)),
        (20220101.0, '%Y%m%d', datetime.datetime(2022, 1, 1)),
        ('20220101', '%Y%m%d', datetime.datetime(2022, 1, 1)),
        ('2022/01/01', '%Y/%m/%d', datetime.datetime(2022, 1, 1)),
        ('01/01/22', '%d/%m/%y', datetime.datetime(2022, 1, 1)),
        (20220101235959, '%Y%m%d%H%M%S', datetime.datetime(2022, 1, 1, 23, 59, 59)),
        (20220101235959.0, '%Y%m%d%H%M%S', datetime.datetime(2022, 1, 1, 23, 59, 59)),
        ('20220101235959', '%Y%m%d%H%M%S', datetime.datetime(2022, 1, 1, 23, 59, 59)),
        (
            '2022-01-01 23-59-59',
            '%Y-%m-%d %H-%M-%S',
            datetime.datetime(2022, 1, 1, 23, 59, 59),
        ),
    ],
)
def test_to_datetime(value, fmt, exp_result):
    assert _to_datetime(value, fmt) == exp_result


@pytest.mark.parametrize(
    ['value', 'fmt', 'exp_result'],
    [
        (
            pd.Series([20220705, 20220801]),
            '%Y%m%d',
            pd.Series([datetime.datetime(2022, 7, 5), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([202207, 202208]),
            '%Y%m',
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([202207.0, 202208.0]),
            '%Y%m',
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series(['202207', '202208']),
            '%Y%m',
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series(['05-07/2022', '01-08/2022']),
            '%d-%m/%Y',
            pd.Series([datetime.datetime(2022, 7, 5), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([20220705235959, 20220801010203]),
            '%Y%m%d%H%M%S',
            pd.Series(
                [
                    datetime.datetime(2022, 7, 5, 23, 59, 59),
                    datetime.datetime(2022, 8, 1, 1, 2, 3),
                ]
            ),
        ),
        (
            pd.Series([20220705235959.0, 20220801010203.0]),
            '%Y%m%d%H%M%S',
            pd.Series(
                [
                    datetime.datetime(2022, 7, 5, 23, 59, 59),
                    datetime.datetime(2022, 8, 1, 1, 2, 3),
                ]
            ),
        ),
        (
            pd.Series(['20220705 235959', '20220801 010203']),
            '%Y%m%d %H%M%S',
            pd.Series(
                [
                    datetime.datetime(2022, 7, 5, 23, 59, 59),
                    datetime.datetime(2022, 8, 1, 1, 2, 3),
                ]
            ),
        ),
    ],
)
def test_to_datetime_with_pandas(value, fmt, exp_result):
    assert all(_to_datetime(value, fmt) == exp_result)
