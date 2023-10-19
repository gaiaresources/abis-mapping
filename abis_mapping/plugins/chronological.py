"""Provides extra frictionless date and time validation checks for the package"""


# Third-party
import frictionless
import frictionless.errors
import attrs

# Local
from abis_mapping.utils import timestamps, types

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class ChronologicalOrder(frictionless.Check):
    """Checks whether the dates or datetimes are in chronological order for each row, based on the order of the
    fields given."""

    # Check attributes
    type = "chronological-order"
    Errors = [frictionless.errors.RowConstraintError]

    # Specific to this check
    field_names: list[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the chronological order of.

        Yields:
            frictionless.Error: When the chronological order is violated.
        """
        # Get dates or datetimes
        dts: list[types.DateOrDatetime] = [row[name] for name in self.field_names if row[name] is not None]

        # Validate chronological order of the list
        chrono_valid = timestamps.is_chronologically_ordered(dts)

        # Check validity
        if not chrono_valid:
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=f"the following dates are not in chronological order: {self.field_names}; with values: {dts}"
            )
