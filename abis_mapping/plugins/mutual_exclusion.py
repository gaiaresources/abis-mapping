"""Provides extra frictionless mutual exclusion checks for the package"""


# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class MutuallyExclusive(frictionless.Check):
    """Checks that mutually exclusive columns are not provided together."""

    # Check Attributes
    type = "mutually-exclusive"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the mutual exclusivity of.

        Yields:
            frictionless.Error: For when the mutual exclusion is violated.
        """
        # Retrieve Field Names for cells with values
        fields_provided = [f for f in self.field_names if row[f] not in (None, "")]

        # Check Mutual Exclusivity
        # If 2 or more of the mutually exclusive fields are provided, that's an error.
        if len(fields_provided) >= 2:
            # Yield Error
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=(
                    f"The columns {self.field_names} are mutually exclusive and must "
                    f"not be provided together "
                    f"(columns {fields_provided} were provided together)"
                ),
            )
