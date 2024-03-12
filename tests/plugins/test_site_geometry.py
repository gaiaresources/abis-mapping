"""Provides unit tests for the abis_mapping.plugins.site_geometry module."""


# Third-party
import frictionless
import pytest
import attrs

# Local
from abis_mapping import plugins

# Typing
from typing import Any, Iterator


@attrs.define(kw_only=True)
class Parameters:
    """Parameters for the test cases"""
    header: list[str]
    cases: list[tuple]

    def compiled(self) -> Iterator[tuple]:
        """Compiles all the parameters for the test cases.

        Yields:
            tuple: The parameters for each test case.
        """
        # Iterate through each of the cases.
        for case in self.cases:
            # Construct data row
            source = {key: val for key, val in zip(self.header, case)}
            # Add siteID column
            source["siteID"] = "site1"
            # Yield result
            yield source, case[-2], case[-1]


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

    @pytest.mark.parametrize(
        "source,site_ids,valid",
        params.compiled()
    )
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
