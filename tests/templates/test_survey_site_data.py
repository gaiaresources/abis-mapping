"""Tests for the survey_site_data template not common to other templates."""

# Standard
import csv
import io

# Third-party
import attrs
import frictionless
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import base
import abis_mapping.templates.survey_site_data.mapping

# Typing
from typing import Any


def test_extract_geometry_defaults(mocker: pytest_mock.MockerFixture) -> None:
    """Test the extract_geometry_defaults method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Construct a dummy raw data set using only the fields that matter to the method.
    rawh = ["siteID", "footprintWKT", "decimalLongitude", "decimalLatitude", "geodeticDatum"]
    raws = [
        ["site1", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "", "", "WGS84"],
        ["site2", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "10.0", "20.0", "WGS84"],
        ["site3", "", "10.0", "20.0", "WGS84"],
        ["site4", "", "", "", ""],
        ["site5", "", "10.0", "20.0", ""],
        ["site6", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "", "", ""],
        ["site7", "", "10.0", "20.0", "AGD66"],
        ["site8", "", "11.0", "21.0", "EPSG:4202"],
        ["site9", "", "12.0", "22.0", "GRS20"],
    ]
    # Amalgamate into a list of dicts
    all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in raws]

    # Get the specific mapper
    mapper = abis_mapping.templates.survey_site_data.mapping.SurveySiteMapper()

    # Modify schema to only include the necessary fields for test
    descriptor = {
        "fields": [
            {"name": "siteID", "type": "string"},
            {"name": "footprintWKT", "type": "wkt"},
            {"name": "decimalLongitude", "type": "number"},
            {"name": "decimalLatitude", "type": "number"},
            {"name": "geodeticDatum", "type": "string"},
        ]
    }
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Create raw data csv string
    with io.StringIO() as output:
        csv_writer = csv.DictWriter(output, fieldnames=rawh)
        csv_writer.writeheader()

        for row in all_raw:
            csv_writer.writerow(row)

        csv_data = output.getvalue().encode("utf-8")

    expected = {
        "site1": "<http://www.opengis.net/def/crs/EPSG/0/4326> POINT (2.5 2.5)",
        "site2": "<http://www.opengis.net/def/crs/EPSG/0/4326> POINT (2.5 2.5)",
        "site3": "<http://www.opengis.net/def/crs/EPSG/0/4326> POINT (10 20)",
        "site7": "<http://www.opengis.net/def/crs/EPSG/0/4202> POINT (10 20)",
        "site8": "<http://www.opengis.net/def/crs/EPSG/0/4202> POINT (11 21)",
    }
    # Invoke method
    actual = mapper.extract_geometry_defaults(csv_data)

    # Validate
    assert actual == expected


class TestSiteIDForeignKeys:
    @attrs.define(kw_only=True)
    class Scenario:
        """Dataclass to hold the scenario parameters."""

        name: str
        raws: list[list[str]]
        site_id_map: dict[str, bool]
        expected_error_codes: set[str] = set()

    scenarios: list[Scenario] = [
        Scenario(
            name="valid_with_site_id_map",
            raws=[
                ["site1", "-38.94", "115.21", "POINT(30 10)", "WGS84"],
                ["site2", "-38.94", "115.21", "", "GDA2020"],
                ["site3", "", "", "LINESTRING(30 10, 10 30, 40 40)", "GDA94"],
                ["site4", "", "", "", ""],
                # Following shows that non-url safe siteIDs get endcoded when mapping.
                ["site a", "-38.94", "115.21", "", "GDA2020"],
                ["site/b", "-38.94", "115.21", "", "GDA2020"],
                [r"site\c", "-38.94", "115.21", "", "GDA2020"],
                ["site\nd", "-38.94", "115.21", "", "GDA2020"],
            ],
            site_id_map={
                "site4": True,
                "siteNone": True,
            },
        ),
        Scenario(
            name="invalid_missing_geometry_and_not_in_map",
            raws=[
                ["site1", "", "", "", ""],
            ],
            site_id_map={"site2": True},
            expected_error_codes={"row-constraint"},
        ),
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=[scenario for scenario in scenarios],
        ids=[scenario.name for scenario in scenarios],
    )
    def test_apply_validation(self, scenario: Scenario, mocker: pytest_mock.MockerFixture) -> None:
        """Tests the apply_validation method with siteID foreign key dictionary provided.

        Args:
            scenario (Scenario): The parameters of the scenario under test.
            mocker (pytest_mock.MockerFixture): The mocker fixture.
        """
        # Construct fake data
        rawh = ["siteID", "decimalLatitude", "decimalLongitude", "footprintWKT", "geodeticDatum"]
        all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in scenario.raws]

        # Get mapper
        mapper = abis_mapping.templates.survey_site_data.mapping.SurveySiteMapper()

        # Modify schema to only fields required for test
        descriptor = {"fields": [field for field in mapper.schema()["fields"] if field["name"] in rawh]}
        descriptor["fields"].sort(key=lambda f: rawh.index(f["name"]))

        # Patch the schema for the test
        mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

        # Create raw data csv string
        with io.StringIO() as output:
            csv_writer = csv.DictWriter(output, fieldnames=rawh)
            csv_writer.writeheader()

            for row in all_raw:
                csv_writer.writerow(row)

            csv_data = output.getvalue().encode("utf-8")

        # Apply validation
        report = mapper.apply_validation(
            data=csv_data,
            site_id_map=scenario.site_id_map,
        )

        # Assert
        assert report.valid == (scenario.expected_error_codes == set())
        if not report.valid:
            error_codes = [code for codes in report.flatten(["type"]) for code in codes]
            assert set(error_codes) == scenario.expected_error_codes


@pytest.mark.parametrize(
    "row_dict",
    [
        {"footprintWKT": None, "geodeticDatum": None},
        {"footprintWKT": None, "geodeticDatum": "WGS84"},
        {"footprintWKT": "POINT (0 0)", "geodeticDatum": None},
    ],
)
def test_add_footprint_geometry_no_geometry(row_dict: dict[str, Any]) -> None:
    """Tests that add_footprint_geometry won't add to graph without valid WKT geometry.

    Args:
        row_dict (dict[str, Any]): Raw data row to use for test case.
    """
    # Create graph
    graph = rdflib.Graph()

    # Create resource
    resource = frictionless.Resource(source=[row_dict])

    # Extract row
    with resource.open() as r:
        row = next(r.row_stream)

    # Create URI
    uri = rdflib.URIRef("http://example.com/abis-mapping/test")

    # Get mapper
    mapper = abis_mapping.templates.survey_site_data.mapping.SurveySiteMapper()

    # Call method
    mapper.add_footprint_geometry(
        uri=uri,
        row=row,
        graph=graph,
    )

    # Validate no triples added to graph
    assert len(graph) == 0


@pytest.mark.parametrize(
    "row_dict",
    [
        {"decimalLatitude": None, "decimalLongitude": None, "geodeticDatum": None},
        {"decimalLatitude": None, "decimalLongitude": None, "geodeticDatum": "WGS84"},
        {"decimalLatitude": None, "decimalLongitude": 0, "geodeticDatum": None},
        {"decimalLatitude": None, "decimalLongitude": 0, "geodeticDatum": "WGS84"},
        {"decimalLatitude": 0, "decimalLongitude": None, "geodeticDatum": None},
        {"decimalLatitude": 0, "decimalLongitude": None, "geodeticDatum": "WGS84"},
        {"decimalLatitude": 0, "decimalLongitude": 0, "geodeticDatum": None},
    ],
)
def test_add_point_geometry_no_geometry(row_dict: dict[str, Any]) -> None:
    """Tests that add_point_geometry method doesn't add to graph for no point geometries.

    Args:
        row_dict (dict[str, Any]): Raw data row to use for test case.
    """
    # Create graph
    graph = rdflib.Graph()

    # Create resource
    resource = frictionless.Resource(source=[row_dict])

    # Extract row
    with resource.open() as r:
        row = next(r.row_stream)

    # Create URI
    uri = rdflib.URIRef("http://example.com/abis-mapping/test")

    # Get mapper
    mapper = abis_mapping.templates.survey_site_data.mapping.SurveySiteMapper()

    # Call method
    mapper.add_point_geometry(
        uri=uri,
        row=row,
        graph=graph,
    )

    # Validate no triples added to graph
    assert len(graph) == 0
