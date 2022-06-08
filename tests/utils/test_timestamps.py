"""Provides Unit Tests for the `abis_mapping.utils.coords` module"""


# Third-Party
import pytest

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
