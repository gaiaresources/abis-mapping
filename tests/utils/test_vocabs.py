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
        description="E",
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
    class Vocab(abis_mapping.utils.vocabs.RestrictedVocabulary):
        vocab_id = "TEST_RESTRICT"
        terms = (
            abis_mapping.utils.vocabs.Term(
                labels=("A",),
                iri=rdflib.URIRef("A"),
                description="A",
            ),
            abis_mapping.utils.vocabs.Term(
                labels=("B",),
                iri=rdflib.URIRef("B"),
                description="B",
            ),
        )

    vocab = Vocab(graph=rdflib.Graph())

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
    class Vocab(abis_mapping.utils.vocabs.FlexibleVocabulary):
        vocab_id = "TEST_FLEX"
        definition = rdflib.Literal("definition")
        base = rdflib.URIRef("base/")
        scheme = rdflib.URIRef("scheme")
        broader = rdflib.URIRef("broader")
        default = None
        terms = (
            abis_mapping.utils.vocabs.Term(
                labels=("A",),
                iri=rdflib.URIRef("A"),
                description="A",
            ),
            abis_mapping.utils.vocabs.Term(
                labels=("B",),
                iri=rdflib.URIRef("B"),
                description="B",
            ),
        )

    # Create graph
    graph = rdflib.Graph()

    # Initialize vocab
    vocab = Vocab(graph=graph)

    # Assert Existing Values
    assert vocab.get("a") == rdflib.URIRef("A")
    assert vocab.get("A") == rdflib.URIRef("A")
    assert vocab.get("b") == rdflib.URIRef("B")
    assert vocab.get("B") == rdflib.URIRef("B")

    # Assert New Values
    vocab.source = rdflib.URIRef("D")
    assert vocab.get("C") == rdflib.URIRef("base/C")
    assert (
        graph.serialize(format="ttl").strip()
        == textwrap.dedent(
            """
        @prefix schema: <https://schema.org/> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <base/C> a skos:Concept ;
            skos:broader <broader> ;
            skos:definition "definition" ;
            skos:inScheme <scheme> ;
            skos:prefLabel "C" ;
            schema:citation "D"^^xsd:anyURI .
        """
        ).strip()
    )

    # Assert Invalid Values
    with pytest.raises(abis_mapping.utils.vocabs.VocabularyError):
        vocab.get(None)  # No Default


def test_vocab_register_id() -> None:
    """Tests that vocabs get registered at import."""
    assert len(abis_mapping.utils.vocabs.Vocabulary.id_registry) > 0


def test_get_vocab() -> None:
    """Tests get_vocab function."""
    # Retrieve vocab
    v1 = abis_mapping.utils.vocabs.get_vocab("SEX")

    # Assert exists
    assert v1 is not None
    assert issubclass(v1, abis_mapping.utils.vocabs.FlexibleVocabulary)


def test_get_vocab_invalid() -> None:
    """Tests get_vocab function with an invalid vocab."""
    # Should raise key error
    with pytest.raises(ValueError):
        abis_mapping.utils.vocabs.get_vocab("NOT_A_VOCAB")
