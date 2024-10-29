"""Provides extra frictionless chained inclusion checks for the package"""

# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class ChainedInclusion(frictionless.Check):
    """Checks whether chained inclusion columns are provided together.

    Observes the order in which the field_names were provided. If the first
    provided field's cell is null then the check is valid. If provided, then
    all other fields' cells must contain values.
    """

    # Check Attributes
    type = "chained-inclusion"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the chained inclusion of.

        Yields:
            frictionless.Error: For when the chained inclusion is violated.
        """
        # Check first field has value
        if row[self.field_names[0]] is None:
            # Valid
            return

        # Get missing field names
        missing = [name for name in self.field_names[1:] if row[name] is None]

        # Check chained inclusion
        # missing must be empty
        if not missing:
            # Valid
            return

        note = (
            f"the columns {self.field_names} are chained inclusive and values"
            " must be provided together if its preceding field contains a value"
            f" (columns {missing} are missing values)"
        )

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )
