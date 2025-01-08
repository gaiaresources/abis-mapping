"""Provides extra frictionless check"""

# Third-Party
import attrs
import frictionless
import frictionless.errors

# Typing
from collections.abc import Iterator


@attrs.define(kw_only=True, repr=False)
class SiteIdentifierCheck(frictionless.Check):
    """Checks if the row has either (siteID + siteIDSource) or existingBDRSiteIRI"""

    # Check Attributes
    type = "site-identifier"
    Errors = [frictionless.errors.RowConstraintError]

    # optionally only apply this check when this field has a value
    skip_when_missing: str | None = None

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row: The row to check.

        Yields:
            Any errors found in the row.
        """
        if self.skip_when_missing is not None and row[self.skip_when_missing] is None:
            return

        # Get values
        site_id: str | None = row["siteID"]
        site_id_source: str | None = row["siteIDSource"]
        existing_bdr_site_iri: str | None = row["existingBDRSiteIRI"]

        if not ((site_id and site_id_source) or existing_bdr_site_iri):
            note = "Either siteID and siteIDSource, or existingBDRSiteIRI must be provided"
            if self.skip_when_missing is not None:
                note += f", when {self.skip_when_missing} is provided"
            note += "."
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=note,
            )
