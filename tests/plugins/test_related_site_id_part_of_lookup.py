"""Provides Unit Tests for the `abis_mapping.plugins.related_site_id_part_of_lookup` module"""

# Third-party
import frictionless

# Local
from abis_mapping import plugins


def test_related_site_id_part_of_lookup() -> None:
    """Tests that the related site id part of lookup check plugin."""
    # Define source data
    source = [
        # Valid
        {"siteID": "A", "relatedSiteID": "AA", "relationshipToRelatedSite": "partOf"},
        {"siteID": "AA", "relatedSiteID": "X", "relationshipToRelatedSite": "sameAs"},
        {"siteID": "AAA", "relatedSiteID": "A", "relationshipToRelatedSite": "part of"},
        # Invalid
        {"siteID": "AAAA", "relatedSiteID": "Y", "relationshipToRelatedSite": "partOf"},
        {"siteID": "AAAAA", "relatedSiteID": "Z", "relationshipToRelatedSite": "part OF"},
    ]
    # Construct fake resource
    resource = frictionless.Resource(source=source)
    sites = {x["siteID"] for x in source}

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[plugins.related_site_id_part_of_lookup.RelatedSiteIDPartOfLookup(site_ids=sites)]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 2
