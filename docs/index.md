# Dateint

[![ci-status](https://github.com/amaralbf/dateint/workflows/ci/badge.svg?event=push&branch=main)](https://github.com/amaralbf/dateint/actions?query=workflow%3Aci+event%3Apush+branch%3Amain)
![PYPI](https://img.shields.io/pypi/pyversions/dateint.svg?color=%2334D058)
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

    ```py hl_lines="6"
    import dateint as di
    import pandas as pd

    dates = pd.Series([202201, 202202, 202203])

    di.add(dates, months=2)
    '''
    0    202203
    1    202204
    2    202205
    dtype: int64
    '''
    ```

## Installation

```sh
pip install dateint
```

## Examples

**Add a time interval to a date**

```py
import dateint as di
import pandas as pd

di.add(20220510, days=15)
# 20220525

dates = pd.Series([202201, 202202, 202203])
di.add(dates, months=2)
'''
0    202203
1    202204
2    202205
dtype: int64
'''
```

**Subtract a time interval from a date**

```py
import dateint as di
import pandas as pd

di.sub(20220510, days=8)
# 20220502

dates = pd.Series([202201, 202202, 202203])
di.sub(dates, years=1)
'''
0    202101
1    202102
2    202103
dtype: int64
'''
```

**Day of week**

```py
import dateint as di
import pandas as pd

di.sub(20220510, days=8)
# 20220502

df = pd.DataFrame(
    {
        'date': [
            20220103,
            20220104,
            20220105,
            20220106,
            20220107,
            20220108,
            20220109,
        ]
    }
)

df['weekday'] = di.weekday(df['date'])
df
'''
       date  weekday
0  20220103        0
1  20220104        1
2  20220105        2
3  20220106        3
4  20220107        4
5  20220108        5
6  20220109        6
'''
```

## License

This project is licensed under the terms of the MIT license.
