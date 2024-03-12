"""Provides extra frictionless geometry sites' data template checks for the package."""


# Third-party
import frictionless
import frictionless.errors
import attrs

# Typing
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class SitesGeometry(frictionless.Check):
    """Checks whether geometry related fields are provided in a correct combination."""

    # Check attributes
    type = "sites-geometry"
    Errors = [frictionless.errors.RowConstraintError]

    # Occurrences site ids to be passed in from occurrence template.
    occurrence_site_ids: set[str] = set()

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check the site's geometry for

        Yields:
            frictionless.Error: For when the check condition is violated.
        """
        # Extract values as bool
        lat = row["decimalLatitude"] is not None
        long = row["decimalLongitude"] is not None
        datum = row["geodeticDatum"] is not None
        wkt = row["footprintWKT"] is not None
        site_id = row["siteID"] in self.occurrence_site_ids

        # Perform check
        if (
            (lat and long and datum) or
            (wkt and datum) or
            site_id
        ):
            return

        # Create error note
        note = "invalid geometry: "
        if (wkt or (lat and long)) and not datum:
            note += f"invalid datum {row['geodeticDatum']} provided."
        elif lat ^ long:
            note += (
                f"latitude and longitude must be provided together, "
                f"got ({row['decimalLatitude']}, {row['decimalLongitude']})"
            )
        else:
            note += "incorrect combination of geometry fields provided."

        # Yield error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=note
        )
