"""Provides custom frictionless list plugin for the package"""


# Third-Party
import frictionless
import frictionless.fields
import attrs

# Typing
from typing import Any, Optional, Type


class ListPlugin(frictionless.Plugin):
    """Custom List Plugin"""

    # Class Attributes
    code = "list"

    def select_field_class(
        self,
        type: Optional[str] = None,  # noqa: A002
    ) -> Optional[Type[frictionless.Field]]:
        """Select field class for this plugin."""
        if type == self.code:
            return ListField
        return None


@attrs.define(kw_only=True, repr=False)
class ListField(frictionless.Field):
    """Custom list type implementation."""

    # Class attributes
    type = "list"
    builtin = False
    supported_constraints = [
        "required",
        "minLength",
        "maxLength",
    ]

    # Separator or delimiter, default is pipe
    delimiter: str = "|"

    def create_value_reader(self) -> frictionless.schema.types.IValueReader:
        """Creates value reader callable."""

        def value_reader(cell: Any) -> Optional[list[str]]:
            """Convert cell (read direction).

            Args:
                cell (Any): Cell to convert

            Returns:
                Optional[list[str]]: Converted cell, or none if invalid.
            """
            # Check that cell is not already a "list"
            if not isinstance(cell, list):
                # Check that cell is a string
                if not isinstance(cell, str):
                    # Invalid
                    return None

                # Create StringField instance
                string_field = frictionless.fields.StringField(
                    name="delegatedParser",
                    format=self.format
                )
                # Split, Strip, Filter and Delegate Cell Parsing to the String Type
                cell = [
                    string_field.read_cell(c.strip())[0]
                    for c in cell.split(self.delimiter) if c
                ]

                # Check for Cell Parsing Failures
                if not all(cell):
                    # Invalid
                    return None

            # Return Validated Cell
            return cell  # type: ignore[no-any-return]

        # Return value reader callable
        return value_reader

    def create_value_writer(self) -> frictionless.schema.types.IValueWriter:
        """Creates value writer callable."""
        def value_writer(cell: list[str]) -> str:
            """Convert cell (write direction).

            Args:
                cell (list): Cell to convert

            Returns:
                str: Converted cell
            """
            # Create StringField object
            string_field = frictionless.fields.StringField(
                name="delegatedSerializer",
                format=self.format,
            )

            # Join and Delegate Cell Serialization to the String Type
            return self.delimiter.join(
                string_field.write_cell(c)[0]
                for c in cell
            )

        # Return writer callable
        return value_writer

    metadata_profile_patch = {
        "properties": {
            "delimiter": {"type": "string"},
        }
    }


# Register List Plugin
frictionless.system.register(
    name=ListPlugin.code,
    plugin=ListPlugin(),
)
