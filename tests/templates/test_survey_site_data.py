"""Tests for the survey_site_data template not common to other templates."""

# Standard
import csv
import io

# Local
from abis_mapping import base
import abis_mapping.templates.survey_site_data.mapping

# Third-party
import pytest_mock


def test_extract_geometry_defaults(mocker: pytest_mock.MockerFixture) -> None:
    """Test the extract_geometry_defaults method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Construct a dummy raw data set using only the fields that matter to the method.
    rawh = ["siteID", "footprintWKT", "decimalLongitude", "decimalLatitude", "geodeticDatum"]
    raws = [["site1", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "", "", "WGS84"],
            ["site2", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "10.0", "20.0", "WGS84"],
            ["site3", "", "10.0", "20.0", "WGS84"],
            ["site4", "", "", "", ""],
            ["site5", "", "10.0", "20.0", ""],
            ["site6", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "", "", ""]]
    # Amalgamate into a list of dicts
    all_raw = [{hname: val for hname, val in zip(rawh, ln)} for ln in raws]

    # Get the specific mapper
    mapper = abis_mapping.templates.survey_site_data.mapping.SurveySiteMapper()

    # Modify schema to only include the necessary fields for test
    descriptor = {"fields": [
        {"name": "siteID", "type": "string"},
        {"name": "footprintWKT", "type": "wkt"},
        {"name": "decimalLongitude", "type": "number"},
        {"name": "decimalLatitude", "type": "number"},
        {"name": "geodeticDatum", "type": "string"},
    ]}
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
    }
    # Invoke method
    actual = mapper.extract_geometry_defaults(csv_data)

    # Validate
    assert actual == expected
