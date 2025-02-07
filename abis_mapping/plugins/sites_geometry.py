"""Provides extra frictionless geometry sites' data template checks for the package."""

# Third-party
import frictionless
import frictionless.errors
import attrs

# Local
from abis_mapping import models

# Typing
from collections.abc import Collection
from typing import Iterator


@attrs.define(kw_only=True, repr=False)
class SitesGeometry(frictionless.Check):
    """Checks whether geometry related fields are provided in a correct combination."""

    # Check attributes
    type = "sites-geometry"
    Errors = [frictionless.errors.RowConstraintError]

    # Occurrences site ids to be passed in from occurrence template.
    occurrence_site_ids: Collection[str] | None = None
    occurrence_site_identifiers: Collection[models.identifier.SiteIdentifier] | None = None

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

        # Perform check
        if (lat and long and datum) or (wkt and datum):
            return

        # See if site was used by the occurrence template
        if self.occurrence_site_ids is not None:
            site_id = row["siteID"]
            site_used_by_occurrences = site_id and site_id in self.occurrence_site_ids
        elif self.occurrence_site_identifiers is not None:
            site_identifier = models.identifier.SiteIdentifier.from_row(row)
            site_used_by_occurrences = site_identifier and site_identifier in self.occurrence_site_identifiers
        else:
            site_used_by_occurrences = False

        # If geometry fields are invalid, but the Site is used by Occurrence(s), dont' error.
        # This is because if all the Occurrences using the Site, have their own valid location,
        # it doesn't matter the location here is missing.
        # On the other hand, if any of the Occurrences don't have their own valid location,
        # An error will be raised on them when they fail to fall back to this Site's location.
        # Also, when the Occurrence reference a Site by existingBDRSiteIRI,
        # then both the Occurrence and Site are allowed to have no geometry,
        # because the Site should already exist with geometry.
        if site_used_by_occurrences:
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
        yield frictionless.errors.RowConstraintError.from_row(row=row, note=note)
