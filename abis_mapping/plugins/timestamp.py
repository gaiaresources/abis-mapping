"""Provides custom frictionless timestamp plugin for the package"""


# Standard
import datetime

# Third-Party
import frictionless

# Local
from abis_mapping.utils import types
from abis_mapping.utils import timestamps

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

        # Not our type
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
                cell = timestamps.parse_timestamp(cell)

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


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
