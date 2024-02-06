"""Tests for specific for the `survey_occurrence_data` template."""

# Third-party
import pytest_mock
import attrs
import pytest
import pandas as pd

# Standard
import io
import csv
import pathlib

# Local
from abis_mapping import base
from abis_mapping import utils
from abis_mapping import vocabs
from tests import conftest


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
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site1", "", "", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site3", "-38.94", "115.21", "AGD66", "", "", "", ""],
                ["site4", "-38.94", "115.21", "EPSG:4202", "", "", "", ""],
            ],
            default_map={
                "site1": "something"
            }
        ),
        Scenario(
            name="invalid_missing_from_default_map",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site1", "", "", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={
                "site3": "something"
            },
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_incidental_occurrence_requires_latlong",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["", "", "", "", "", "", "VU", "VIC"],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={},
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="valid_incidental_occurrence_requires_latlong",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["", "-38.94", "115.21", "WGS84", "", "", "VU", "VIC"],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={},
        ),
        Scenario(
            name="invalid_missing_long",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site1", "-38.94", "", "WGS84", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={
                "site1": "something"
            },
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_missing_lat",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site1", "", "115.21", "WGS84", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={
                "site1": "something"
            },
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_incidental_occurrence_missing_lat",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["", "", "115.21", "WGS84", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={},
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_incidental_occurrence_missing_long",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["", "-38.94", "", "WGS84", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={},
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_missing_geodetic_datum",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["site1", "-38.94", "115.21", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={
                "site1": "something"
            },
            expected_error_codes={"row-constraint"}
        ),
        Scenario(
            name="invalid_incidental_occurrence_missing_geodetic_datum",
            raws=[
                ["site1", "-38.94", "115.21", "WGS84", "", "", "", ""],
                ["", "-38.94", "115.21", "", "", "", "", ""],
                ["site2", "-38.94", "115.21", "WGS84", "", "", "", ""],
            ],
            default_map={},
            expected_error_codes={"row-constraint"}
        ),
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=[scenario for scenario in scenarios],
        ids=[scenario.name for scenario in scenarios],
    )
    def test_apply_validation(self, scenario: Scenario, mocker: pytest_mock.MockerFixture) -> None:
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
            "geodeticDatum",
            "organismQuantity",
            "organismQuantityType",
            "threatStatus",
            "conservationJurisdiction",
        ]
        all_raw = [{hname: val for hname, val in zip(rawh, ln)} for ln in scenario.raws]

        # Get mapper
        mapper = base.mapper.get_mapper("survey_occurrence_data.csv")
        assert mapper is not None

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

    def test_apply_mapping(self) -> None:
        """Tests apply_mapping method with default geometry map."""
        # Build a dataframe from an existing csv
        df = pd.read_csv(
            "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.csv"
        )

        # Modify and preserve first entry
        col_names = ["decimalLongitude", "decimalLatitude", "geodeticDatum"]
        s_geo_vals = df[[*col_names, "siteID"]].iloc[0]
        df.loc[0] = df.loc[0].drop(col_names)

        # Proving the values null for first row
        assert df[col_names].loc[0].isna().all()

        # Write out to memory
        with io.StringIO() as output:
            # Write dataframe to memory as csv
            df.to_csv(output, index=False)

            # Assign csv data to variable
            csv_data = output.getvalue().encode("utf-8")

        # Get mapper
        mapper = base.mapper.get_mapper("survey_occurrence_data.csv")
        assert mapper is not None

        expected = pathlib.Path("abis_mapping/templates/survey_occurrence_data/examples/organism_qty.ttl").read_text()

        # Resulting graph doesn't match expected when no lat/long provided
        graphs = list(mapper().apply_mapping(csv_data))
        assert len(graphs) == 1
        assert not conftest.compare_graphs(graphs[0], expected)

        # Make site id geo default map using values extracted previously
        val = str(
            utils.rdf.to_wkt_point_literal(
                latitude=s_geo_vals["decimalLatitude"],
                longitude=s_geo_vals["decimalLongitude"],
                datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(s_geo_vals["geodeticDatum"])
            )
        )
        default_map = {s_geo_vals["siteID"]: val}

        # Create graph
        graphs = list(mapper().apply_mapping(
            data=csv_data,
            site_id_geometry_map=default_map,
        ))
        assert len(graphs) == 1

        # Now with the provided default map values the graph should match.
        assert conftest.compare_graphs(graphs[0], expected)
        assert "None" not in graphs[0].serialize(format="ttl")
