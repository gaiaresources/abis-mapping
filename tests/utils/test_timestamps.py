"""Provides Unit Tests for the `abis_mapping.utils.timestamps` module"""


# Third-Party
import pytest

# Standard
import datetime

# Local
from abis_mapping import utils

# Typing
from typing import Any


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
    ordered_datetimes = [
        datetime.datetime(2022, 9, 11, 15, 15, 15),
        datetime.datetime(2023, 9, 11, 15, 15, 15),
        datetime.datetime(2023, 10, 11, 15, 15, 15),
    ]
    unordered_datetimes = [
        datetime.datetime(2022, 9, 11, 15, 15, 15),
        datetime.datetime(2023, 10, 11, 15, 15, 15),
        datetime.datetime(2023, 9, 11, 15, 15, 15),
    ]

    # Check chronologically increasing
    assert utils.timestamps.is_chronologically_ordered(ordered_datetimes)
    assert not utils.timestamps.is_chronologically_ordered(unordered_datetimes)

