"""Provides extra frictionless coordinate validation checks for the package"""


# Third-Party
import frictionless
import frictionless.errors
import attrs

# Local
from abis_mapping.utils import coords

# Typing
from typing import Any, Iterator


@attrs.define(kw_only=True, repr=False)
class ValidCoordinates(frictionless.Check):
    """Checks whether the latitude and longitude of the row are valid."""

    # Check Attributes
    type = "valid-coordinates"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    latitude_name: str
    longitude_name: str

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the coordinates of.

        Yields:
            frictionless.Error: For when the coordinates are deemed invalid.
        """
        # Get Latitude and Longitude
        latitude = row[self.latitude_name]
        longitude = row[self.longitude_name]

        # Check Existence
        if latitude is None or longitude is None:
            # Short-circuit
            return

        # Validate Coordinates
        coords_valid = coords.validate_coordinates(
            latitude=latitude,
            longitude=longitude,
        )

        # Check Validity
        if not coords_valid:
            # Yield Error
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note="the specified coordinates are not within the allowed boundaries",
            )
