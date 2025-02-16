"""Tests the organism quantity type vocab functionality."""

# Local
from abis_mapping import utils

# Third-party
import rdflib


def test_get_percentage_biomass() -> None:
    """Tests that a label using a % sign will retrieve correct term."""
    # Create graph
    graph = rdflib.Graph()

    # Get vocab
    vocab = utils.vocabs.get_flexible_vocab("ORGANISM_QUANTITY_TYPE")
    assert vocab is not None
    iri = vocab(graph=graph, base_iri=utils.namespaces.EXAMPLE).get("% of biomass")

    # Assert
    assert iri == rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiomass")
