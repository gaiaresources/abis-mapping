"""Tests for the survey_site_visit_data v2 template not common to other templates."""

# Standard
import csv
import dataclasses
import io
import pathlib

# Third-party
import pyshacl
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import models
from abis_mapping.templates.survey_site_visit_data_v2 import mapping

# Typing
from typing import Iterator


@pytest.fixture
def mapper() -> Iterator[mapping.SurveySiteVisitMapper]:
    """Provides site visit mapper for tests.

    Yields:
        SurveySiteVisitMapper: site visit mapper instance.
    """
    # Create mapper
    mapper = mapping.SurveySiteVisitMapper()

    # Clear schema cache
    mapper.schema.cache_clear()

    # Yield mapper
    yield mapper

    # Clear schema cache again
    mapper.schema.cache_clear()


@dataclasses.dataclass
class Scenario:
    name: str
    start_date: str
    end_date: str | None = None


scenarios = [
    Scenario(
        name="start_date_only",
        start_date="2024-10-11",
    ),
    Scenario(
        name="both_dates",
        start_date="2024-10-11",
        end_date="2025-10-11",
    ),
]


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=scenarios,
    ids=[s.name for s in scenarios],
)
def test_add_temporal_coverage_node(scenario: Scenario, mapper: mapping.SurveySiteVisitMapper) -> None:
    """Tests the graph output from add_temporal_coverage_node method.

    Args:
        scenario (Scenario): Data structure containing test parameters.
        mapper (SurveySiteVisitMapper): Site visit mapper instance fixture.
    """
    # Parse dates
    start_date = models.temporal.parse_timestamp(scenario.start_date)
    end_date = None if scenario.end_date is None else models.temporal.parse_timestamp(scenario.end_date)

    # Create graph
    graph = rdflib.Graph()

    # Invoke
    mapper.add_temporal_coverage_bnode(
        graph=graph,
        start_date=start_date,
        end_date=end_date,
    )

    # Perform validation on shapes
    shape_file = pathlib.Path("abis_mapping/base/validators/shapes.ttl")
    shape_graph = rdflib.Graph().parse(data=shape_file.read_bytes())
    valid, _, report = pyshacl.validate(data_graph=graph, shacl_graph=shape_graph)

    # If not valid raise assertion error with report output
    assert valid, report


class TestMapExtractors:
    """Tests for the key value extraction methods."""

    def test_extract_temporal_defaults(
        self,
        mapper: mapping.SurveySiteVisitMapper,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests the extract_temporal_defaults method.

        Args:
            mapper (SurveySiteVisitMapper): Site visit mapper instance fixture.
            mocker (pytest_mock.MockerFixture): The mocker fixture
        """
        # Retrieve actual descriptor
        original_descriptor = mapping.SurveySiteVisitMapper.schema()

        # Define fields of relevance for tests
        fieldnames = ["siteVisitID", "siteVisitStart", "siteVisitEnd"]

        # Make descriptor only include these fields
        descriptor = {
            **original_descriptor,
            "fields": [f for f in original_descriptor["fields"] if f["name"] in fieldnames],
        }

        # Patch schema
        mocked_schema = mocker.patch.object(mapping.SurveySiteVisitMapper, "schema", return_value=descriptor)

        # Declare some raw data
        expected_rows = [
            {
                "siteVisitID": "SV1",
                "siteVisitStart": "2024-10-14",
                "siteVisitEnd": "2025-10-14",
            },
            {
                "siteVisitID": "SV2",
                "siteVisitStart": "2024-10-14",
            },
        ]
        excluded_rows = [
            # The map should exclude these since there are no
            # values for default temporal entity must have start date
            {
                "siteVisitID": "SV3",
                "siteVisitEnd": "2025-10-14",
            },
            {
                "siteVisitID": "SV4",
            },
            # map should exclude these because there is no siteVisitID
            {
                "siteVisitID": "",
                "siteVisitStart": "2024-10-14",
                "siteVisitEnd": "2025-10-14",
            },
            {
                "siteVisitID": "",
                "siteVisitStart": "2024-10-14",
            },
        ]
        # Build elements for expected map
        graphs = [rdflib.Graph() for _ in range(2)]
        for g, r in zip(graphs, expected_rows, strict=True):
            raw_start: str = r["siteVisitStart"]
            raw_end: str | None = r.get("siteVisitEnd")
            start = models.temporal.parse_timestamp(raw_start)
            end = models.temporal.parse_timestamp(raw_end) if raw_end is not None else None
            mapper.add_temporal_coverage_bnode(graph=g, start_date=start, end_date=end)

        # Construct expected map
        expected = {r["siteVisitID"]: g.serialize(format="turtle") for g, r in zip(graphs, expected_rows, strict=True)}

        # Create raw data csv string
        with io.StringIO() as output:
            csv_writer = csv.DictWriter(output, fieldnames=expected_rows[0].keys())
            csv_writer.writeheader()

            for row in expected_rows + excluded_rows:
                csv_writer.writerow(row)

            csv_data = output.getvalue().encode("utf-8")
        # Invoke
        actual = mapper.extract_temporal_defaults(csv_data)

        # Assert
        assert actual == expected
        mocked_schema.assert_called_once()

    def test_extract_site_visit_id_to_site_id_map(
        self,
        mapper: mapping.SurveySiteVisitMapper,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests the extract_site_visit_id_to_site_id_map method.

        Args:
            mapper: Mapper instance fixture.
            mocker: The mocker fixture.
        """
        # Retrieve actual descriptor
        original_descriptor = mapping.SurveySiteVisitMapper.schema()

        # Define fields of relevance for tests
        fieldnames = ["siteID", "siteVisitID"]

        # Make descriptor only include these fields
        descriptor = {
            **original_descriptor,
            "fields": [f for f in original_descriptor["fields"] if f["name"] in fieldnames],
        }

        # Patch schema
        mocked_schema = mocker.patch.object(mapping.SurveySiteVisitMapper, "schema", return_value=descriptor)

        # Declare some raw data
        expected_rows: list[dict[str, str | None]] = [
            {
                "siteID": "S1",
                "siteVisitID": "SV1",
            },
            {
                "siteID": "S1",
                "siteVisitID": "SV2",
            },
        ]
        excluded_rows: list[dict[str, str | None]] = [
            # The map should exclude these since there are no
            # values for siteID
            {
                "siteID": "",
                "siteVisitID": "SV3",
            },
            {
                "siteID": None,
                "siteVisitID": "SV4",
            },
            # map should exclude these because there is no siteVisitID
            {
                "siteID": "S2",
                "siteVisitID": "",
            },
            {
                "siteID": "S3",
                "siteVisitID": None,
            },
        ]
        # Construct expected map
        expected = {r["siteVisitID"]: r["siteID"] for r in expected_rows}

        # Create raw data csv string
        with io.StringIO() as output:
            csv_writer = csv.DictWriter(output, fieldnames=expected_rows[0].keys())
            csv_writer.writeheader()

            for row in expected_rows + excluded_rows:
                csv_writer.writerow(row)

            csv_data = output.getvalue().encode("utf-8")
        # Invoke
        actual = mapper.extract_site_visit_id_to_site_id_map(csv_data)

        # Assert
        assert actual == expected
        mocked_schema.assert_called_once()
