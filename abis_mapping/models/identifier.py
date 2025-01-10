"""Provides models related to "identifiers" in the template data."""

# Standard library
import dataclasses

# Third-party
import frictionless

# Typing
from typing import Self


@dataclasses.dataclass(eq=True, frozen=True, kw_only=True)
class SiteIdentifier:
    """A class to represent how a Site is identified in a row from a template.

    This is effectively either the existingBDRSiteIRI field,
    or a combination of the siteID and siteIDSource fields.
    These are the two ways Sites can be identified in a template.
    """

    site_id: str | None
    site_id_source: str | None
    existing_bdr_site_iri: str | None

    @classmethod
    def from_row(cls, row: frictionless.Row) -> Self | None:
        """Given a row in a template, return a SiteIdentifier for the site-id related fields.

        Args:
            row: The row of data.

        Returns:
            The SiteIdentifier for the siteID-related fields.
            None when the siteID-related fields are not in the row.

        """
        # "existingBDRSiteIRI" is considered a higher "source of truth",
        # if a row has that, only use that as the identifier.
        # This means that two sets of identifier fields will compare equal if their
        # existingBDRSiteIRI matches, even if the others fields do not match.
        existing_bdr_site_iri: str | None = row["existingBDRSiteIRI"]
        if existing_bdr_site_iri:
            return cls(
                site_id=None,
                site_id_source=None,
                existing_bdr_site_iri=existing_bdr_site_iri,
            )

        # Otherwise try to use siteID and siteIDSource.
        site_id: str | None = row["siteID"]
        site_id_source: str | None = row["siteIDSource"]
        if site_id and site_id_source:
            return cls(
                site_id=site_id,
                site_id_source=site_id_source,
                existing_bdr_site_iri=None,
            )

        # Otherwise return None.
        return None
