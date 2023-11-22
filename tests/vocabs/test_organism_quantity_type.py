"""Tests the organism quantity type vocab functionality."""

# Local
from abis_mapping import vocabs

# Third-party
import rdflib


def test_get_percentage_biomass() -> None:
    """Tests that a label using a % sign will retrieve correct term."""
    # Create graph
    graph = rdflib.Graph()

    # Get vocab
    iri = vocabs.organism_quantity_type.ORGANISM_QUANTITY_TYPE.get(graph, "% of biomass")

    # Assert
    assert iri == rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiomass")
