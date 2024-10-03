"""Provides extra frictionless logical OR checks for the package"""

# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator, Any


@attrs.define(kw_only=True, repr=False)
class LogicalOr(frictionless.Check):
    """Checks whether logical OR columns are provided together."""

    # Check attributes
    type = "logical-or"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Field names to perform check on
    field_names: list[str]

    # Special case check, occurs if value not provided in field_names
    # fields then checks current row field provided as key to foreign_keys
    # and ensures its value is provided in the corresponding set.
    foreign_keys: dict[str, set[Any]] = dict()

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the logical OR of.

        Yields:
            frictionless.Error: For when the logical OR condition is violated.
        """
        # Filter out field names that contain values
        filtered = [field_name for field_name in self.field_names if row[field_name] is not None]

        # Check for at least one value provided
        if len(filtered) > 0:
            return

        # Perform special case check on foreign key sets
        row_fk_map = {
            field_name: row[field_name] for field_name, fk_set in self.foreign_keys.items() if row[field_name] in fk_set
        }

        # If there is at least one item in the dictionary then it is deemed valid.
        if len(row_fk_map) > 0:
            return

        # Create error note base on values provided to the check
        note = f"the fields {self.field_names}"
        note += f" and foreign key fields {self.foreign_keys.keys()}" if len(self.foreign_keys) > 0 else ""
        note += " are constrained by logical OR, one or more value must be provided"

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )
