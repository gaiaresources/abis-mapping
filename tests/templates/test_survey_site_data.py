"""Tests for the survey_site_data template not common to other templates."""
import csv
import io
from abis_mapping import base
import pytest_mock

import abis_mapping.templates.survey_site_data.mapping


def test_extract_geometry_defaults(mocker: pytest_mock.MockerFixture) -> None:
    """Test the extract_geometry_defaults method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Construct a dummy raw data set using only the fields that matter to the method.
    rawh = ["siteID", "footprintWKT", "decimalLongitude", "decimalLatitude"]
    raws = [["site1", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "", ""],
            ["site2", "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))", "10.0", "20.0"],
            ["site3", "", "10.0", "20.0"],
            ["site4", "", "", ""]]
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
        "site1": "POINT (2.5 2.5)",
        "site2": "POINT (2.5 2.5)",
        "site3": "POINT (10 20)",
    }
    # Invoke method
    actual = mapper.extract_geometry_defaults(csv_data)

    # Validate
    assert actual == expected
