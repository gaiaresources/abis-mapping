"""Tests for the survey_site_visit_data v2 template not common to other templates."""

# Standard
import csv
import dataclasses
import io
import pathlib
import unittest

# Third-party
import pyshacl
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import types
import abis_mapping.templates.survey_site_visit_data_v2.mapping

# Typing
from typing import Callable


# Alias mapper
Mapper = abis_mapping.templates.survey_site_visit_data_v2.mapping.SurveySiteVisitMapper


@dataclasses.dataclass
class Scenario:
    name: str
    start_date: str | None = None
    end_date: str | None = None


scenarios = [
    Scenario(
        name="end_date_only",
        end_date="2025-10-11",
    ),
    Scenario(
        name="start_date_only",
        start_date="2024-10-11",
    ),
    Scenario(
        name="both_dates",
        start_date="2024-10-11",
        end_date="2025-10-11",
    ),
    Scenario(
        name="no_dates",
    ),
]


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=scenarios,
    ids=[s.name for s in scenarios],
)
def test_add_temporal_coverage_node(graph_comparer: Callable, scenario: Scenario) -> None:
    """Tests the graph output from add_temporal_coverage_node method.

    Args:
        scenario (Scenario): Data structure containing test parameters.
        graph_comparer (Callable): Graph comparer fixture.
    """
    # Parse dates
    date_fn = lambda x: types.temporal.parse_timestamp(x) if x is not None else None  # noqa: E731
    start_date = date_fn(scenario.start_date)
    end_date = date_fn(scenario.end_date)

    # Create graph
    graph = rdflib.Graph()

    # Create mapper
    mapper = Mapper()

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


class TestExtractTemporalDefaults:
    @pytest.fixture
    def mocked_schema(self, mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
        """Patches and returns mock for schema method on mapper.

        Args:
            mocker (pytest_mock.MockerFixture): Mocker fixture.

        Returns:
            unittest.mock.MagicMock: Mocked schema.
        """
        # Retrieve actual descriptor
        descriptor = Mapper.schema()

        # Define fields of relevance for tests
        fieldnames = ["siteVisitID", "siteVisitStart", "siteVisitEnd"]

        # Make descriptor only include these fields
        descriptor["fields"] = [f for f in descriptor["fields"] if f["name"] in fieldnames]

        # Patch and return
        return mocker.patch.object(Mapper, "schema", return_value=descriptor)

    def test_extract_temporal_defaults(self, mocked_schema: unittest.mock.MagicMock) -> None:
        """Tests the extract_temporal_defaults method.

        Args:
            mocked_schema (unittest.mock.MagicMock): Mocked schema method fixture.
        """
        # Declare some raw data
        rows = [
            {
                "siteVisitID": "SV1",
                "siteVisitStart": "2024-10-14",
                "siteVisitEnd": "2025-10-14",
            },
            {
                "siteVisitID": "SV2",
                "siteVisitStart": "2024-10-14",
            },
            {
                "siteVisitID": "SV3",
                "siteVisitEnd": "2025-10-14",
            },
            # The map should exclude this since there are no
            # values for temporal entity provided without error
            {
                "siteVisitID": "SV4",
            },
        ]
        # Build elements for expected map
        graphs = [rdflib.Graph() for _ in range(3)]
        mapper = Mapper()
        for g, r in zip(graphs, rows, strict=False):
            raw_start = r.get("siteVisitStart")
            raw_end = r.get("siteVisitEnd")
            start = types.temporal.parse_timestamp(raw_start) if raw_start is not None else None
            end = types.temporal.parse_timestamp(raw_end) if raw_end is not None else None
            mapper.add_temporal_coverage_bnode(g, start, end)

        # Construct expected map
        expected = {r["siteVisitID"]: g.serialize(format="turtle") for g, r in zip(graphs, rows, strict=False)}

        # Create raw data csv string
        with io.StringIO() as output:
            csv_writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            csv_writer.writeheader()

            for row in rows:
                csv_writer.writerow(row)

            csv_data = output.getvalue().encode("utf-8")
        # Invoke
        actual = Mapper().extract_temporal_defaults(csv_data)

        # Assert
        assert actual == expected
