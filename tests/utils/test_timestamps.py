"""Provides Unit Tests for the `abis_mapping.utils.timestamps` module"""


# Third-Party
import pytest

# Standard
import datetime
import contextlib

# Local
from abis_mapping import utils
from abis_mapping.utils import types

# Typing
from typing import Any, Tuple


@pytest.mark.parametrize(
    [
        "raw",
        "expected"
    ],
    [
        ("26/04/2022", "2022-04-26"),
        ("2022-04-26", "2022-04-26"),
        ("2022-04-26T22Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00.000Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00.000000Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00.000+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00.000000+08:00", "2022-04-26T22:00:00+08:00"),
    ]
)
def test_timestamp_parse_valid(raw: str, expected: str) -> None:
    """Tests the Timestamp Parser with Valid Input

    Args:
        raw (str): Raw string to parse.
        expected (str): Expected result of parsing the raw string.
    """
    # Parse Valid Timestamp
    assert utils.timestamps.parse_timestamp(raw).isoformat() == expected


@pytest.mark.parametrize(
    [
        "raw",
    ],
    [
        (123, ),
        (45.6, ),
        ("hello world", ),
        ("2022-04-26T22:00:00", ),
        ("2022", ),
        ("2022-04", ),
    ]
)
def test_timestamp_parse_invalid(raw: Any) -> None:
    """Tests the Timestamp Parser with Invalid Input

    Args:
        raw (str): Raw string to parse.
    """
    # Parse Invalid Timestamps
    with pytest.raises(ValueError):
        utils.timestamps.parse_timestamp(raw)


def test_is_chronologically_ordered() -> None:
    """Tests the is_chronologically_ordered() function."""

    # Define scenario lists
    ordered_datetimes: list[utils.types.Timestamp] = [
        datetime.datetime(2022, 9, 11, 15, 15, 15),
        datetime.datetime(2023, 9, 11, 15, 15, 15),
        datetime.date(2023, 10, 11),
        datetime.date(2023, 10, 11),
        datetime.datetime(2023, 10, 12, 0, 0, 1),
        types.YearMonth(2023, 11),
        types.YearMonth(2023, 12),
        2024,
        2024,
        types.YearMonth(2024, 1),
    ]

    unordered_datetimes_dates: list[utils.types.Timestamp] = [
        datetime.date(2022, 9, 11),
        datetime.datetime(2023, 10, 11, 15, 15, 15),
        datetime.datetime(2023, 9, 11, 15, 15, 15),
    ]

    unordered_datetimes_times: list[utils.types.Timestamp] = [
        datetime.datetime(2023, 9, 11, 15, 15, 15),
        datetime.datetime(2023, 9, 11, 15, 15, 14),
    ]

    # Check chronologically increasing
    assert utils.timestamps.is_chronologically_ordered(ordered_datetimes)
    assert not utils.timestamps.is_chronologically_ordered(unordered_datetimes_dates)
    assert not utils.timestamps.is_chronologically_ordered(unordered_datetimes_times)


@pytest.mark.parametrize(
    "year,month,expected,raise_error",
    [
        (2022, 4, 30, contextlib.nullcontext()),
        (2022, 12, 31, contextlib.nullcontext()),
        (2022, 2, 28, contextlib.nullcontext()),
        (2022, 13, 0, pytest.raises(ValueError)),
        (-5, 12, 0, pytest.raises(ValueError)),
    ]
)
def test_max_date(
    year: int,
    month: int,
    expected: int,
    raise_error: contextlib.AbstractContextManager,
) -> None:
    """Tests the functionality of the max_data function.

    Args:
        year (int): Year input
        month (int): Month input
        expected (int): Expected return
        raise_error (contextlib.AbstractContextManager | pytest.RaisesContext | pytest.ExceptionInfo):
            Exception to be raised or not.
    """
    with raise_error:
        assert utils.timestamps.max_date(year, month) == expected


# Constants to help setup the next test
dt1 = datetime.datetime(1111, 1, 1, 1, 1, 1)
dt2 = datetime.datetime(2222, 2, 2, 2, 2, 2)


@pytest.mark.parametrize(
    "inputs,expected",
    [
        # Both naive
        ((dt1, dt2), (dt1, dt2)),

        # Both timezoned same
        ((dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
          dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1)))),
         (dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
          dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))))),

        # Both timezoned different
        ((dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
          dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=2)))),
         (dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
          dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=2))))),

        # First timezoned second naive
        ((dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))), dt2),
         (dt1, dt2)),

        # Second timezoned first naive
        ((dt1, dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1)))),
         (dt1, dt2))
    ]
)
def test_set_offsets_for_comparison(
    inputs: Tuple[datetime.datetime, datetime.datetime],
    expected: Tuple[datetime.datetime, datetime.datetime],
) -> None:
    """Tests the set_offsets_for_comparison function.

    Args:
        inputs (datetime.datetime, datetime.datetime): Inputs args for the function
        expected (datetime.datetime, datetime.datetime): Expected returned
    """
    assert utils.timestamps.set_offsets_for_comparison(*inputs) == expected


# Another set of constants to help with test setup
date1 = datetime.date(2022, 4, 4)
max_time = datetime.time.max
min_time = datetime.time.min
ym1 = types.YearMonth(2022, 4)


@pytest.mark.parametrize(
    "timestamp,round_up,expected",
    [
        # datetime with timezone
        (dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
         False,
         dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1)))),
        # datetime naive
        (dt1, False, dt1),
        # date
        (date1, False, datetime.datetime.combine(date1, min_time)),
        # date roundup
        (date1, True, datetime.datetime.combine(date1, max_time)),
        # yearmonth
        (ym1, False, datetime.datetime.combine(datetime.date(ym1.year, ym1.month, 1), min_time)),
        # yearmonth roundup
        (ym1, True, datetime.datetime.combine(datetime.date(ym1.year, ym1.month, 30), max_time)),
        # year
        (2022, False, datetime.datetime.combine(datetime.date(2022, 1, 1), min_time)),
        # year roundup
        (2022, True, datetime.datetime.combine(datetime.date(2022, 12, 31), max_time)),
    ]
)
def test_transform_timestamp_to_datetime(
    timestamp: utils.types.Timestamp,
    round_up: bool,
    expected: datetime.datetime
) -> None:
    """Tests the transform_timestamp_to_datetime function.

    Args:
        timestamp (utils.types.Timestamp): Input to be converted
        round_up (bool): Whether to round up the timestamp up when converting.
        expected (datetime.datetime): Expected output
    """
    assert utils.timestamps.transform_timestamp_to_datetime(timestamp, round_up) == expected
