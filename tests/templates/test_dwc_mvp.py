"""Provides Unit Tests for the `dwc_mvp.csv` Template"""


# Standard
import pathlib
import re

# Local
import abis_mapping


# Constants
TEMPLATE = "dwc_mvp.csv"
DATA_DIR = pathlib.Path("abis_mapping/templates/dwc_mvp/examples/margaret_river_flora/")


def test_validation() -> None:
    """Tests the validation for the template"""
    # Load Data
    data = (DATA_DIR / "margaret_river_flora.csv").read_bytes()

    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert report.valid


def test_mapping() -> None:
    """Tests the mapping for the template"""
    # Load Data and Expected Output
    data = (DATA_DIR / "margaret_river_flora.csv").read_bytes()
    output = (DATA_DIR / "margaret_river_flora.ttl").read_text()

    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE)
    assert mapper

    # Map
    graph = mapper().apply_mapping(data)
    result = graph.serialize(format="ttl")

    # Everything should currently match except for the `dcterms:issued` date
    # The following code replaces that line with regex
    result = re.sub(r"dcterms:issued.+", "test", result)
    output = re.sub(r"dcterms:issued.+", "test", output)
    assert result == output
