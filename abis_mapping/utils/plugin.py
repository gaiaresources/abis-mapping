"""Provides custom frictionless types for the package"""


# Standard
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
        return cell

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
    """Parses an ISO8601 string to a date or datetime with timezone

    Args:
        raw (str): Raw ISO8601 string to be parsed

    Returns:
        types.DateOrDatetime: Either a date or timezone aware datetime.

    Raises:
        ValueError: Raised if the string cannot be parsed as either a date or
            timezone aware datetime
    """
    # Catch Errors
    try:
        # Parse as `date` first
        timestamp = datetime.date.fromisoformat(raw)

    except ValueError as exc:
        # Timestamp is not a date, try `datetime`
        timestamp = datetime.datetime.fromisoformat(raw)

        # Check for Timezone
        if not timestamp.tzinfo:
            # Re-Raise Error
            raise ValueError("Datetime must include timezone") from exc

    # Return
    return timestamp


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
