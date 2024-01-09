"""Tests for specific for the `survey_occurrence_data` template."""

# Third-party
import pytest_mock
import attrs
import pytest

# Standard
import io
import csv

# Local
from abis_mapping import base


class TestDefaultMap:
    @attrs.define(kw_only=True)
    class Scenario:
        """Dataclass to hold the scenario parameters."""
        name: str
        raws: list[list[str]]
        expected_error_codes: set[str] = set()
        default_map: dict[str, str]

    # List of scenarios for the apply_validation method tests
    scenarios: list[Scenario] = [
        Scenario(
            name="valid_with_default_map",
            raws=[
                ["site1", "-38.94", "115.21", "", "", "", ""],
                ["site1", "", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "", "", "", ""],
            ],
            default_map={
                "site1": "something"
            }
        ),
        Scenario(
            name="invalid_missing_from_default_map",
            raws=[
                ["site1", "-38.94", "115.21", "", "", "", ""],
                ["site1", "", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "", "", "", ""],
            ],
            default_map={
                "site3": "something"
            },
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_incidental_occurrence_requires_latlong",
            raws=[
                ["site1", "-38.94", "115.21", "", "", "", ""],
                ["", "", "", "", "", "VU", "VIC"],
                ["site2", "-38.94", "115.21", "", "", "", ""],
            ],
            default_map={},
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="valid_incidental_occurrence_requires_latlong",
            raws=[
                ["site1", "-38.94", "115.21", "", "", "", ""],
                ["", "-38.94", "115.21", "", "", "VU", "VIC"],
                ["site2", "-38.94", "115.21", "", "", "", ""],
            ],
            default_map={},
        )
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=[scenario for scenario in scenarios],
        ids=[scenario.name for scenario in scenarios],
    )
    def test_apply_validation_default_map(self, scenario: Scenario, mocker: pytest_mock.MockerFixture) -> None:
        """Tests the `apply_validation` method with a supplied default map.

        Args:
            scenario (Scenario): The parameters of the scenario under test.
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
        all_raw = [{hname: val for hname, val in zip(rawh, ln)} for ln in scenario.raws]

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

        # Apply validation
        report = mapper().apply_validation(
            data=csv_data,
            site_id_geometry_map=scenario.default_map,
        )

        # Assert
        assert report.valid == (scenario.expected_error_codes == set())
        if not report.valid:
            error_codes = [code for codes in report.flatten(['type']) for code in codes]
            assert set(error_codes) == scenario.expected_error_codes
