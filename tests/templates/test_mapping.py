"""Provides all relevant mapping tests."""

# Third-party
import pyshacl
import pytest
import rdflib

# Local
from tests.templates import conftest
import abis_mapping
import tests.conftest


@pytest.mark.parametrize(
    argnames="template_id,test_params",
    argvalues=[(id_, params) for (_, id_, params) in conftest.mapping_test_args() if params.expected is not None],
    ids=[id_ for (id_, _, params) in conftest.mapping_test_args() if params.expected is not None],
)
def test_apply_mapping(template_id: str, test_params: conftest.MappingParameters) -> None:
    """Tests the mapping for the template.

    Args:
        template_id (str): The id of the template.
        test_params (conftest.MappingParameters): Datastructure
            holding parameters used commonly in tests.
    """
    # Load Data and Expected Output
    data = test_params.data.read_bytes()
    assert test_params.expected is not None
    expected = test_params.expected.read_text()

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

    # Perform shacl validation if provided
    if test_params.shacl is not None:
        shape_graph = rdflib.Graph().parse(data=test_params.shacl.read_bytes())
        for data_graph in graphs:
            valid, _, report = pyshacl.validate(data_graph=data_graph, shacl_graph=shape_graph)
            # If not valid raise assertion error with report output
            assert valid, report

        # Perform validation on the expected result as well
        expected_graph = rdflib.Graph().parse(data=expected)
        valid, _, report = pyshacl.validate(data_graph=expected_graph, shacl_graph=shape_graph)

        # If not valid raise assertion error with report output
        assert valid, report


@pytest.mark.parametrize(
    argnames="template_id,test_params",
    argvalues=[(id_, params) for (_, id_, params) in conftest.chunking_test_args()],
    ids=[id_ for (id_, _, params) in conftest.chunking_test_args()],
)
def test_apply_mapping_chunking(template_id: str, test_params: conftest.ChunkingParameters) -> None:
    """Tests the chunking functionality for apply_mapping where applicable."""
    # Load data
    data = test_params.data.read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(template_id)
    assert mapper

    # Map
    graphs = list(mapper().apply_mapping(data, chunk_size=test_params.chunk_size))

    # Assert
    assert len(graphs) == test_params.yield_count
