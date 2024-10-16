"""Provides extra frictionless mutual inclusion checks for the package"""

# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator, Any


@attrs.define(kw_only=True, repr=False)
class MutuallyInclusive(frictionless.Check):
    """Checks whether mutually inclusive columns are provided together."""

    # Check Attributes
    type = "mutually-inclusive"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    field_names: list[str]

    # Special case check, occurs if value not provided in field_names
    # fields then checks current row field provided as key to whitelists
    # and ensures its value is provided in the corresponding set. If so then
    # condition is bypassed for this row.
    whitelists: dict[str, set[Any]] = dict()

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

        # Perform special case check on foreign key sets
        row_fk_map = {
            field_name: row[field_name] for field_name, fk_set in self.whitelists.items() if row[field_name] in fk_set
        }

        # If there is at least one item in the dictionary then it is deemed valid.
        if len(row_fk_map) > 0:
            return

        note = f"the columns {self.field_names} are mutually inclusive and values must be provided together "

        if len(self.whitelists) > 0:
            note += (
                f" or a given value must be referenced by one of the supplied whitelist fields"
                f" {self.whitelists.keys()}"
            )
        note += f"(columns {missing} are missing values)"

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )
