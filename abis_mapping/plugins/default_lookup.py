"""Provides extra frictionless default lookup checks for the package."""

# Standard Library
from collections.abc import Mapping

# Third-party
import attrs
import frictionless
import frictionless.errors

# Typing
from typing import Callable, Iterator


# TODO remove once SSD v2 removed.
_default_error_template = (
    "'{key_field}': '{key_value}' has no default value for field '{value_field}' and no other value provided."
)


@attrs.define(kw_only=True, repr=False)
class DefaultLookup(frictionless.Check):
    """Checks whether default value is provided for keyed value in other field."""

    # Check attributes
    type = "default-lookup"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Name of field used for lookup value, or a callable to get the lookup value.
    key_field: str | Callable[[frictionless.Row], object]
    # Name of field which default map value corresponds
    value_field: str
    # Default map consisting of keys from key_field and values for value_field
    default_map: Mapping[object, object]
    # error message templates,
    # used when key_field doesn't get a value from the row.
    no_key_error_template: str = _default_error_template
    # used when the default_map doesn't provide a value.
    no_default_error_template: str = _default_error_template

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

        # Get value to lookup default map with
        if isinstance(self.key_field, str):
            lookup_value = row[self.key_field]
        else:
            lookup_value = self.key_field(row)

        # No lookup value is an error
        if lookup_value is None:
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=self.no_key_error_template.format(
                    key_value=lookup_value,
                    key_field=self.key_field,
                    value_field=self.value_field,
                ),
            )
            return

        # Determine if default value entry exists
        if lookup_value in self.default_map:
            return

        # Yield Error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=self.no_default_error_template.format(
                key_value=lookup_value,
                key_field=self.key_field,
                value_field=self.value_field,
            ),
        )
