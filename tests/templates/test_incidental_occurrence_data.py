"""Provides Unit Tests for the `incidental_occurrence_data.csv` Template"""


# Standard
import pathlib

# Local
import abis_mapping
import tests.conftest


# Constants
TEMPLATE_ID = "incidental_occurrence_data.csv"
DATA = pathlib.Path(
    "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv"
)
EXPECTED = pathlib.Path(
    "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.ttl"
)  # noqa: E501


def test_validation() -> None:
    """Tests the validation for the template"""
    # Load Data
    data = DATA.read_bytes()

    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert report.valid


def test_mapping() -> None:
    """Tests the mapping for the template"""
    # Load Data and Expected Output
    data = DATA.read_bytes()
    expected = EXPECTED.read_text()

    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
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
