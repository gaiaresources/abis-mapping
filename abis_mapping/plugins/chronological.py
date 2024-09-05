"""Provides extra frictionless date and time validation checks for the package"""


# Third-party
import frictionless
import frictionless.errors
import attrs

# Local
from abis_mapping.types import temporal

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class ChronologicalOrder(frictionless.Check):
    """Checks whether Timestamps are in chronological order for each row, based on the order of the fields given."""

    # Check attributes
    type = "chronological-order"
    Errors = [frictionless.errors.RowConstraintError]

    # Specific to this check, names of fields all of which must be timestamp type.
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the chronological order of.

        Yields:
            frictionless.Error: When the chronological order is violated.
        """
        # Get Timestamps
        tstmps: list[temporal.Timestamp] = [row[name] for name in self.field_names if row[name] is not None]

        # Test for 0 - 1 length list
        if len(tstmps) < 2:
            return  # If there are 0 or 1 values, they are considered chronological

        # Check validity
        if not all(x <= y for x, y in zip(tstmps[:-1], tstmps[1:], strict=True)):
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=f"the following dates are not in chronological order: {self.field_names}; with values: {tstmps}"
            )
