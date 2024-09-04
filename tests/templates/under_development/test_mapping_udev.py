"""Provides tests for the template mapping modules whilst in development."""

# Standard
import pathlib
import dataclasses
import os

# Third-party
import pyshacl
import pytest
import rdflib

# Local
from abis_mapping import base
from abis_mapping import settings
import abis_mapping.templates.incidental_occurrence_data_v3.mapping
import abis_mapping.templates.survey_occurrence_data_v2.mapping

# Typing
from typing import Callable, Type


@dataclasses.dataclass
class Parameters:
    mapper: Type[base.mapper.ABISMapper]
    data: bytes
    expected: str
    shacl: bytes


minversion = pytest.mark.skipif(
    settings.SETTINGS.MAJOR_VERSION < 5 and not os.getenv("PYTEST_NO_SKIPS"), reason="templates not released until v5"
)


@minversion
@pytest.mark.parametrize(
    "parameters",
    [
        Parameters(
            mapper=abis_mapping.templates.incidental_occurrence_data_v3.mapping.IncidentalOccurrenceMapper,
            data=pathlib.Path(
                "abis_mapping/templates/incidental_occurrence_data_v3/examples/margaret_river_flora/margaret_river_flora.csv"  # noqa: E501
            ).read_bytes(),
            expected=pathlib.Path(
                "abis_mapping/templates/incidental_occurrence_data_v3/examples/margaret_river_flora/margaret_river_flora.ttl"  # noqa: E501
            ).read_text(),
            shacl=pathlib.Path(
                "abis_mapping/templates/incidental_occurrence_data_v3/validators/validator.ttl"
            ).read_bytes(),
        ),
        Parameters(
            mapper=abis_mapping.templates.survey_occurrence_data_v2.mapping.SurveyOccurrenceMapper,
            data=pathlib.Path(
                "abis_mapping/templates/survey_occurrence_data_v2/examples/margaret_river_flora/margaret_river_flora.csv"  # noqa: E501
            ).read_bytes(),
            expected=pathlib.Path(
                "abis_mapping/templates/survey_occurrence_data_v2/examples/margaret_river_flora/margaret_river_flora.ttl"  # noqa: E501
            ).read_text(),
            shacl=pathlib.Path(
                "abis_mapping/templates/survey_occurrence_data_v2/validators/validator.ttl"
            ).read_bytes(),
        ),
    ]
)
class TestMapping:
    def test_apply_mapping(self, parameters: Parameters, graph_comparer: Callable) -> None:
        """Tests apply mapping for the specific template while in development.

        Args:
            parameters (Parameters): Parameters for the test.
            graph_comparer (Callable): Graph comparison fixture.
        """
        # Invoke
        graphs: list[rdflib.Graph] = list(parameters.mapper().apply_mapping(parameters.data))

        # Ensure only one graph
        assert len(graphs) == 1

        # Compare, output to file if not valid
        if not (is_same := graph_comparer(graphs[0], parameters.expected)):
            graphs[0].serialize(f"tests/templates/under_development/{parameters.mapper().template_id}-result.ttl")
        assert is_same

        # Check that there are no `None`s in the Graph
        # This check is important. As some fields are optional they can be `None`
        # at runtime. Unfortunately, `None` is valid in many contexts in Python,
        # including string formatting. This means that type-checking is unable to
        # determine whether a statement is valid in our specific context. As such,
        # we check here to see if any `None`s have snuck their way into the RDF.
        assert "None" not in graphs[0].serialize(format="ttl")

    def test_shapes(self, parameters: Parameters) -> None:
        """Tests generated rdf against expected shape graph.

        Args:
            parameters (Parameters): Parameters for the test.
        """
        # Create data graph
        data_graphs = (g for g in parameters.mapper().apply_mapping(parameters.data))

        # Create shape graph
        shape_graph = rdflib.Graph().parse(data=parameters.shacl)

        # Perform validation
        for data_graph in data_graphs:
            valid, _, report = pyshacl.validate(data_graph=data_graph, shacl_graph=shape_graph)
            if not valid:
                raise AssertionError(report)

        # Perform validation on the expected result as well
        expected_graph = rdflib.Graph().parse(data=parameters.expected)
        valid, _, report = pyshacl.validate(data_graph=expected_graph, shacl_graph=shape_graph)

        if not valid:
            raise AssertionError(report)
