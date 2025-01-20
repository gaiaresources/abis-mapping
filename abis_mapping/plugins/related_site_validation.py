"""Module providing custom validation for the related Site fields"""

# Third-party
import attrs
import frictionless
import frictionless.checks
import frictionless.errors

# Local
from abis_mapping import models

# Typing
from collections.abc import Collection, Iterable


@attrs.define(kw_only=True, repr=False)
class RelatedSiteValidation(frictionless.Check):
    """Validation relating to the "related site" fields.

    Checks:
    1. relationshipToRelatedSite and the "related site" are specified together.
        The "related site" can be specified either by the relatedSiteIRI field,
        or by the combination of the relatedSiteID and relatedSiteIDSource field.
    2. When the "related site" is specified by relatedSiteID and relatedSiteIDSource,
        check that those fields match a siteID and siteIDSource in this template.

    Attributes:
        site_identifiers: All SiteIdentifiers provided in the template.
    """

    Errors = [frictionless.errors.RowConstraintError]

    # SiteIdentifiers from the template being validated.
    site_identifiers: Collection[models.identifier.SiteIdentifier]

    def validate_row(self, row: frictionless.Row) -> Iterable[frictionless.Error]:
        """Validate a row.

        Args:
            row: Row of data to be validated.

        Yields:
            Errors encountered, if any
        """
        related_site_id: str | None = row["relatedSiteID"]
        related_site_id_source: str | None = row["relatedSiteIDSource"]
        related_site_iri: str | None = row["relatedSiteIRI"]
        relationship_to_related_site: str | None = row["relationshipToRelatedSite"]

        if related_site_iri:
            # If relatedSiteIRI is provided, ignore relatedSiteID(Source) fields,
            # just check relationshipToRelatedSite is provided.
            if not relationship_to_related_site:
                yield frictionless.errors.RowConstraintError.from_row(
                    row=row,
                    note=(
                        "When relatedSiteIRI is provided, relationshipToRelatedSite "
                        "must also be provided to specify the type of relationship."
                    ),
                )
            # Don't check the relatedSiteIRI matches a existingBDRSiteIRI, because it
            # could refer to an 'external' site not listed in this template.

        elif related_site_id and related_site_id_source:
            # Else, relatedSiteID(Source) fields are provided, check they match a site
            # in the template.
            related_site_identifier = models.identifier.SiteIdentifier(
                site_id=related_site_id,
                site_id_source=related_site_id_source,
                existing_bdr_site_iri=None,
            )
            if related_site_identifier not in self.site_identifiers:
                yield frictionless.errors.RowConstraintError.from_row(
                    row=row,
                    note=(
                        "relatedSiteID and relatedSiteIDSource must match the siteID "
                        "and siteIDSource of a site in this template."
                    ),
                )
            # Also check the relationship is specified.
            if not relationship_to_related_site:
                yield frictionless.errors.RowConstraintError.from_row(
                    row=row,
                    note=(
                        "When relatedSiteID and relatedSiteIDSource are provided, "
                        "relationshipToRelatedSite must also be provided to specify the type of relationship."
                    ),
                )

        elif relationship_to_related_site:
            # Else, related site is not specified, but relationshipToRelatedSite is,
            # that's an error.
            yield frictionless.errors.RowConstraintError.from_row(
                row=row,
                note=(
                    "When relationshipToRelatedSite is provided, either relatedSiteIRI, "
                    "or relatedSiteID and relatedSiteIDSource must be provided to "
                    "specify the related site."
                ),
            )

        # Else, no fields provided, all valid.
