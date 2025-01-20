"""Provides Unit Tests for the `abis_mapping.plugins.related_site_validation` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import models
from abis_mapping import plugins


def test_related_site_validation_with_valid_data() -> None:
    """Tests the RelatedSiteValidation Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # No related site fields
            {
                "rowID": "1",
                "relatedSiteID": None,
                "relatedSiteIDSource": None,
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": None,
            },
            # relatedSiteIRI and relationship
            {
                "rowID": "2",
                "relatedSiteID": None,
                "relatedSiteIDSource": None,
                "relatedSiteIRI": "https://example.com/site/1",
                "relationshipToRelatedSite": "SAME AS",
            },
            # site ID and relationship
            {
                "rowID": "3",
                "relatedSiteID": "S1",
                "relatedSiteIDSource": "TEST",
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": "PART OF",
            },
        ],
    )
    # Fake SiteIdentifiers from template
    site_identifiers = {
        models.identifier.SiteIdentifier(site_id="S1", site_id_source="TEST", existing_bdr_site_iri=None),
    }

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.related_site_validation.RelatedSiteValidation(
                    site_identifiers=site_identifiers,
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_related_site_validation_with_invalid_data() -> None:
    """Tests the RelatedSiteValidation Checker with invalid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # relatedSiteIRI but no relationship
            {
                "rowID": "4",
                "relatedSiteID": None,
                "relatedSiteIDSource": None,
                "relatedSiteIRI": "https://example.com/site/1",
                "relationshipToRelatedSite": None,
            },
            # site ID but no relationship
            {
                "rowID": "5",
                "relatedSiteID": "S1",
                "relatedSiteIDSource": "TEST",
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": None,
            },
            # relationship but no related site
            {
                "rowID": "6",
                "relatedSiteID": None,
                "relatedSiteIDSource": None,
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": "SAME AS",
            },
            # related site ID+Source does not appear in template
            {
                "rowID": "7",
                "relatedSiteID": "S2",
                "relatedSiteIDSource": "TEST",
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": "PART OF",
            },
            # related site ID+Source does not appear in template, AND not relationship
            {
                "rowID": "8",
                "relatedSiteID": "S3",
                "relatedSiteIDSource": "TEST",
                "relatedSiteIRI": None,
                "relationshipToRelatedSite": None,
            },
        ],
    )
    # Fake SiteIdentifiers from template
    site_identifiers = {
        models.identifier.SiteIdentifier(site_id="S1", site_id_source="TEST", existing_bdr_site_iri=None),
    }

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.related_site_validation.RelatedSiteValidation(
                    site_identifiers=site_identifiers,
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 6
    assert report.tasks[0].errors[0].message == (
        "The row at position 2 has an error: When relatedSiteIRI is provided, "
        "relationshipToRelatedSite must also be provided to specify the type of relationship."
    )
    assert report.tasks[0].errors[1].message == (
        "The row at position 3 has an error: When relatedSiteID and relatedSiteIDSource are provided, "
        "relationshipToRelatedSite must also be provided to specify the type of relationship."
    )
    assert report.tasks[0].errors[2].message == (
        "The row at position 4 has an error: When relationshipToRelatedSite is provided, "
        "either relatedSiteIRI, or relatedSiteID and relatedSiteIDSource must be "
        "provided to specify the related site."
    )
    assert report.tasks[0].errors[3].message == (
        "The row at position 5 has an error: relatedSiteID and relatedSiteIDSource "
        "must match the siteID and siteIDSource of a site in this template."
    )
    # last row has two errors:
    assert report.tasks[0].errors[4].message == (
        "The row at position 6 has an error: relatedSiteID and relatedSiteIDSource "
        "must match the siteID and siteIDSource of a site in this template."
    )
    assert report.tasks[0].errors[5].message == (
        "The row at position 6 has an error: When relatedSiteID and relatedSiteIDSource are provided, "
        "relationshipToRelatedSite must also be provided to specify the type of relationship."
    )
