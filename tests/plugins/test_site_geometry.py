"""Provides unit tests for the abis_mapping.plugins.site_geometry module."""

# Third-party
import frictionless
import pytest
import attrs

# Local
from abis_mapping import models
from abis_mapping import plugins

# Typing
from typing import Any, Iterator


@attrs.define(kw_only=True)
class Parameters:
    """Parameters for the test cases"""

    header: list[str]
    cases: list[tuple[str, str, str, str, set[str], bool]]

    def compiled(self) -> Iterator[tuple[dict[str, str], set[str], bool]]:
        """Compiles all the parameters for the test cases.

        Yields:
            tuple: The parameters for each test case.
        """
        # Iterate through each of the cases.
        for case in self.cases:
            *values, site_ids, valid = case
            # Construct data row
            source = dict(zip(self.header, values, strict=True))
            # Add siteID column
            source["siteID"] = "site1"
            # Yield result
            yield source, site_ids, valid


class TestSiteGeometry:
    """Test the site_geometry check"""

    params = Parameters(
        header=["decimalLatitude", "decimalLongitude", "footprintWKT", "geodeticDatum"],
        cases=[
            ("", "", "", "", set(), False),
            ("", "", "", "", {"site1"}, True),
            ("", "", "", "WGS84", set(), False),
            ("", "", "", "WGS84", {"site1"}, True),
            ("", "", "POINT (0 0)", "", set(), False),
            ("", "", "POINT (0 0)", "", {"site1"}, True),
            ("", "", "POINT (0 0)", "WGS84", set(), True),
            ("", "", "POINT (0 0)", "WGS84", {"site1"}, True),
            ("", "0", "", "", set(), False),
            ("", "0", "", "", {"site1"}, True),
            ("", "0", "", "WGS84", set(), False),
            ("", "0", "", "WGS84", {"site1"}, True),
            ("", "0", "POINT(0 0)", "", set(), False),
            ("", "0", "POINT(0 0)", "", {"site1"}, True),
            ("", "0", "POINT(0 0)", "WGS84", set(), True),
            ("", "0", "POINT(0 0)", "WGS84", {"site1"}, True),
            ("0", "", "", "", set(), False),
            ("0", "", "", "", {"site1"}, True),
            ("0", "", "", "WGS84", set(), False),
            ("0", "", "", "WGS84", {"site1"}, True),
            ("0", "", "POINT (0 0)", "", set(), False),
            ("0", "", "POINT (0 0)", "", {"site1"}, True),
            ("0", "", "POINT (0 0)", "WGS84", set(), True),
            ("0", "", "POINT (0 0)", "WGS84", {"site1"}, True),
            ("0", "0", "", "", set(), False),
            ("0", "0", "", "", {"site1"}, True),
            ("0", "0", "", "WGS84", set(), True),
            ("0", "0", "", "WGS84", {"site1"}, True),
            ("0", "0", "POINT(0 0)", "", set(), False),
            ("0", "0", "POINT(0 0)", "", {"site1"}, True),
            ("0", "0", "POINT(0 0)", "WGS84", set(), True),
            ("0", "0", "POINT(0 0)", "WGS84", {"site1"}, True),
        ],
    )

    @pytest.mark.parametrize("source,site_ids,valid", params.compiled())
    def test_check_site_geometry_valid(self, source: dict[str, Any], site_ids: set[str], valid: bool) -> None:
        """Tests the site goemetry checker.

        Args:
            source (dict[str, Any]): Source for creating resource.
            site_ids (set[str]): Site ids sent from occurrence template.
            valid (bool): Whether the case is valid.
        """
        # Construct schema
        descriptor = {
            "fields": [
                {
                    "name": "decimalLatitude",
                    "type": "number",
                },
                {
                    "name": "decimalLongitude",
                    "type": "number",
                },
                {
                    "name": "footprintWKT",
                    "type": "string",
                },
                {
                    "name": "geodeticDatum",
                    "type": "string",
                },
                {
                    "name": "siteID",
                    "type": "string",
                },
            ],
        }
        schema = frictionless.Schema.from_descriptor(descriptor)

        # Construct fake resource
        resource = frictionless.Resource(
            source=[source],
            schema=schema,
        )

        # Validate
        report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[plugins.sites_geometry.SitesGeometry(occurrence_site_ids=site_ids)]
            )
        )

        # Assert
        assert report.valid == valid


def test_site_geometry_with_site_identifiers() -> None:
    """Tests the site geometry checker with site identifiers."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # valid with location
            {
                "decimalLatitude": "40",
                "decimalLongitude": "40",
                "footprintWKT": None,
                "geodeticDatum": "GDA2020",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
            {
                "decimalLatitude": None,
                "decimalLongitude": None,
                "footprintWKT": "POINT (20, 20)",
                "geodeticDatum": "GDA2020",
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
            # valid with a site in occurrence file
            {
                "decimalLatitude": None,
                "decimalLongitude": None,
                "footprintWKT": None,
                "geodeticDatum": None,
                "siteID": "S1",
                "siteIDSource": "ORG",
                "existingBDRSiteIRI": None,
            },
            {
                "decimalLatitude": None,
                "decimalLongitude": None,
                "footprintWKT": None,
                "geodeticDatum": None,
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": "SITE-IRI",
            },
        ],
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.sites_geometry.SitesGeometry(
                    occurrence_site_identifiers={
                        models.identifier.SiteIdentifier(
                            site_id="S1", site_id_source="ORG", existing_bdr_site_iri=None
                        ),
                        models.identifier.SiteIdentifier(
                            site_id=None, site_id_source=None, existing_bdr_site_iri="SITE-IRI"
                        ),
                    }
                )
            ]
        )
    )

    # Assert
    assert report.valid


def test_site_geometry_with_site_identifiers_invalid_data() -> None:
    """Tests the site geometry checker with site identifiers and invalid data."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # invalid, no complete location or site
            {
                "decimalLatitude": "30",
                "decimalLongitude": None,
                "footprintWKT": None,
                "geodeticDatum": None,
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": None,
            },
            # invalid, no location and site not in occurrence file
            {
                "decimalLatitude": None,
                "decimalLongitude": None,
                "footprintWKT": None,
                "geodeticDatum": None,
                "siteID": "S2",
                "siteIDSource": "ORG",
                "existingBDRSiteIRI": None,
            },
            {
                "decimalLatitude": None,
                "decimalLongitude": None,
                "footprintWKT": None,
                "geodeticDatum": None,
                "siteID": None,
                "siteIDSource": None,
                "existingBDRSiteIRI": "SITE-IRI-2",
            },
        ],
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.sites_geometry.SitesGeometry(
                    occurrence_site_identifiers={
                        models.identifier.SiteIdentifier(
                            site_id="S1", site_id_source="ORG", existing_bdr_site_iri=None
                        ),
                        models.identifier.SiteIdentifier(
                            site_id=None, site_id_source=None, existing_bdr_site_iri="SITE-IRI"
                        ),
                    }
                )
            ]
        )
    )

    # Assert
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 3
    assert [error.type for error in report.tasks[0].errors] == ["row-constraint", "row-constraint", "row-constraint"]
