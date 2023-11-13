"""Provides extra frictionless mutual exclusion checks for the package"""


# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class LogicalOr(frictionless.Check):
    """Checks whether logical OR columns are provided together."""

    # Check attributes
    type = "logical-or"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Field names to perform check on
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the mutual exclusion of.

        Yields:
            frictionless.Error: For when the mutual exclusion is violated.
        """
        # Filter out field names that contain values
        filtered = [field_name for field_name in self.field_names if row[field_name] is not None]

        # Check for at least one value provided
        if len(filtered) > 0:
            return

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=(
                f"the columns {self.field_names} are constrained by logical OR, one or more value must be provided"
            )
        )

