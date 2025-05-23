"""Provides all relevant mapping tests."""

# Third-party
import pyshacl
import pytest
import rdflib

# Local
from tests.templates import conftest
import abis_mapping
import tests.helpers


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
    graphs = list(
        mapper().apply_mapping(
            data=data,
            chunk_size=None,
            dataset_iri=tests.helpers.TEST_DATASET_IRI,
            base_iri=tests.helpers.TEST_BASE_NAMESPACE,
            submission_iri=tests.helpers.TEST_SUBMISSION_IRI,
            project_iri=tests.helpers.TEST_PROJECT_IRI,
            submitted_on_date=tests.helpers.TEST_SUBMITTED_ON_DATE,
        )
    )

    # Assert
    assert len(graphs) == 1

    # Compare Graphs
    assert tests.helpers.compare_graphs(
        graph1=graphs[0],
        graph2=expected,
    ), (
        "Mapping result did not compare equal with expected graph. "
        "Run the ./scripts/generate_example_ttl_files.py script to update the ttl files "
        "that hold the expected graphs if you have made changes to mapping."
    )

    # Check that there are no `None`s in the Graph
    # This check is important. As some fields are optional they can be `None`
    # at runtime. Unfortunately, `None` is valid in many contexts in Python,
    # including string formatting. This means that type-checking is unable to
    # determine whether a statement is valid in our specific context. As such,
    # we check here to see if any `None`s have snuck their way into the RDF.
    assert "None" not in graphs[0].serialize(format="ttl")


@pytest.mark.parametrize(
    argnames="template_id,test_params",
    argvalues=[(id_, params) for (_, id_, params) in conftest.mapping_test_args() if params.shacl],
    ids=[id_ for (id_, _, params) in conftest.mapping_test_args() if params.shacl],
)
def test_against_shacl(template_id: str, test_params: conftest.MappingParameters) -> None:
    """Tests the mapping for the template against defined shapes.

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
    graphs = list(
        mapper().apply_mapping(
            data=data,
            chunk_size=None,
            dataset_iri=tests.helpers.TEST_DATASET_IRI,
            base_iri=tests.helpers.TEST_BASE_NAMESPACE,
            submission_iri=tests.helpers.TEST_SUBMISSION_IRI,
            project_iri=tests.helpers.TEST_PROJECT_IRI,
            submitted_on_date=tests.helpers.TEST_SUBMITTED_ON_DATE,
        )
    )

    # Assert
    assert len(graphs) == 1

    # Consruct shape graph
    shape_graph = rdflib.Graph()
    for shacl in test_params.shacl:
        shape_graph.parse(data=shacl.read_bytes())

    # Perform validation per data graph
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
    num_chunks = 0
    for chunk in mapper().apply_mapping(
        data=data,
        chunk_size=test_params.chunk_size,
        dataset_iri=tests.helpers.TEST_DATASET_IRI,
        base_iri=tests.helpers.TEST_BASE_NAMESPACE,
        submission_iri=tests.helpers.TEST_SUBMISSION_IRI,
        project_iri=tests.helpers.TEST_PROJECT_IRI,
        submitted_on_date=tests.helpers.TEST_SUBMITTED_ON_DATE,
    ):
        num_chunks += 1
        del chunk

    # Assert
    assert num_chunks == test_params.yield_count
