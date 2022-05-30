"""Provides Unit Tests for the `dwc_mvp.csv` Template"""


# Standard
import pathlib

# Local
import abis_mapping
import tests.conftest


# Constants
TEMPLATE_ID = "dwc_mvp.csv"
DATA = pathlib.Path("abis_mapping/templates/dwc_mvp/examples/margaret_river_flora/margaret_river_flora.csv")
EXPECTED = pathlib.Path("abis_mapping/templates/dwc_mvp/examples/margaret_river_flora/margaret_river_flora.ttl")


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
