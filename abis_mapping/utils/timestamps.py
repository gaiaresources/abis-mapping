"""Provides timestamp utilities for the package"""


# Standard
import contextlib
import datetime

# Third-Party
import dateutil.parser

# Local
from . import types


def parse_timestamp(raw: str) -> types.DateOrDatetime:
    """Parses a string to a date or datetime with timezone

    This function allows for the following formats:
        (1): ISO86001 Date
        (2): dd/mm/YYYY Date
        (3): ISO86001 Datetime with Timezone

    Args:
        raw (str): Raw string to be parsed

    Returns:
        types.DateOrDatetime: Either a date or timezone aware datetime.

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


def is_chronologically_ordered(dates_or_datetimes: list[types.DateOrDatetime]) -> bool:
    """Tests the chronological ordering of a given list of dates or datetimes.

    If two dates are compared with the same value then they are translated to
    have occurred at the beginning or end of the day depending on which operand
    of the comparison the date falls on in a given iteration i.e. if the same date
    is found then it is deemed in order.

    Args:
        dates_or_datetimes (list[types.DateOrDatetime]): Dates or datetimes to be checked

    Returns:
        True if all dates or datetimes in the given list are monotonically increasing else False
        It returns True for empty or single value list.
    """
    # Test for 0 - 1 length list
    if len(dates_or_datetimes) < 2:
        return True  # If there are 0 or 1 dates or datetimes, they are considered chronological

    # Iterate through the values and determine if each greater than the previous
    for i in range(len(dates_or_datetimes) - 1):
        elem1 = dates_or_datetimes[i]
        elem2 = dates_or_datetimes[i + 1]
        # Perform a conversion to datetime if a date is found
        if type(elem1) is datetime.date:
            elem1 = datetime.datetime.combine(elem1, datetime.datetime.min.time())
        if type(elem2) is datetime.date:
            elem2 = datetime.datetime.combine(elem2, datetime.datetime.max.time())
        if elem1 > elem2:
            return False

    return True
