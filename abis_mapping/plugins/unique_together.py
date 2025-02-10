"""Provides extra frictionless unique together checks for the package"""

# Third-Party
import attrs
import frictionless
import frictionless.errors

# Local
from abis_mapping import utils

# Typing
from collections.abc import Iterator, Sequence, Collection
from typing import Literal


class UniqueTogetherError(frictionless.errors.RowError):
    type = "unique-together"
    title = "Unique Together Error"
    description = "Each row must have a unique combination of values in the unique together fields."
    template = 'Row at position "{rowNumber}" violates the unique together constraint: {note}'


@attrs.define(kw_only=True, repr=False)
class UniqueTogether(frictionless.Check):
    """Checks whether 2 or more columns are unique together within the dataset."""

    # Check Attributes
    type = "unique-together"
    Errors = [UniqueTogetherError]

    # Attributes to customize this check
    fields: Sequence[str]
    null_handling: Literal[
        "skip",  # Skip any row where any of the fields is None
        # This is like a regular multi-column unique constrain in SQL.
        "include",  # Include rows with None in the check, treating None as equal to itself.
        # This is like a multi-column unique constrain in SQL with the NULLS NOT DISTINCT option.
    ]
    error_message_template: str = (
        "The unique together fields [{fields}] contain the values [{values}] "
        'that have already been used in the row at position "{first_seen_row_number}"'
    )
    # Fields which should be slugified before checking their uniqueness.
    # Why would we want this?
    # Often after checking a field is unique, we slugify the value to use in an IRI,
    # which also needs to be unique.
    # This ensures that two rows' values that pass the unique check, can be slugified
    # and used in IRIs, and the IRIs are also guaranteed to be unique.
    slugified_fields: Collection[str] = ()

    # Private attribute to track the values seen so far, and at which row number
    _seen_values: dict[tuple[object, ...], int] = attrs.field(factory=dict, init=False)

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row: The row to check.

        Yields:
            Any errors found in the row.
        """
        # Get tuple of values for the fields
        values: tuple[object, ...] = tuple(row[key] for key in self.fields)

        # Check if the row should be skipped
        if None in values and self.null_handling == "skip":
            return

        values_to_check = tuple(self._get_check_value(key, row) for key in self.fields)

        if (first_seen_row_number := self._seen_values.get(values_to_check)) is not None:
            # If values already seen, return an error
            yield UniqueTogetherError.from_row(
                row=row,
                note=self.error_message_template.format(
                    fields=", ".join(self.fields),
                    values=", ".join(map(str, values)),
                    first_seen_row_number=first_seen_row_number,
                ),
            )
        else:
            # otherwise add them to the seen values to check following rows.
            self._seen_values[values_to_check] = row.row_number

    def _get_check_value(self, key: str, row: frictionless.Row) -> object:
        """Get the value for a key which is used in the unique check."""
        value: object = row[key]

        # Slugify value if required
        if key in self.slugified_fields and value is not None:
            if not isinstance(value, str):
                raise TypeError("value for slugified field {key} must be a string")
            value = utils.rdf.slugify_for_uri(value)

        return value
