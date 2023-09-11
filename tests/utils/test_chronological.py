"""Provides unit tests for the `abis_mapping.utils.chronological` module."""

# Standard
import datetime

# Local
from abis_mapping.utils import chronological


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
    assert chronological.is_chronologically_ordered(ordered_datetimes)
    assert not chronological.is_chronologically_ordered(unordered_datetimes)

