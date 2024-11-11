"""Provides extra frictionless bypassable row-wise required checks for the package"""

# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterable


@attrs.define(kw_only=True, repr=False)
class RequiredEnhanced(frictionless.Check):
    """Checks whether specified columns are all provided in a row-wise manner.

    It also allows the bypassing of the constraint through the provision
    of whitelists. This check is only effective when the original
    schema for each field is `required = False`, otherwise the check,
    does nothing.

    Attributes:
        field_names (list[str]): Names of fields in the row to be checked.
        whitelists (dict[str, set]): A dictionary with the key corresponding
            to a fieldname in the row, not necessarily provided in `field_names,
            which contains a set of values which will allow the check to be
            bypassed, if encountered as a value in any of that given row's
            corresponding fields' cells
    """

    # Check Attributes
    type = "required-enhanced"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    field_names: list[str]
    whitelists: dict[str, set] = {}

    def validate_start(self) -> Iterable[frictionless.Error]:
        """Called to validate the resource after opening

        Yields:
            Error: found errors
        """
        # Check whitelist keys correspond to fields
        for f in self.whitelists:
            if f not in self.resource.schema.field_names:
                note = f"required enhanced value check requires field {f} to exist"
                yield frictionless.errors.CheckError(note=note)

    def validate_row(self, row: frictionless.Row) -> Iterable[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the required enhanced of.

        Yields:
            frictionless.Error: For when the required enhanced is violated.
        """
        # Retrieve Field Names for Missing Cells
        missing = [f for f in self.field_names if not row[f]]

        # Check to see if any missing fields found
        if len(missing) == 0:
            return

        # Determine if rule is bypassable
        bypassable_values = [row[k] for k, v in self.whitelists.items() if row[k] in v]
        if len(bypassable_values) > 0:
            return

        note = f"the columns {self.field_names} are all required"
        if self.whitelists:
            note += (
                f" unless the values provided in fields {self.whitelists.keys()}"
                " match any of those in their supplied whitelists"
            )
        note += f" ({missing} are missing)."

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )
