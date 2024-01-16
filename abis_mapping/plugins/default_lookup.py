"""Provides extra frictionless default lookup checks for the package."""


# Third-party
import attrs
import frictionless
import frictionless.errors

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class DefaultLookup(frictionless.Check):
    """Checks whether default value is provided for keyed value in other field."""

    # Check attributes
    type = "default-lookup"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Name of field used for default map lookup
    key_field: str
    # Name of field which default map value corresponds
    value_field: str
    # Default map consisting of keys from key_field and values for value_field
    default_map: dict

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate given row (on every row)

        Args:
            row (frictionless.Row): The row to check defaults for

        Yields::
           frictionless.Error: When the default lookup fails
        """
        # Determine if field value already exists
        if row[self.value_field] is not None:
            return

        # Determine if default value entry exists
        if row[self.key_field] in self.default_map:
            return

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=(
                f"'{self.key_field}': '{row[self.key_field]}' has no default value "
                f"for field '{self.value_field}' and no other value provided."
            )
        )
