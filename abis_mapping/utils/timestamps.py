"""Provides timestamp utilities for the package"""


# Standard
import contextlib
import datetime

# Third-Party
import dateutil.parser

# Local
from . import types

# Typing
from typing import Tuple


def parse_timestamp(raw: str) -> datetime.datetime | datetime.date:
    """Parses a string to a date or datetime with timezone

    This function allows for the following formats:
        (1): ISO86001 Date
        (2): dd/mm/YYYY Date
        (3): ISO86001 Datetime with Timezone

    Args:
        raw (str): Raw string to be parsed

    Returns:
        datetime.datetime | datetime.date: Either a date or timezone aware datetime.

    Raises:
        ValueError: Raised if the string cannot be parsed as either a date or
            timezone aware datetime
    """
    # (1) Try Parse as ISO86001 Date
    with contextlib.suppress(Exception):
        return datetime.date.fromisoformat(raw)

    # (2) Try Parse as `dd/mm/YYYY` Date
    with contextlib.suppress(Exception):
        return datetime.datetime.strptime(raw, "%d/%m/%Y").date()

    # (3) Try Parse as ISO Datetime with Timezone
    with contextlib.suppress(Exception):
        assert len(raw) > 10  # Shortcut to disable some formats we don't want
        timestamp = dateutil.parser.isoparse(raw)
        assert timestamp.tzinfo is not None
        return timestamp

    # Could not parse the string to a date or a datetime
    # Raise a ValueError
    raise ValueError(f"Could not parse '{raw}' as date or datetime with timezone")


def is_chronologically_ordered(timestamps: list[types.Timestamp]) -> bool:
    """Tests the chronological ordering of a given list of dates or datetimes.

    If two dates are compared with the same value then they are translated to
    have occurred at the beginning or end of the day depending on which operand
    of the comparison the date falls on in a given iteration i.e. if the same date
    is found then it is deemed in order.

    Args:
        timestamps (list[types.Timestamp]): Values to be checked

    Returns:
        True if all timestamps in the given list are monotonically increasing else False
        It returns True for empty or single value list.
    """
    # Test for 0 - 1 length list
    if len(timestamps) < 2:
        return True  # If there are 0 or 1 values, they are considered chronological

    # Iterate through the values and determine if each greater than the previous
    for i in range(len(timestamps) - 1):
        # Retrieve element pairs from list and convert to datetime (if necessary)
        elem1 = transform_timestamp_to_datetime(timestamps[i], round_up=False)
        elem2 = transform_timestamp_to_datetime(timestamps[i + 1], round_up=True)

        # Cleanse datetimes to allow for comparison of offset-naive to offset-aware datetimes
        (elem1, elem2) = set_offsets_for_comparison(elem1, elem2)

        # Compare
        if elem1 > elem2:
            return False

    return True





def transform_timestamp_to_datetime(timestamp: types.Timestamp, round_up: bool = False) -> datetime.datetime:
    """Converts a timestamp to a datetime object.

    Args:
        timestamp (types.Timestamp): timestamp to convert.
        round_up (bool): If true, round up the timestamp to the max month/day/time for
            data missing else round down.

    Returns:
        datetime.datetime: converted timestamp.
    """
    # Match the type pattern (except year)
    match timestamp:
        # Datetime case
        case datetime.datetime():
            # No conversion necessary
            return timestamp
        # Date case
        case datetime.date():
            # Return datetime with max time if round up else min time
            time = datetime.datetime.max.time() if round_up else datetime.datetime.min.time()
            return datetime.datetime.combine(date=timestamp, time=time)
        # Yearmonth case
        case types.YearMonth(_year=year, _month=month):
            # Create date with max day if round_up else 1 and recursively call
            day = max_date(year, month) if round_up else 1
            return transform_timestamp_to_datetime(datetime.date(year, month, day), round_up=round_up)

    # Handle the year only case
    if isinstance(timestamp, int):
        # Max out month and day if round up else 1 for both
        month = 12 if round_up else 1
        day = max_date(year=timestamp, month=month) if round_up else 1
        # Recursively call with date
        return transform_timestamp_to_datetime(
            timestamp=datetime.date(year=timestamp, month=month, day=day),
            round_up=round_up
        )

    # Should not reach this point if type annotation adhered to
    raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")



