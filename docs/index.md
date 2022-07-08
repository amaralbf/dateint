# Dateint

[![ci-status](https://github.com/amaralbf/dateint/workflows/ci/badge.svg?event=push&branch=main)](https://github.com/amaralbf/dateint/actions?query=workflow%3Aci+event%3Apush+branch%3Amain)
![PYPI](https://img.shields.io/pypi/pyversions/dateint.svg?color=%2334D058)
[![Downloads](https://img.shields.io/pypi/dm/dateint)](https://pypistats.org/packages/dateint)
[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)

It's very common to store date/datetimes as **integers** or **strings** using formats
such as `YYYYmmdd` or `YYYYmm`. In python, to perform date/datetime arithmetic on those
values, one needs to:

1. convert the original value to `date` or `datetime`
2. perform the date/datetime operation
3. convert the result back to the original format

With `dateint`, we **abstract** all convertion operations so you can focus on the
**arithmetic step**:

- **single value:**

    ```py hl_lines="3"
    import dateint as di

    di.add(20220510, days=15)
    # 20220525
    ```

- **pandas:**

    ```py hl_lines="7"
    import dateint as di
    import pandas as pd

    dates = pd.Series([202201, 202202, 202203])

    # Pandas support
    di.add(dates, months=2)
    """
    0    202203
    1    202204
    2    202205
    dtype: int64
    """
    ```
