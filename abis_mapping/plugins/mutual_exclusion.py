"""Provides extra frictionless mutual exclusion checks for the package"""


# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class MutuallyExclusive(frictionless.Check):
    """Checks whether mutually exclusive columns are provided together."""

    # Check attributes
    type = "mutually-exclusive"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Field names to perform check on
    field_names: list[str]

    # When true will allow values in more than one field
    use_or_behavior: bool = False

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the mutual exclusion of.

        Yields:
            frictionless.Error: For when the mutual exclusion is violated.
        """
        # Filter out values from row
        filtered = {field_name: row[field_name] for field_name in self.field_names if row[field_name] is not None}

        if self.use_or_behavior:
            # Allows for case that at least one value should be present
            if len(filtered) >= 1:
                return
            note = (
                f"the columns {self.field_names} are constrained by logical OR, one or more value must be provided"
            )
        else:
            # This means only one field can have a value
            if len(filtered) == 1:
                return
            note = (
                f"the columns {self.field_names} are mutually exclusive, one and only one must be provided "
                f"(columns {filtered.keys()} contained values)"
            ),

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )

