"""Tests for the survey_site_visit_data v2 template not common to other templates."""

# Standard
import csv
import dataclasses
import io
import pathlib

# Third-party
import pandas as pd
import pyshacl
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import types
from abis_mapping.templates.survey_site_visit_data_v2 import mapping

# Typing
from typing import Callable, Iterator


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
def test_add_temporal_coverage_node(
    graph_comparer: Callable, scenario: Scenario, mapper: mapping.SurveySiteVisitMapper
) -> None:
    """Tests the graph output from add_temporal_coverage_node method.

    Args:
        scenario (Scenario): Data structure containing test parameters.
        graph_comparer (Callable): Graph comparer fixture.
        mapper (SurveySiteVisitMapper): Site visit mapper instance fixture.
    """
    # Parse dates
    date_fn = lambda x: types.temporal.parse_timestamp(x) if x is not None else None  # noqa: E731
    start_date = date_fn(scenario.start_date)
    end_date = date_fn(scenario.end_date)

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


class TestExtractTemporalDefaults:
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
            raw_start = r.get("siteVisitStart")
            raw_end = r.get("siteVisitEnd")
            start = types.temporal.parse_timestamp(raw_start) if raw_start is not None else None
            end = types.temporal.parse_timestamp(raw_end) if raw_end is not None else None
            mapper.add_temporal_coverage_bnode(g, start, end)

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


class TestApplyValidation:
    @pytest.fixture(scope="class")
    def data(self) -> bytes:
        """Takes an existing csv path and returns it unmodified.

        The csv returned is expected to have both start and end dates plus site visit id
        included for all rows.
        """
        # Create path object and return contents
        return pathlib.Path("abis_mapping/templates/survey_site_visit_data_v2/examples/minimal.csv").read_bytes()

    def _nullify_columns(self, columns: list[str], data: bytes) -> bytes:
        """Replaces any values in specified csv colunms with null.

        Args:
            columns (list[str]): Field names in supplied csv
                to make null values.
            data (bytes): Original csv data to modify.

        Returns:
            bytes: Modified csv.
        """
        # Create dataframe from existing csv
        df = pd.read_csv(io.BytesIO(data))
        # Set all values for columns to null
        for col in columns:
            df[col].values[:] = pd.NA
        # Return csv
        result: bytes = df.to_csv(index=False).encode("utf-8")
        return result

    @pytest.fixture(scope="class")
    def data_no_start_date(self, data: bytes) -> bytes:
        """Modifies existing csv and sets all start dates to null.

        Args:
            data (bytes): The original data fixture

        Returns:
            bytes: Modified csv.
        """
        return self._nullify_columns(["siteVisitStart"], data)

    @pytest.fixture(scope="class")
    def data_no_end_date(self, data: bytes) -> bytes:
        """Modifies existing csv and sets all end dates to null.

        Args:
            data (bytes): The original csv data fixture.

        Returns:
            bytes: Modified csv.
        """
        return self._nullify_columns(["siteVisitEnd"], data)

    def test_with_site_visit_id_map(self, mapper: mapping.SurveySiteVisitMapper, data_no_start_date: bytes) -> None:
        """Tests the apply_validation method with site_visit_id map supplied and no start date.

        Args:
            mapper (SurveySiteVisitMapper): Site visit mapper instance fixture.
            data_no_start_date (bytes): Csv with no start dates.
        """
        # Construct map
        svid_map = {"VA-99": True, "FAKEID": True}

        # Invoke
        report = mapper.apply_validation(data_no_start_date, site_visit_id_map=svid_map)

        # Assert
        assert report.valid

    def test_with_site_visit_id_map_invalid(
        self, mapper: mapping.SurveySiteVisitMapper, data_no_start_date: bytes
    ) -> None:
        """Tests the apply_validation method with site_visit_id_map supplied and no corresponding id in map.

        Args:
            mapper (mapping.SurveySiteVisitMapper): Site visit mapper instances fixture.
            data_no_start_date (bytes): Csv with no start dates.
        """
        # Construct map
        svid_map = {"FAKEID": True}

        # Invoke
        report = mapper.apply_validation(data_no_start_date, site_visit_id_map=svid_map)

        # Assert and check errors
        assert not report.valid
        assert report.flatten(["type"]) == [["row-constraint"]]
