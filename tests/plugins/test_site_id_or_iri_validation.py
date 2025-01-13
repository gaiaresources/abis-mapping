"""Provides Unit Tests for the `abis_mapping.plugins.site_id_or_iri_validation` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_with_valid_data() -> None:
    """Tests the SiteIdentifierCheck Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {
                "rowID": "1",
                "siteID": "P1",
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": None,
            },
            {
                "rowID": "2",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": "https://linked.data.gov.au/dataset/bdr/site/TERN/P2",
            },
            {
                "rowID": "3",
                "siteID": "P3",
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": "https://linked.data.gov.au/dataset/bdr/site/TERN/P3",
            },
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_id_or_iri_validation.SiteIdentifierCheck(),
            ],
        ),
    )

    # Check
    assert report.valid


def test_with_invalid_data() -> None:
    """Tests the SiteIdentifierCheck Checker with invalid data"""
    resource = frictionless.Resource(
        source=[
            {
                "rowID": "1",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
            {
                "rowID": "2",
                "siteID": "P1",
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
            {
                "rowID": "3",
                "siteID": None,
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": None,
            },
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_id_or_iri_validation.SiteIdentifierCheck(),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 3
    assert report.tasks[0].errors[0].message == (
        "The row at position 2 has an error: Either siteID and siteIDSource, or existingBDRSiteIRI must be provided."
    )
    assert report.tasks[0].errors[1].message == (
        "The row at position 3 has an error: Either siteID and siteIDSource, or existingBDRSiteIRI must be provided."
    )
    assert report.tasks[0].errors[2].message == (
        "The row at position 4 has an error: Either siteID and siteIDSource, or existingBDRSiteIRI must be provided."
    )


def test_with_valid_data_with_skip_field() -> None:
    """Tests the SiteIdentifierCheck Checker with valid data and a skip_when_missing field."""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {
                "rowID": "1",
                "some_field": "...",
                "siteID": "P1",
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": None,
            },
            {
                "rowID": "2",
                "some_field": "...",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": "https://linked.data.gov.au/dataset/bdr/site/TERN/P2",
            },
            {
                "rowID": "3",
                "some_field": "...",
                "siteID": "P3",
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": "https://linked.data.gov.au/dataset/bdr/site/TERN/P3",
            },
            # valid, but is not checked anyway because some_field is null
            {
                "rowID": "4",
                "some_field": None,
                "siteID": "P3",
                "siteIDSource": "TERN",
                "existingBDRSiteIRI": "https://linked.data.gov.au/dataset/bdr/site/TERN/P3",
            },
            # invalid, but not checked because some_field is null
            {
                "rowID": "5",
                "some_field": None,
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_id_or_iri_validation.SiteIdentifierCheck(
                    skip_when_missing="some_field",
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_with_invalid_data_with_skip_field() -> None:
    """Tests the SiteIdentifierCheck Checker with invalid data and a skip_when_missing field"""
    resource = frictionless.Resource(
        source=[
            # invalid, and is checked because some_field has a value
            {
                "rowID": "1",
                "some_field": "...",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_id_or_iri_validation.SiteIdentifierCheck(
                    skip_when_missing="some_field",
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 1
    assert report.tasks[0].errors[0].message == (
        "The row at position 2 has an error: Either siteID and siteIDSource, "
        "or existingBDRSiteIRI must be provided, when some_field is provided."
    )
