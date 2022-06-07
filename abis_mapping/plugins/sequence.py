"""Provides custom frictionless sequence plugin for the package"""


# Third-Party
import frictionless

# Typing
from typing import Any, Optional


class SequencePlugin(frictionless.Plugin):
    """Custom Sequence Plugin"""

    # Class Attributes
    code = "sequence"
    status = "stable"

    def create_type(self, field: frictionless.Field) -> Optional[frictionless.Type]:
        """Create type from this plugin

        Args:
            field (frictionless.Field): Corresponding field.

        Returns:
            Optional[frictionless.Type]: Possible type from this plugin.
        """
        # Check for our type
        if field.type == SequenceType.code:
            # Return
            return SequenceType(field)

        # Not our type
        return None


class SequenceType(frictionless.Type):
    """Custom Sequence Type Implementation."""

    # Class Attributes
    code = "sequence"
    builtin = False
    constraints = [
        "required",
        "minLength",
        "maxLength",
        # "pattern",  # TODO -> Check whether this works
        # "enum",  # TODO -> Check whether this works
    ]

    # Delimiter
    delimiter = " "

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

            # Split and Delegate Cell Parsing to the String Type
            cell = [
                frictionless.types.StringType.read_cell(self, c)
                for c in cell.split(self.delimiter)
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


# Register Sequence Plugin
frictionless.system.register(
    name=SequencePlugin.code,
    plugin=SequencePlugin(),
)
