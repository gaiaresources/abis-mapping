"""Provides extra frictionless check"""

# Third-Party
import attrs
import frictionless
import frictionless.errors

# Local
from abis_mapping import models

# Typing
from collections.abc import Iterator, Mapping


@attrs.define(kw_only=True, repr=False)
class SiteIdentifierMatches(frictionless.Check):
    """Checks if the row's siteVisitID+SiteIdentifier matches another template.

    This is used by the survey_occurrence_data template to check that each occurrence
    with a siteVisitID, has a SiteIdentifier that matches the SiteIdentifier for that
    siteVisitID in the survey_site_data_visit template.

    i.e. The 'source of truth' FKs linking an Occurrence to a Site (when there is a Visit) are;

    occurrence.siteVisitID --> site_visit.siteVisitID && site_visit.SiteIdentifier --> site.SiteIdentifier

    There is also a 'short-cut' FK directly from Occurrence to Site;

    occurrence.SiteIdentifier --> site.SiteIdentifier

    This Check ensures the 'short-cut' FK agrees with the 'source of truth' ones.
    """

    # Check Attributes
    type = "site-identifier-matches"
    Errors = [frictionless.errors.RowConstraintError, frictionless.errors.ConstraintError]

    # Map from siteVisitID to SiteIdentifier, from the other template (typically survey_site_visit_data).
    site_visit_id_site_id_map: Mapping[str, models.identifier.SiteIdentifier | None]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row: The row to check.

        Yields:
            Any errors found in the row.
        """
        # If this template has no siteVisitID, skip the check.
        site_visit_id: str | None = row["siteVisitID"]
        if not site_visit_id:
            return
        # If siteVisitID should be compulsory, enforce that with a required constraint or similar.

        # If this template has no identifier, skip the check
        identifier = models.identifier.SiteIdentifier.from_row(row)
        if not identifier:
            return
        # If the identifier must be provided, enforce that with the SiteIdentifierCheck plugin.

        # if siteVisitID not in the map, means it wasn't in the site visit data template,
        # that's an error in this template.
        if site_visit_id not in self.site_visit_id_site_id_map:
            yield frictionless.errors.ConstraintError.from_row(
                row=row,
                note="siteVisitID must match a siteVisitID in the survey_site_visit_data template",
                field_name="siteVisitID",
            )
            return

        expected_site_identifier = self.site_visit_id_site_id_map[site_visit_id]
        if not expected_site_identifier:
            # The site_visit_data template is missing the site identifier,
            # that will be an error in that template, no need to raise an error here.
            return

        # both templates have SiteIdentifiers, check if they don't match.
        if expected_site_identifier != identifier:
            if expected_site_identifier.existing_bdr_site_iri:
                fields = "existingBDRSiteIRI"
            else:
                fields = "siteID and siteIDSource"
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=(
                    f'{fields} must match their values in the survey_site_visit_data template at the row with siteVisitID "{site_visit_id}".'
                ),
            )
            return

        # Otherwise identifiers match, no error to raise.
