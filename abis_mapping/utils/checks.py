"""Provides extra frictionless checks for the package"""


# Third-Party
import frictionless

# Local
from . import coords

# Typing
from typing import Any, Iterator


class ValidCoordinates(frictionless.Check):
    """Checks whether the latitude and longitude of the row are valid."""

    # Check Attributes
    code = "valid-coordinates"
    Errors = [frictionless.errors.RowConstraintError]

    def __init__(
        self,
        descriptor: Any=None,
        *,
        latitude_name: str,
        longitude_name: str,
        ) -> None:
        """Instantiate the ValidCoordinates Checker"""
        # Initialise Super Class
        super().__init__(descriptor)

        # Instance Attributes
        self.__latitude_name = latitude_name
        self.__longitude_name = longitude_name

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the coordinates of.

        Yields:
            frictionless.Error: For when the coordinates are deemed invalid.
        """
        # Get Latitude and Longitude
        latitude = row[self.__latitude_name]
        longitude = row[self.__longitude_name]

        # Check Existence
        if latitude is None or longitude is None:
            # Short-circuit
            return None

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


class NotEmpty(frictionless.Check):
    """Checks whether the resource has at least 1 row."""

    # Check Attributes
    code = "not-empty"
    Errors = [frictionless.errors.TableDimensionsError]

    def validate_end(self) -> Iterator[frictionless.Error]:
        """Called to validate the resource before closing.

        Yields:
            frictionless.Error: If the table is empty.
        """
        # Check Number of Rows
        if not self.resource.stats.get("rows"):
            # Yield Error
            yield frictionless.errors.TableDimensionsError(
                note=f"Current number of rows is 0, the minimum is 1",
                limits={"minRows": 1, "numberRows": 0},
            )


class NotTabular(frictionless.Check):
    """Checks whether the resource is at least tabular data in nature."""

    # Check Attributes
    code = "not-tabular"
    Errors = [frictionless.errors.SourceError]

    def validate_start(self) -> Iterator[frictionless.Error]:
        """Called to validate the resource after opening

        Yields:
            frictionless.Error: If the resource is not tabular data.
        """
        # Check if tabular
        if not self.resource.tabular:
            # Yield Error
            yield frictionless.errors.SourceError(
                note="the source is not tabular data",
            )
