"""Tests for specific for the `survey_occurrence_data` template."""

# Third-party
import pytest_mock

# Standard
import io
import csv

# Local
from abis_mapping import base


def test_apply_validation_default_map(mocker: pytest_mock.MockerFixture) -> None:
    """Tests the `apply_validation` method with a supplied default map.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """

    # Construct fake data
    rawh = [
        "siteID",
        "decimalLatitude",
        "decimalLongitude",
        "organismQuantity",
        "organismQuantityType",
        "threatStatus",
        "conservationJurisdiction",
    ]
    raws = [
        ["site1", "-38.94", "115.21", "", "", "", ""],
        ["site1", "", "", "", "", "", ""],
        ["site2", "", "", "", "", "", ""],
    ]
    all_raw = [{hname: val for hname, val in zip(rawh, ln)} for ln in raws]

    # Construct default map
    default_map = {
        "site1": "something"
    }

    # Get mapper
    mapper = base.mapper.get_mapper("survey_occurrence_data.csv")

    # Modify schema to only fields required for test
    descriptor = {
        "fields": [field for field in mapper.schema()["fields"] if field["name"] in rawh]
    }
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

    report = mapper().apply_validation(
        data=csv_data,
        site_id_geometry_map=default_map,
    )

    assert report.valid
