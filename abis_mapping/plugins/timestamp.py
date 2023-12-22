"""Provides custom frictionless timestamp plugin for the package"""


# Third-Party
import attrs
import frictionless

# Local
from abis_mapping.utils import types

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


@attrs.define(kw_only=True, repr=False)
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

    # Flags to allow for year and yearMonth types
    allow_year: bool = False
    allow_year_month: bool = False

    def create_value_reader(self) -> frictionless.schema.types.IValueReader:
        """Creates value reader callable."""

        def value_reader(cell: Any) -> types.Timestamp | None:
            """Convert cell (read direction).

            Args:
                cell (Any): Cell to convert

            Returns:
                Optional[types.DateOrDatetime]: Converted cell, or none if invalid.
            """
            # Check cell not already timestamp value
            if isinstance(cell, types.Timestamp):
                return cell

            # Check that cell is a string
            if not isinstance(cell, str):
                # Invalid
                return None

            # Catch Parsing Errors
            try:
                # Parse and return
                result = types.parse_timestamp(cell)
                # If Year returned and not allowed, then it's invalid
                if isinstance(result, types.Year) and not self.allow_year:
                    return None
                # If YearMonth returned and not allowed, then it's invalid
                if isinstance(result, types.YearMonth) and not self.allow_year_month:
                    return None
                return result
            except ValueError:
                # Invalid
                return None

        # Return value_reader callable
        return value_reader

    def create_value_writer(self) -> frictionless.schema.types.IValueWriter:
        """Creates value writer callable."""
        def value_writer(cell: types.Timestamp) -> str:
            """Convert cell (write direction)

            Args:
                cell (types.Timestamp): Cell to convert

            Returns:
                str: Converted cell
            """
            return str(cell)

        # Return value writer callable
        return value_writer

    # Add the extra params to the metadata profile
    metadata_profile_patch = {
        "properties": {
            "allowYear": {"type": "boolean"},
            "allowYearMonth": {"type": "boolean"}
        }
    }


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
