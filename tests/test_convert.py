import datetime

import pandas as pd
import pytest

from dateint.convert import _first_matching_format, _from_date, _to_datetime
from dateint.exception import FloatFormatError, FormatError


@pytest.mark.parametrize(
    ["dt", "fmt", "return_type", "exp_result"],
    [
        (datetime.date(2022, 1, 10), "%Y%m%d", str, "20220110"),
        (datetime.date(2022, 1, 10), "%Y%m%d", int, 20220110),
        (datetime.date(2022, 1, 10), "%Y%m%d", float, 20220110.0),
        (datetime.datetime(2022, 1, 10, 5, 10, 25), "%Y%m%d", str, "20220110"),
        (
            datetime.datetime(2022, 1, 10, 5, 10, 25),
            "%Y%m%d %H%M%S",
            str,
            "20220110 051025",
        ),
        (
            datetime.datetime(2020, 2, 29, 23, 59, 59),
            "%Y%m%d%H%M%S",
            int,
            20200229235959,
        ),
        (
            datetime.datetime(2020, 2, 29, 23, 59, 59),
            "%Y%m%d%H%M%S",
            float,
            20200229235959.0,
        ),
    ],
)
def test_from_date(dt, fmt, return_type, exp_result):
    assert _from_date(dt, fmt, return_type) == exp_result


def test_from_date_with_invalid_type():
    invalid_value = []
    with pytest.raises(TypeError):
        _from_date(dt=invalid_value, fmt="%Y%m%d", return_type=int)


@pytest.mark.parametrize(
    ["dt", "fmt", "return_type", "exp_result"],
    [
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            "%Y%m%d",
            int,
            pd.Series([20200229, 20210228]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            "%Y%m%d",
            float,
            pd.Series([20200229.0, 20210228.0]),
        ),
        (
            pd.Series(
                pd.to_datetime(
                    [datetime.date(2020, 2, 29), datetime.date(2021, 2, 28)],
                )
            ),
            "%Y/%m/%d",
            str,
            pd.Series(["2020/02/29", "2021/02/28"]),
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
            "%Y%m%d%H%M%S",
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
            "%Y%m%d%H%M%S",
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
            "%Y-%m-%d %H:%M:%S",
            str,
            pd.Series(["2020-02-29 23:59:59", "2021-02-28 00:01:02"]),
        ),
    ],
)
def test_from_date_with_pandas(dt, fmt, return_type, exp_result):
    result = _from_date(dt, fmt, return_type)
    assert all(result == exp_result)
    assert result.dtype == exp_result.dtype


@pytest.mark.parametrize(
    ["value", "fmt", "exp_result"],
    [
        (20220101, "%Y%m%d", datetime.datetime(2022, 1, 1)),
        (220101, "%y%m%d", datetime.datetime(2022, 1, 1)),
        (20220101.0, "%Y%m%d", datetime.datetime(2022, 1, 1)),
        ("20220101", "%Y%m%d", datetime.datetime(2022, 1, 1)),
        ("2022/01/01", "%Y/%m/%d", datetime.datetime(2022, 1, 1)),
        ("01/01/22", "%d/%m/%y", datetime.datetime(2022, 1, 1)),
        (20220101235959, "%Y%m%d%H%M%S", datetime.datetime(2022, 1, 1, 23, 59, 59)),
        (20220101235959.0, "%Y%m%d%H%M%S", datetime.datetime(2022, 1, 1, 23, 59, 59)),
        ("20220101235959", "%Y%m%d%H%M%S", datetime.datetime(2022, 1, 1, 23, 59, 59)),
        (
            "2022-01-01 23-59-59",
            "%Y-%m-%d %H-%M-%S",
            datetime.datetime(2022, 1, 1, 23, 59, 59),
        ),
    ],
)
def test_to_datetime(value, fmt, exp_result):
    assert _to_datetime(value, fmt) == exp_result


@pytest.mark.parametrize(
    ["value", "fmt", "exp_result"],
    [
        (
            pd.Series([20220705, 20220801]),
            "%Y%m%d",
            pd.Series([datetime.datetime(2022, 7, 5), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([202207, 202208]),
            "%Y%m",
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([202207.0, 202208.0]),
            "%Y%m",
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series(["202207", "202208"]),
            "%Y%m",
            pd.Series([datetime.datetime(2022, 7, 1), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series(["05-07/2022", "01-08/2022"]),
            "%d-%m/%Y",
            pd.Series([datetime.datetime(2022, 7, 5), datetime.datetime(2022, 8, 1)]),
        ),
        (
            pd.Series([20220705235959, 20220801010203]),
            "%Y%m%d%H%M%S",
            pd.Series(
                [
                    datetime.datetime(2022, 7, 5, 23, 59, 59),
                    datetime.datetime(2022, 8, 1, 1, 2, 3),
                ]
            ),
        ),
        (
            pd.Series([20220705235959.0, 20220801010203.0]),
            "%Y%m%d%H%M%S",
            pd.Series(
                [
                    datetime.datetime(2022, 7, 5, 23, 59, 59),
                    datetime.datetime(2022, 8, 1, 1, 2, 3),
                ]
            ),
        ),
        (
            pd.Series(["20220705 235959", "20220801 010203"]),
            "%Y%m%d %H%M%S",
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


@pytest.mark.parametrize(
    ["value", "exp_result"],
    [
        (202211, "%Y%m"),
        ("20220304", "%Y%m%d"),
        (20220708, "%Y%m%d"),
        (20221108.0, "%Y%m%d"),
        (20221108235959, "%Y%m%d%H%M%S"),
        (20221108235950.0, "%Y%m%d%H%M%S"),
        ("20221108 235959", "%Y%m%d %H%M%S"),
    ],
)
def test_first_matching_format(value, exp_result):
    assert _first_matching_format(value) == exp_result


@pytest.mark.parametrize(
    ["value", "exp_result"],
    [
        (pd.Series([202211, 202211]), "%Y%m"),
        (pd.Series(["20220304", "20220304"]), "%Y%m%d"),
        (pd.Series([20220708, 20220708]), "%Y%m%d"),
        (pd.Series([20221108.0, 20221108.0]), "%Y%m%d"),
        (pd.Series([20221108235959, 20221108235959]), "%Y%m%d%H%M%S"),
        (pd.Series([20221108235950.0, 20221108235950.0]), "%Y%m%d%H%M%S"),
        (pd.Series(["20221108 235959", "20221108 235959"]), "%Y%m%d %H%M%S"),
    ],
)
def test_first_matching_format_with_pandas(value, exp_result):
    assert _first_matching_format(value) == exp_result


def test_float_with_non_zero_decimal_part():
    with pytest.raises(FloatFormatError):
        _first_matching_format(20220707.1)


def test_series_with_float_with_non_zero_decimal_part():
    with pytest.raises(FloatFormatError):
        _first_matching_format(pd.Series([20220707.1]))


@pytest.mark.parametrize(
    ["invalid_value"],
    [
        (2022071,),
        (202271,),
        ("asdasd",),
    ],
)
def test_invalid_format_input(invalid_value):
    with pytest.raises(FormatError, match=str(invalid_value)):
        _first_matching_format(invalid_value)


@pytest.mark.parametrize(
    ["invalid_value"],
    [
        (pd.Series([2022071, 2022071]),),
        (pd.Series(["asdasd", "asdasd"]),),
    ],
)
def test_invalid_format_input_with_pandas(invalid_value):
    with pytest.raises(FormatError, match=str(invalid_value.iloc[0])):
        _first_matching_format(invalid_value)
