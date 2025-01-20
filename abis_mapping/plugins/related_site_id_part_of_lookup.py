"""Module providing custom relatedSiteID lookup checks when value of relationshipToRelatedSite is partOf"""

# Third-party
import attrs
import frictionless
import frictionless.checks
import frictionless.errors

# Typing
from typing import Iterable


# TODO remove once SSD v2 is removed
@attrs.define(kw_only=True, repr=False)
class RelatedSiteIDPartOfLookup(frictionless.Check):
    """Specific check confirming relationshipToRelatedSite is a valid siteID when relationship is `partOf`.

    Attributes:
        site_ids: All siteIDs provided in the template.
    """

    Errors = [frictionless.errors.RowConstraintError]
    site_ids: set[str]

    def validate_row(self, row: frictionless.Row) -> Iterable[frictionless.Error]:
        """Validate row (every row).

        Args:
            row: Row of data to be validated.

        Yields:
            Errors encountered, if any
        """
        check = (
            row["relatedSiteID"] in self.site_ids
            if row["relatedSiteID"]
            and row["relationshipToRelatedSite"]
            and row["relationshipToRelatedSite"].lower().replace(" ", "") == "partof"
            else True
        )
        if not check:
            yield frictionless.errors.RowConstraintError.from_row(
                row,
                note=(
                    f"relatedSiteID '{row['relatedSiteID']}' needs to be provided as a siteID when "
                    f"relationshipToRelatedSite is '{row['relationshipToRelatedSite']}'"
                ),
            )
