"""Provides Unit Tests for the `abis_mapping.plugins.site_identifier_match` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import models
from abis_mapping import plugins


def test_site_identifier_match_with_valid_data() -> None:
    """Tests the SiteIdentifierMatches Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # No siteVisitID, check is skipped
            {"rowID": "1", "siteVisitID": None, "siteID": None, "siteIDSource": None, "existingBDRSiteIRI": None},
            # No SiteIdentifier, check is skipped
            {"rowID": "2", "siteVisitID": "V1", "siteID": None, "siteIDSource": None, "existingBDRSiteIRI": None},
            # siteVisitID is None in map, no error in this check/template.
            {"rowID": "3", "siteVisitID": "V2", "siteID": "S1", "siteIDSource": "TEST", "existingBDRSiteIRI": None},
            # valid data with matching SiteIdentifier
            {"rowID": "4", "siteVisitID": "V3", "siteID": "S1", "siteIDSource": "TEST", "existingBDRSiteIRI": None},
            {"rowID": "5", "siteVisitID": "V4", "siteID": None, "siteIDSource": None, "existingBDRSiteIRI": "TEST-IRI"},
            # siteID fields ignored when existingBDRSiteIRI is present.
            {"rowID": "6", "siteVisitID": "V4", "siteID": "AA", "siteIDSource": "BB", "existingBDRSiteIRI": "TEST-IRI"},
        ],
    )
    # Fake map from site visit data template.
    site_visit_id_site_id_map = {
        "V2": None,
        "V3": models.identifier.SiteIdentifier(site_id="S1", site_id_source="TEST", existing_bdr_site_iri=None),
        "V4": models.identifier.SiteIdentifier(site_id=None, site_id_source=None, existing_bdr_site_iri="TEST-IRI"),
    }

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_identifier_match.SiteIdentifierMatches(
                    site_visit_id_site_id_map=site_visit_id_site_id_map,
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_site_identifier_match_with_invalid_data() -> None:
    """Tests the SiteIdentifierMatches Checker with invalid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # siteVisitID not in map, that's an error
            {
                "rowID": "7",
                "siteVisitID": "UNKNOWN",
                "siteID": "S1",
                "siteIDSource": "TEST",
                "existingBDRSiteIRI": None,
            },
            # Not matching SiteIdentifiers, that's an error
            {"rowID": "8", "siteVisitID": "V5", "siteID": "S1", "siteIDSource": "TEST", "existingBDRSiteIRI": None},
            {
                "rowID": "9",
                "siteVisitID": "V6",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": "TEST-IRI-2",
            },
        ],
    )
    # Fake map from site visit data template.
    site_visit_id_site_id_map = {
        "V5": models.identifier.SiteIdentifier(site_id="S2", site_id_source="TEST", existing_bdr_site_iri=None),
        "V6": models.identifier.SiteIdentifier(site_id=None, site_id_source=None, existing_bdr_site_iri="TEST-IRI"),
    }

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.site_identifier_match.SiteIdentifierMatches(
                    site_visit_id_site_id_map=site_visit_id_site_id_map,
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 3
    assert report.tasks[0].errors[0].message == (
        'The cell "UNKNOWN" in row at position "2" and field "siteVisitID" '
        'at position "2" does not conform to a constraint: '
        "siteVisitID must match a siteVisitID in the survey_site_visit_data template"
    )
    assert report.tasks[0].errors[1].message == (
        "The row at position 3 has an error: siteID and siteIDSource must match their "
        'values in the survey_site_visit_data template at the row with siteVisitID "V5".'
    )
    assert report.tasks[0].errors[2].message == (
        "The row at position 4 has an error: existingBDRSiteIRI must match their "
        'values in the survey_site_visit_data template at the row with siteVisitID "V6".'
    )
