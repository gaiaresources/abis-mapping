"""Provides Unit Tests for the `abis_mapping.utils.vocabs` module"""


# Standard
import textwrap

# Third-Party
import pytest
import rdflib

# Local
import abis_mapping.utils.vocabs


def test_vocabs_term() -> None:
    """Tests the Term Class"""
    # Create Term
    term = abis_mapping.utils.vocabs.Term(
        labels=("A", "B", "C"),
        iri=rdflib.URIRef("D"),
    )

    # Test Mapping
    assert term.to_mapping() == {
        "A": rdflib.URIRef("D"),
        "B": rdflib.URIRef("D"),
        "C": rdflib.URIRef("D"),
    }

    # Test Match
    assert term.match("a")
    assert term.match("A")
    assert term.match("b")
    assert term.match("B")
    assert term.match("c")
    assert term.match("C")
    assert not term.match("X")


def test_vocabs_restricted_vocab() -> None:
    """Tests the RestrictedVocab Class"""
    # Create Vocab
    vocab = abis_mapping.utils.vocabs.RestrictedVocabulary(
        vocab_id="TEST_RESTRICT",
        terms=(
            abis_mapping.utils.vocabs.Term(("A",), rdflib.URIRef("A")),
            abis_mapping.utils.vocabs.Term(("B",), rdflib.URIRef("B")),
        ),
    )

    # Assert Existing Values
    assert vocab.get("a") == rdflib.URIRef("A")
    assert vocab.get("A") == rdflib.URIRef("A")
    assert vocab.get("b") == rdflib.URIRef("B")
    assert vocab.get("B") == rdflib.URIRef("B")

    # Assert Invalid Values
    with pytest.raises(abis_mapping.utils.vocabs.VocabularyError):
        vocab.get("C")


def test_vocabs_flexible_vocab() -> None:
    """Tests the FlexibleVocab Class"""
    # Create Vocab
    vocab = abis_mapping.utils.vocabs.FlexibleVocabulary(
        vocab_id="TEST_FLEX",
        definition=rdflib.Literal("definition"),
        base=rdflib.URIRef("base/"),
        scheme=rdflib.URIRef("scheme"),
        broader=rdflib.URIRef("broader"),
        default=None,
        terms=(
            abis_mapping.utils.vocabs.Term(("A",), rdflib.URIRef("A")),
            abis_mapping.utils.vocabs.Term(("B",), rdflib.URIRef("B")),
        ),
    )

    # Create Graph
    graph = rdflib.Graph()

    # Assert Existing Values
    assert vocab.get(graph, "a") == rdflib.URIRef("A")
    assert vocab.get(graph, "A") == rdflib.URIRef("A")
    assert vocab.get(graph, "b") == rdflib.URIRef("B")
    assert vocab.get(graph, "B") == rdflib.URIRef("B")

    # Assert New Values
    assert vocab.get(graph, "C", rdflib.URIRef("D")) == rdflib.URIRef("base/C")
    assert graph.serialize(format="ttl").strip() == textwrap.dedent(
        """
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <base/C> a skos:Concept ;
            dcterms:source "D"^^xsd:anyURI ;
            skos:broader <broader> ;
            skos:definition "definition" ;
            skos:inScheme <scheme> ;
            skos:prefLabel "C" .
        """
    ).strip()

    # Assert Invalid Values
    with pytest.raises(abis_mapping.utils.vocabs.VocabularyError):
        vocab.get(graph, None)  # No Default
