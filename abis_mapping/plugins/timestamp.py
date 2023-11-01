"""Provides custom frictionless timestamp plugin for the package"""


# Standard
import datetime

# Third-Party
import frictionless

# Local
from abis_mapping.utils import types
from abis_mapping.utils import timestamps

# Typing
from typing import Any, Optional, Type


class TimestampPlugin(frictionless.Plugin):
    """Custom Timestamp Plugin"""

    # Class Attributes
    code = "timestamp"
    status = "stable"

    def select_field_class(self, type: Optional[str] = None) -> Optional[Type[frictionless.Field]]:
        """Return the custom field class for the plugin.

        Args:
            type (str): Denotes the type passed in from the frictionless
                framework for a field.

        Returns:
            Optional[Type[frictionless.Field]]: Reference to TimestampField if type
                matches code else None.
        """
        if type == self.code:
            return TimestampField
        return None


class TimestampField(frictionless.Field):
    """Custom timestamp type implementation."""

    # Class attributes
    type = "timestamp"
    builtin = False
    supported_constraints = [
        "required",
        "minimum",
        "maximum",
        "enum"
    ]

    def create_value_reader(self) -> frictionless.schema.types.IValueReader:
        """Creates value reader callable."""

        def value_reader(cell: Any) -> Optional[types.DateOrDatetime]:
            """Convert cell (read direction).

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

        # Return value_reader callable
        return value_reader

    def create_value_writer(self) -> frictionless.schema.types.IValueWriter:
        """Creates value writer callable."""
        def value_writer(cell: types.DateOrDatetime) -> str:
            """Convert cell (write direction)

            Args:
                cell (types.DateOrDatetime): Cell to convert

            Returns:
                str: Converted cell
            """
            # Serialize to ISO-8601 Format
            return cell.isoformat()

        # Return value writer callable
        return value_writer


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
