"""Provides frictionless check for validating the geometry on an Occurrence."""

# Standard Library
import decimal

# Third-party
import attrs
import frictionless
import frictionless.errors

# Local
from abis_mapping import models

# Typing
from collections.abc import Iterator, Mapping


@attrs.define(kw_only=True, repr=False)
class GeometryValidation(frictionless.Check):
    """Validate an Occurrence has geometry, or a fallback in the geometry map."""

    # Check attributes
    type = "geometry-validation"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    # Default map from a Site Identifier to the geometry for that site
    site_id_geometry_map: Mapping[models.identifier.SiteIdentifier, str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate given row (on every row)

        Args:
            row (frictionless.Row): The row to check defaults for

        Yields::
           frictionless.Error: When the default lookup fails
        """
        # Determine if regular geometry fields have a value
        latitude: decimal.Decimal | None = row["decimalLatitude"]
        longitude: decimal.Decimal | None = row["decimalLongitude"]
        geodetic_datum: str | None = row["geodeticDatum"]
        # All geometry fields have a value, all good.
        if latitude is not None and longitude is not None and geodetic_datum is not None:
            return
        # Partially complete geometry fields are checked by a separate MutuallyInclusive check.

        # Otherwise no geometry, check if there is a Site with geometry.

        site_identifier = models.identifier.SiteIdentifier.from_row(row)

        # If no Site identifier (and not all geometry fields), that's an error
        if site_identifier is None:
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=(
                    "decimalLatitude, decimalLongitude and geodeticDatum must be provided, "
                    "or siteID and siteIDSource, or existingBDRSiteIRI, must be provided to use the geometry of a Site."
                ),
            )
            return

        # Determine if default geometry exists for site, if so, all good
        if site_identifier in self.site_id_geometry_map:
            return

        # Otherwise that's an error
        yield frictionless.errors.RowConstraintError.from_row(
            row=row,
            note=f"Could not find a Site with {site_identifier} and geometry to use for Occurrence geometry.",
        )
        return
