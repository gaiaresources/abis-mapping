"""Tests for specific for the `survey_occurrence_data` template."""

# Standard
import csv
import io
import pathlib

# Third-party
import attrs
import pandas as pd
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import base
from abis_mapping import models
import abis_mapping.templates.survey_occurrence_data_v3.mapping
import tests.helpers

# Typing
from typing import Iterable


# Alias mapper
Mapper = abis_mapping.templates.survey_occurrence_data_v3.mapping.SurveyOccurrenceMapper

# Convenient shortcut
a = rdflib.RDF.type


@pytest.fixture
def mapper() -> Iterable[Mapper]:
    """Fixture to provide a mapper instance for tests."""
    # Clear schema lru cache prior to creating instance
    Mapper.schema.cache_clear()

    # Yield
    yield Mapper()

    # Clear schema lru cache after running test
    Mapper.schema.cache_clear()


def test_extract_site_visit_id_keys(mocker: pytest_mock.MockerFixture, mapper: Mapper) -> None:
    """Test the extract_site_visit_id_keys method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
        mapper (Mapper): The mapper object fixture.
    """
    # Modify schema to only include the necessary fields
    descriptor = {"fields": [{"name": "siteVisitID", "type": "string"}]}
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Create raw data csv string
    csv_data = b"\r\n".join(
        [
            b"siteVisitID",
            b"S1",
            b"S2",
            b"",
            b"S3",
            b"S2",
            b"S1",
        ]
    )

    expected = {
        "S1": True,
        "S2": True,
        "S3": True,
    }

    # Invoke method
    actual = mapper.extract_site_visit_id_keys(csv_data)

    # Validate
    assert actual == expected


class TestDefaultGeometryMap:
    @attrs.define(kw_only=True)
    class Scenario:
        """Dataclass to hold the scenario parameters."""

        name: str
        raws: list[list[str]]
        expected_error_codes: list[str] | None
        default_map: dict[models.identifier.SiteIdentifier, str]

    # List of scenarios for the apply_validation method tests
    scenarios: list[Scenario] = [
        Scenario(
            name="valid_with_default_map",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "site1", "ORG", "", "", "", ""],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R4", "site3", "ORG", "", "-38.94", "115.21", "AGD66"],
                ["R5", "site4", "ORG", "", "-38.94", "115.21", "EPSG:4202"],
            ],
            default_map={
                (
                    models.identifier.SiteIdentifier(site_id="site1", site_id_source="ORG", existing_bdr_site_iri=None)
                ): "something",
            },
            expected_error_codes=None,
        ),
        Scenario(
            name="invalid_missing_from_default_map",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "site1", "ORG", "", "", "", ""],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="invalid_survey_occurrence_requires_latlong",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "", "", "", "", "", ""],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="valid_survey_occurrence_requires_latlong",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "", "", "", "-38.94", "115.21", "WGS84"],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
                # The following show that non-url safe characters get encoded during mapping.
                ["R4", "site a", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R5", "site/b", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R6", "site%20c", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=None,
        ),
        Scenario(
            name="invalid_missing_long",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "site1", "ORG", "", "-38.94", "", "WGS84"],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={
                (
                    models.identifier.SiteIdentifier(site_id="site1", site_id_source="ORG", existing_bdr_site_iri=None)
                ): "something",
            },
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="invalid_missing_lat",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "site1", "ORG", "", "", "115.21", "WGS84"],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={
                (
                    models.identifier.SiteIdentifier(site_id="site1", site_id_source="ORG", existing_bdr_site_iri=None)
                ): "something",
            },
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="invalid_survey_occurrence_missing_lat",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "", "", "", "", "115.21", "WGS84"],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=["row-constraint", "row-constraint"],
        ),
        Scenario(
            name="invalid_survey_occurrence_missing_long",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "", "", "", "-38.94", "", "WGS84"],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="invalid_missing_geodetic_datum",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "site1", "ORG", "", "-38.94", "115.21", ""],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={
                (
                    models.identifier.SiteIdentifier(site_id="site1", site_id_source="ORG", existing_bdr_site_iri=None)
                ): "something",
            },
            expected_error_codes=["row-constraint"],
        ),
        Scenario(
            name="invalid_survey_occurrence_missing_geodetic_datum",
            raws=[
                ["R1", "site1", "ORG", "", "-38.94", "115.21", "WGS84"],
                ["R2", "", "", "", "-38.94", "115.21", ""],
                ["R3", "site2", "ORG", "", "-38.94", "115.21", "WGS84"],
            ],
            default_map={},
            expected_error_codes=["row-constraint"],
        ),
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=scenarios,
        ids=(scenario.name for scenario in scenarios),
    )
    def test_apply_validation(self, scenario: Scenario, mocker: pytest_mock.MockerFixture, mapper: Mapper) -> None:
        """Tests the `apply_validation` method with a supplied default map.

        Args:
            scenario (Scenario): The parameters of the scenario under test.
            mocker (pytest_mock.MockerFixture): The mocker fixture.
            mapper (Mapper): Mapper instance fixture.
        """
        # Construct fake data
        rawh = [
            "providerRecordID",
            "siteID",
            "siteIDSource",
            "existingBDRSiteIRI",
            "decimalLatitude",
            "decimalLongitude",
            "geodeticDatum",
        ]
        all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in scenario.raws]

        # Modify schema to only fields required for test
        original_fields = mapper.schema()["fields"]
        assert set(rawh) - {f["name"] for f in original_fields} == set()
        descriptor = {"fields": [field for field in original_fields if field["name"] in rawh]}
        descriptor["fields"].sort(key=lambda f: rawh.index(f["name"]))

        # Patch the schema for the test
        mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

        # Create raw data csv string
        output = io.StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=rawh)
        csv_writer.writeheader()
        for row in all_raw:
            csv_writer.writerow(row)
        csv_data = output.getvalue().encode("utf-8")

        # Apply validation
        report = mapper.apply_validation(
            data=csv_data,
            site_id_geometry_map=scenario.default_map,
        )

        # Assert
        if scenario.expected_error_codes is None:
            assert report.valid
        else:
            assert not report.valid
            assert len(report.tasks) == 1
            error_codes = [error.type for error in report.tasks[0].errors]
            assert error_codes == scenario.expected_error_codes

    def test_apply_mapping(self, mapper: Mapper) -> None:
        """Tests apply_mapping method with default geometry map.

        Args:
            mapper (Mapper): Mapper instance fixture.
        """
        # Build a dataframe from an existing csv
        df = pd.read_csv("abis_mapping/templates/survey_occurrence_data_v3/examples/organism_qty.csv")

        # Modify and preserve first entry
        col_names = ["decimalLongitude", "decimalLatitude", "geodeticDatum"]
        s_geo_vals = df[[*col_names, "siteID"]].iloc[0]
        df.loc[0] = df.loc[0].drop(col_names)

        # Proving the values null for first row
        assert df[col_names].loc[0].isna().all()

        # Write out to memory
        output = io.StringIO()
        # Write dataframe to memory as csv
        df.to_csv(output, index=False)

        # Assign csv data to variable
        csv_data = output.getvalue().encode("utf-8")

        expected = pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data_v3/examples/organism_qty.ttl"
        ).read_text()

        # Resulting graph doesn't match expected when no lat/long provided
        graphs = list(
            mapper.apply_mapping(
                data=csv_data,
                chunk_size=None,
                dataset_iri=tests.helpers.TEST_DATASET_IRI,
                base_iri=tests.helpers.TEST_BASE_NAMESPACE,
            )
        )
        assert len(graphs) == 1
        assert not tests.helpers.compare_graphs(graphs[0], expected)

        # Make site id geo default map using values extracted previously
        val = str(
            models.spatial.Geometry(
                raw=models.spatial.LatLong(s_geo_vals["decimalLatitude"], s_geo_vals["decimalLongitude"]),
                datum=s_geo_vals["geodeticDatum"],
            ).to_rdf_literal()
        )
        default_map = {s_geo_vals["siteID"]: val}

        # Create graph
        graphs = list(
            mapper.apply_mapping(
                data=csv_data,
                chunk_size=None,
                dataset_iri=tests.helpers.TEST_DATASET_IRI,
                base_iri=tests.helpers.TEST_BASE_NAMESPACE,
                site_id_geometry_map=default_map,
            )
        )
        assert len(graphs) == 1

        # Now with the provided default map values the graph should match.
        assert tests.helpers.compare_graphs(graphs[0], expected)
        assert "None" not in graphs[0].serialize(format="ttl")


class TestDefaultTemporalMap:
    """Tests specific to the provision of a default temporal map."""

    @attrs.define(kw_only=True)
    class Scenario:
        """Dataclass to hold the scenario parameters."""

        name: str
        raws: list[list[str]]
        expected_error_codes: set[str] = set()
        default_map: dict[str, str]

    scenarios: list[Scenario] = [
        Scenario(
            name="valid_with_default_map",
            raws=[
                ["SV1", "S1", "ORG", "2024-10-16"],
                ["SV2", "S1", "ORG", ""],
                ["SV3", "S1", "ORG", "2024-10-16T15:15:15+0800"],
                ["SV4", "S1", "ORG", ""],
            ],
            default_map={"SV2": "some rdf", "SV4": "some rdf"},
        ),
        Scenario(
            name="invalid_with_default_map",
            raws=[
                ["SV1", "S1", "ORG", "2024-10-16"],
                ["SV2", "S1", "ORG", ""],
                ["SV3", "S1", "ORG", "2024-10-16T15:15:15+0800"],
                ["SV4", "S1", "ORG", ""],
            ],
            default_map={"SV2": "some rdf"},
            expected_error_codes={"row-constraint"},
        ),
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=scenarios,
        ids=[scenario.name for scenario in scenarios],
    )
    def test_apply_validation(self, scenario: Scenario, mocker: pytest_mock.MockerFixture, mapper: Mapper) -> None:
        """Tests the `apply_validation` method with a supplied default map.

        Args:
            scenario (Scenario): The parameters of the scenario under test.
            mocker (pytest_mock.MockerFixture): The mocker fixture.
            mapper (Mapper): Mapper instance fixture.
        """
        # Construct fake data
        rawh = [
            "siteVisitID",
            "siteID",
            "siteIDSource",
            "eventDateStart",
        ]
        all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in scenario.raws]

        # Modify schema to only fields required for test
        descriptor = {"fields": [field for field in Mapper.schema()["fields"] if field["name"] in rawh]}
        descriptor["fields"].sort(key=lambda f: rawh.index(f["name"]))

        # Patch the schema for the test
        mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

        # Create raw data csv string
        output = io.StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=rawh)
        csv_writer.writeheader()
        for row in all_raw:
            csv_writer.writerow(row)
        csv_data = output.getvalue().encode("utf-8")

        # Apply validation
        report = mapper.apply_validation(
            data=csv_data,
            site_visit_id_temporal_map=scenario.default_map,
        )

        # Assert
        assert report.valid == (scenario.expected_error_codes == set())
        if not report.valid:
            error_codes = [code for codes in report.flatten(["type"]) for code in codes]
            assert set(error_codes) == scenario.expected_error_codes

    def test_apply_mapping(self, mapper: Mapper) -> None:
        """Tests the `apply_mapping` method with supplied default map.

        Args:
            mapper (Mapper): Mapper instance fixture.
        """
        # Build a dataframe from an existing csv
        df: pd.DataFrame = pd.read_csv("abis_mapping/templates/survey_occurrence_data_v3/examples/organism_qty.csv")

        # Set first row site_visit_id to test value and nullify event date
        df["siteVisitID"] = df["siteVisitID"].astype(str)
        df.loc[0, "siteVisitID"] = "SV1"
        df.loc[0, "eventDateStart"] = pd.NA

        # Create a default temporal map.
        temp_g = rdflib.Graph()
        top_node = rdflib.BNode()
        ftn = rdflib.URIRef("http://example.com/FakeTestNode")
        temp_g.add((top_node, a, rdflib.TIME.TemporalEntity))
        temp_g.add((top_node, a, ftn))
        site_visit_id_temporal_map = {"SV1": temp_g.serialize()}

        # Invoke
        graphs = mapper.apply_mapping(
            data=df.to_csv(index=False).encode("utf-8"),
            chunk_size=None,
            dataset_iri=tests.helpers.TEST_DATASET_IRI,
            base_iri=tests.helpers.TEST_BASE_NAMESPACE,
            site_visit_id_temporal_map=site_visit_id_temporal_map,
        )
        res_g = next(graphs)
        # Ensure temporal entity added to graph
        assert next(res_g.subjects(a, ftn)) is not None


class TestSiteVisitIDSiteIDMap:
    """Tests specific to the provision of a site visit id -> site id map."""

    @attrs.define(kw_only=True)
    class Scenario:
        """Dataclass to hold the scenario parameters."""

        name: str
        raws: list[list[str | None]]
        expected_error_codes: list[str] | None
        lookup_map: dict[str, models.identifier.SiteIdentifier | None]

    scenarios: list[Scenario] = [
        Scenario(
            name="valid_with_default_map",
            raws=[
                ["SV1", "S1", "ORG", None],
                ["SV2", "S2", "ORG", None],
                ["SV3", None, None, "https://linked.data.gov.au/dataset/bdr/site/ORG/S3"],
            ],
            lookup_map={
                "SV1": None,
                "SV2": models.identifier.SiteIdentifier(
                    site_id="S2",
                    site_id_source="ORG",
                    existing_bdr_site_iri=None,
                ),
                "SV3": models.identifier.SiteIdentifier(
                    site_id=None,
                    site_id_source=None,
                    existing_bdr_site_iri="https://linked.data.gov.au/dataset/bdr/site/ORG/S3",
                ),
            },
            expected_error_codes=None,
        ),
        Scenario(
            name="invalid_with_default_map",
            raws=[
                ["SV1", "S1", "ORG", None],
                ["SV2", "S1", "ORG", None],
                ["SV3", None, None, "https://linked.data.gov.au/dataset/bdr/site/ORG/S1"],
            ],
            lookup_map={
                "SV2": models.identifier.SiteIdentifier(
                    site_id="S2",
                    site_id_source="ORG",
                    existing_bdr_site_iri=None,
                ),
                "SV3": models.identifier.SiteIdentifier(
                    site_id=None,
                    site_id_source=None,
                    existing_bdr_site_iri="https://linked.data.gov.au/dataset/bdr/site/ORG/S3",
                ),
            },
            expected_error_codes=["constraint-error", "row-constraint", "row-constraint"],
        ),
    ]

    @pytest.mark.parametrize(
        argnames="scenario",
        argvalues=scenarios,
        ids=[scenario.name for scenario in scenarios],
    )
    def test_apply_validation(self, scenario: Scenario, mocker: pytest_mock.MockerFixture, mapper: Mapper) -> None:
        """Tests the `apply_validation` method with a supplied default map.

        Args:
            scenario (Scenario): The parameters of the scenario under test.
            mocker (pytest_mock.MockerFixture): The mocker fixture.
            mapper (Mapper): Mapper instance fixture.
        """
        # Construct fake data
        rawh = [
            "siteVisitID",
            "siteID",
            "siteIDSource",
            "existingBDRSiteIRI",
        ]
        all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in scenario.raws]

        # Modify schema to only fields required for test
        descriptor = {"fields": [field for field in Mapper.schema()["fields"] if field["name"] in rawh]}
        descriptor["fields"].sort(key=lambda f: rawh.index(f["name"]))

        # Patch the schema for the test
        mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

        # Create raw data csv string
        output = io.StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=rawh)
        csv_writer.writeheader()
        for row in all_raw:
            csv_writer.writerow(row)
        csv_data = output.getvalue().encode("utf-8")

        # Apply validation
        report = mapper.apply_validation(
            data=csv_data,
            site_visit_id_site_id_map=scenario.lookup_map,
        )

        # Assert
        if scenario.expected_error_codes is None:
            assert report.valid
        else:
            assert not report.valid
            assert len(report.tasks) == 1
            error_codes = [error.type for error in report.tasks[0].errors]
            assert error_codes == scenario.expected_error_codes


def test_extract_site_id_keys(
    mocker: pytest_mock.MockerFixture,
    mapper: Mapper,
) -> None:
    """Test the extract_site_id_keys method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Construct a raw data set only using fields relevant to method.
    rawh = ["siteID", "siteIDSource", "existingBDRSiteIRI"]
    raws = [
        ["site1", "ORG", ""],
        ["", "", ""],
        ["site2", "ORG", ""],
        ["site2", "ORG", ""],
        ["", "", "SITE-IRI"],
    ]

    # Amalgamate into a list of dicts
    all_raw = [{hname: val for hname, val in zip(rawh, ln, strict=True)} for ln in raws]

    # Modify schema to only include the necessary fields
    descriptor = {
        "fields": [
            {"name": "siteID", "type": "string"},
            {"name": "siteIDSource", "type": "string"},
            {"name": "existingBDRSiteIRI", "type": "string"},
        ]
    }
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Create raw data csv string
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=rawh)
    csv_writer.writeheader()
    for row in all_raw:
        csv_writer.writerow(row)
    csv_data = output.getvalue().encode("utf-8")

    expected = {
        models.identifier.SiteIdentifier(site_id="site1", site_id_source="ORG", existing_bdr_site_iri=None): True,
        models.identifier.SiteIdentifier(site_id="site2", site_id_source="ORG", existing_bdr_site_iri=None): True,
        models.identifier.SiteIdentifier(site_id=None, site_id_source=None, existing_bdr_site_iri="SITE-IRI"): True,
    }

    # Invoke method
    actual = mapper.extract_site_id_keys(csv_data)

    # Validate
    assert actual == expected


def test_validation_with_survey_id_set_valid(
    mapper: Mapper,
) -> None:
    """Test surveyID cross-validation when the file is valid."""
    example_file = pathlib.Path(
        "abis_mapping/templates/survey_occurrence_data_v3/examples/margaret_river_flora/margaret_river_flora.csv"
    )

    with example_file.open("rb") as data:
        report = mapper.apply_validation(
            data,
            # provide surveyIDs in the file, to make it valid
            survey_id_set={"MR-R1": True},
        )

    assert report.valid


def test_validation_with_survey_id_set_invalid(
    mapper: Mapper,
) -> None:
    """Test surveyID cross-validation when the file is invalid."""
    example_file = pathlib.Path(
        "abis_mapping/templates/survey_occurrence_data_v3/examples/margaret_river_flora/margaret_river_flora.csv"
    )

    with example_file.open("rb") as data:
        report = mapper.apply_validation(
            data,
            # Don't provide surveyIDs in the file, to make it invalid
            survey_id_set={"SOME_OTHER_ID": True},
        )

    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 2
    assert report.tasks[0].errors[0].note == "surveyID must match a surveyID in the survey_metadata template"
    assert report.tasks[0].errors[1].note == "surveyID must match a surveyID in the survey_metadata template"
