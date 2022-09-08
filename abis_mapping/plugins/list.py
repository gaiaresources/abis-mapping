"""Provides custom frictionless list plugin for the package"""


# Standard
import re

# Third-Party
import frictionless

# Typing
from typing import Any, Optional


# Code and Delimiter Detection Regex
REGEX_CODE_DELIMITER = re.compile(r"^list(?:\[(.+)\])?$")


class ListPlugin(frictionless.Plugin):
    """Custom List Plugin"""

    # Class Attributes
    code = "list"
    status = "stable"

    def create_type(self, field: frictionless.Field) -> Optional[frictionless.Type]:
        """Create type from this plugin

        Args:
            field (frictionless.Field): Corresponding field.

        Returns:
            Optional[frictionless.Type]: Possible type from this plugin.
        """
        # Perform Regex
        matches = REGEX_CODE_DELIMITER.match(field.type)

        # Check for Match
        if matches:
            # Extract Delimiter
            delimiter = matches.group(1)

            # Create List Type
            field_type = ListType(field)

            # Set Delimiter
            field_type.delimiter = delimiter or ListType.delimiter  # Handle Default

            # Return
            return field_type

        # Not our type
        return None


class ListType(frictionless.Type):
    """Custom List Type Implementation."""

    # Class Attributes
    code = "list"
    builtin = False
    constraints = [
        "required",
        "minLength",
        "maxLength",
        # "pattern",  # TODO -> Check whether this works
        # "enum",  # TODO -> Check whether this works
    ]

    # Serialization and Deserialization Delimiter
    delimiter = " "  # Default Delimiter is Space

    def read_cell(self, cell: Any) -> Optional[list[str]]:
        """Convert cell (read direction)

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

            # Split, Strip, Filter and Delegate Cell Parsing to the String Type
            cell = [
                frictionless.types.StringType.read_cell(self, c.strip())
                for c in cell.split(self.delimiter) if c
            ]

            # Check for Cell Parsing Failures
            if not all(cell):
                # Invalid
                return None

        # Return Validated Cell
        return cell  # type: ignore[no-any-return]

    def write_cell(self, cell: list[str]) -> str:
        """Convert cell (write direction)

        Args:
            cell (list): Cell to convert

        Returns:
            str: Converted cell
        """
        # Join and Delegate Cell Serialization to the String Type
        return self.delimiter.join(
            frictionless.types.StringType.write_cell(self, c)
            for c in cell
        )


# Register List Plugin
frictionless.system.register(
    name=ListPlugin.code,
    plugin=ListPlugin(),
)
