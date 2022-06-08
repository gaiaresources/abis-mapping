"""Provides Unit Tests for the `abis_mapping.utils.vocabs` module"""


# Standard
import textwrap

# Third-Party
import pytest
import rdflib

# Local
from abis_mapping import utils


def test_vocabs_restricted_vocab() -> None:
    """Tests the RestrictedVocab Class"""
    # Create Vocab
    vocab = utils.vocabs.RestrictedVocabulary(
        mapping={
            "A": rdflib.URIRef("A"),
            "B": rdflib.URIRef("B"),
        }
    )

    # Assert Existing Values
    assert vocab.get("A") == rdflib.URIRef("A")
    assert vocab.get("B") == rdflib.URIRef("B")

    # Assert Invalid Values
    with pytest.raises(utils.vocabs.VocabularyError):
        vocab.get("C")


def test_vocabs_flexible_vocab() -> None:
    """Tests the FlexibleVocab Class"""
    # Create Vocab
    vocab = utils.vocabs.FlexibleVocabulary(
        definition=rdflib.Literal("definition"),
        base=rdflib.URIRef("base/"),
        scheme=rdflib.URIRef("scheme"),
        broader=rdflib.URIRef("broader"),
        default=None,
        mapping={
            "A": rdflib.URIRef("A"),
            "B": rdflib.URIRef("B"),
        }
    )

    # Create Graph
    graph = rdflib.Graph()

    # Assert Existing Values
    assert vocab.get(graph, "A") == rdflib.URIRef("A")
    assert vocab.get(graph, "B") == rdflib.URIRef("B")

    # Assert New Values
    assert vocab.get(graph, "C") == rdflib.URIRef("base/C")
    assert graph.serialize(format="ttl").strip() == textwrap.dedent(
        """
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <base/C> a skos:Concept ;
            skos:broader <broader> ;
            skos:definition "definition" ;
            skos:inScheme <scheme> ;
            skos:prefLabel "C" .
        """
    ).strip()

    # Assert Invalid Values
    with pytest.raises(utils.vocabs.VocabularyError):
        vocab.get(graph, None)  # No Default
