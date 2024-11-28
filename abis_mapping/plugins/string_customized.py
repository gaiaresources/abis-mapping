"""Provides the customised string frictionless plugin and field."""

# Third-Party
import attrs
import frictionless
import frictionless.fields

# Typing
from typing import Any


class CustomizedStringPlugin(frictionless.Plugin):
    """Customized String Plugin."""

    def select_field_class(
        self,
        type: str | None = None,  # noqa: A002
    ) -> type[frictionless.Field] | None:
        """This hook allows a plugin to override the class used for a field, depending on the field's type.

        Args:
            type: The type of the field.

        Returns:
            Return the class to use for the field, or None.
        """
        # Override the class for string fields with our custom class.
        if type == "string":
            return CustomizedStringField
        # Not a string field, don't override the class.
        # Frictionless will fall back to other plugins or the built-in field classes.
        return None


@attrs.define(kw_only=True, repr=False)
class CustomizedStringField(frictionless.fields.StringField):
    """Custom String Field.

    Compared to the normal string field, this class
    1. Converts any whitespace-only cell to the empty string before validating and reading it.
        This is so whitespace-only cells are treated the same as empty cells.
    """

    # Class attributes
    type = "string"
    builtin = False

    # Read

    def create_cell_reader(self) -> frictionless.schema.ICellReader:
        """Override the way that cells are read.

        NOTE we override create_cell_reader() rather than create_value_reader(), so that
        1. An all-whitespace cell is converted to an emtpy string BEFORE frictionless
            checks if the cell is an "empty value".
            This means an all-whitespace cell will be None when our code reads the
            value when mapping, the same as an empty cell.
        2. This also means that an all-whitespace cell will fail validation when the
            field is required.

        Returns:
            A function to read cell contents.
        """
        # get the cell_reader for the parent class (StringField)
        default_cell_reader = super().create_cell_reader()

        # define our custom cell reader
        def cell_reader(cell: Any) -> tuple[Any, frictionless.schema.INotes]:
            # first convert whitespace-only cell to empty string
            if isinstance(cell, str) and cell.isspace():
                cell = ""

            # then let frictionless do its normal conversions/validations
            return default_cell_reader(cell)

        return cell_reader


# Register Plugin
frictionless.system.register(
    name="customized-string",
    plugin=CustomizedStringPlugin(),
)
