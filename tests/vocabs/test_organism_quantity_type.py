"""Tests the organism quantity type vocab functionality."""

# Local
from abis_mapping import utils
from tests import helpers

# Third-party
import rdflib


def test_get_percentage_biomass() -> None:
    """Tests that a label using a % sign will retrieve correct term."""
    # Create graph
    graph = rdflib.Graph()

    # Get vocab
    vocab = utils.vocabs.get_flexible_vocab("ORGANISM_QUANTITY_TYPE")
    assert vocab is not None
    vocab_instance = vocab(
        graph=graph,
        source=helpers.TEST_DATASET_IRI,
        submitted_on_date=helpers.TEST_SUBMITTED_ON_DATE,
    )
    iri = vocab_instance.get("% of biomass")

    # Assert
    assert iri == rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/369c3d2c-fcf7-4fda-b0b1-3ca10ab4809c")
