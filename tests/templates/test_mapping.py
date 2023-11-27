"""Provides all relevant mapping tests."""


# Standard
import pathlib

# Third-party
import pytest

# Local
from tests.templates import conftest
import abis_mapping
import tests.conftest

# Typing
from typing import Iterable


def mapping_test_args() -> Iterable[tuple[str, str, pathlib.Path, pathlib.Path]]:
    """Constructs parameter sets necessary to perform mapping tests."""
    for test_case in conftest.TEST_CASES:
        for mapping_case in test_case.mapping_cases:
            name = f"{test_case.template_id}"
            name += f"-{mapping_case.scenario_name}" if mapping_case.scenario_name is not None else ""
            d = (name, test_case.template_id, mapping_case.data, mapping_case.expected)
            yield d


@pytest.mark.parametrize(
    argnames="template_id,data_path,expected_path",
    argvalues=[vals[1:] for vals in mapping_test_args()],
    ids=[vals[0] for vals in mapping_test_args()],
)
def test_mapping(template_id: str, data_path: pathlib.Path, expected_path: pathlib.Path) -> None:
    """Tests the mapping for the template"""
    # Load Data and Expected Output
    data = data_path.read_bytes()
    expected = expected_path.read_text()

    # Get Mapper
    mapper = abis_mapping.get_mapper(template_id)
    assert mapper

    # Map
    graphs = list(mapper().apply_mapping(data))

    # Assert
    assert len(graphs) == 1

    # Compare Graphs
    assert tests.conftest.compare_graphs(
        graph1=graphs[0],
        graph2=expected,
    )

    # Check that there are no `None`s in the Graph
    # This check is important. As some fields are optional they can be `None`
    # at runtime. Unfortunately, `None` is valid in many contexts in Python,
    # including string formatting. This means that type-checking is unable to
    # determine whether a statement is valid in our specific context. As such,
    # we check here to see if any `None`s have snuck their way into the RDF.
    assert "None" not in graphs[0].serialize(format="ttl")
