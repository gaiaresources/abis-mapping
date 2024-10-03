"""Provides Unit Tests for the `abis_mapping.utils.rdf` module"""

# Third-Party
import rdflib
import pytest

# Local
from abis_mapping import utils


def test_rdf_create_graph() -> None:
    """Tests the create_graph() Function"""
    # Create Graph
    graph = utils.rdf.create_graph()

    # Check Graph returned
    assert isinstance(graph, rdflib.Graph)

    # Check namespaces correctly assigned
    namespaces = list(graph.namespaces())
    required_namespaces = [(name, rdflib.term.URIRef(str(uri))) for (name, uri) in utils.rdf.REQUIRED_NAMESPACES]
    for ns in required_namespaces:
        assert ns in namespaces


def test_rdf_uri() -> None:
    """Tests the uri() Function"""
    # Create Fake Namespace
    namespace = rdflib.Namespace("http://hello.org/")

    # Create URIs
    a = utils.rdf.uri()
    b = utils.rdf.uri(internal_id="hello")
    c = utils.rdf.uri(namespace=namespace)
    d = utils.rdf.uri(internal_id="world", namespace=namespace)

    # Asserts
    assert isinstance(a, rdflib.URIRef)
    assert isinstance(b, rdflib.URIRef)
    assert isinstance(c, rdflib.URIRef)
    assert isinstance(d, rdflib.URIRef)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("http://hello.org", rdflib.Literal("http://hello.org", datatype=rdflib.XSD.anyURI)),
        ("some name", rdflib.Literal("some name")),
    ],
)
def test_rdf_uri_or_string_literal(raw: str, expected: rdflib.Literal) -> None:
    """Test the uri_or_string_literal function.

    Args:
        raw (str): Raw URI or string.
        expected (rdflib.Literal): Expected
    """
    # Call and assert
    assert utils.rdf.uri_or_string_literal(raw) == expected
