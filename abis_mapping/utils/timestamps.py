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
