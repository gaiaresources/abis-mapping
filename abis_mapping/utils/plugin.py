"""Provides custom frictionless types for the package"""


# Standard
import contextlib
import datetime

# Third-Party
import frictionless

# Local
from abis_mapping.base import types

# Typing
from typing import Any, Optional


class TimestampPlugin(frictionless.Plugin):
    """Custom Timestamp Plugin"""

    # Class Attributes
    code = "timestamp"
    status = "stable"

    def create_type(self, field: frictionless.Field) -> Optional[frictionless.Type]:
        """Create type from this plugin

        Args:
            field (frictionless.Field): Corresponding field.

        Returns:
            Optional[frictionless.Type]: Possible type from this plugin.
        """
        # Check for our type
        if field.type == TimestampType.code:
            # Return
            return TimestampType(field)

        # Not out type
        return None


class TimestampType(frictionless.Type):
    """Custom Timestamp Type Implementation."""

    # Class Attributes
    code = "timestamp"
    builtin = False
    constraints = [
        "required",
        "minimum",
        "maximum",
        "enum",
    ]

    def read_cell(self, cell: Any) -> Optional[types.DateOrDatetime]:
        """Convert cell (read direction)

        Args:
            cell (Any): Cell to convert

        Returns:
            Optional[types.DateOrDatetime]: Converted cell, or none if invalid.
        """
        # Check that cell is not already a "date" or "datetime"
        if not isinstance(cell, (datetime.date, datetime.datetime)):
            # Check that cell is a string
            if not isinstance(cell, str):
                # Invalid
                return None

            # Catch Parsing Errors
            try:
                # Parse
                cell = parse_timestamp(cell)

            except ValueError:
                # Invalid
                return None

        # Return Validated Cell
        return cell  # type: ignore[no-any-return]

    def write_cell(self, cell: types.DateOrDatetime) -> str:
        """Convert cell (write direction)

        Args:
            cell (types.DateOrDatetime): Cell to convert

        Returns:
            str: Converted cell
        """
        # Serialize to ISO-8601 Format
        return cell.isoformat()


# Helper Functions
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
        timestamp = datetime.datetime.fromisoformat(raw)
        assert timestamp.tzinfo is not None
        return timestamp

    # Could not parse the string to a date or a datetime
    # Raise a ValueError
    raise ValueError(f"Could not parse '{raw}' as date or datetime with timezone")


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
