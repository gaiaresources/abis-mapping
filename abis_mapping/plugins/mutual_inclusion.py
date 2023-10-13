"""Provides extra frictionless mutual inclusion checks for the package"""


# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Any, Iterator

@attrs.define(kw_only=True, repr=False)
class MutuallyInclusive(frictionless.Check):
    """Checks whether mutually inclusive columns are provided together."""

    # Check Attributes
    type = "mutually-inclusive"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the mutual inclusion of.

        Yields:
            frictionless.Error: For when the mutual inclusion is violated.
        """
        # Retrieve Field Names for Missing Cells
        missing = [f for f in self.field_names if not row[f]]

        # Check Mutual Inclusivity
        # Either none of the cells must be missing, or all of them must be
        # missing, which is checked below by comparing the number of missing
        # cells against the expected number of cells
        if len(missing) in (0, len(self.field_names)):
            # Short-circuit
            return

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=(
                f"the columns {self.field_names} are mutually inclusive and must be provided together "
                f"(columns {missing} are missing)"
            ),
        )
