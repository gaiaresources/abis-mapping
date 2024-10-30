"""Provides extra frictionless lookup match checks for the package"""

# Third-Party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator, Mapping


@attrs.define(kw_only=True, repr=False)
class VLookupMatch(frictionless.Check):
    """Takes the as a key, the value of one column to perform a VLOOKUP style check.

    Validation fails if the cell value for `key_field` does not match any keys of the provided
    map. If a null value for key is encountered then check is bypassed.

    Attributes:
        key_field: name of the column to use as the key for the lookup.
        value_field: name of the column to be compared against during lookup comparison.
        lu_map: map consisting of the valid combinations value for a given key.
    """

    # Check Attributes
    type = "vlookup-match"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    key_field: str
    value_field: str
    lu_map: Mapping

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the mutual inclusion of.

        Yields:
            frictionless.Error: For when the mutual inclusion is violated.
        """
        # Check for null key
        if row[self.key_field] is None:
            # Bypass
            return 

        # Confirm key column value exists in map
        if self.lu_map.get(row[self.key_field]) is not None:
            # Extract lookup values
            expected = self.lu_map[row[self.key_field]]
            actual = row[self.value_field]

            # Perform lookup check
            if actual == expected:
                # Valid
                return
            else:
                # Customise error note for the result
                note = (
                    f"Expected cell value `{expected}` for field `{self.value_field}` given key"
                    f" `{row[self.key_field]}` for field `{self.key_field}; got `{actual}`"
                )
        else:
            # Customise note for error
            note = f"Index `{row[self.key_field]}` does not exist in the provided lookup map"

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note,
        )
