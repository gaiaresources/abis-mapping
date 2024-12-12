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

    # Create URI
    result = utils.rdf.uri(internal_id="world", namespace=namespace)

    # Asserts
    assert isinstance(result, rdflib.URIRef)
    assert result == rdflib.URIRef("http://hello.org/world")


@pytest.mark.parametrize(
    ("namespace", "path", "fields", "expected"),
    [
        pytest.param(
            rdflib.Namespace("https://test.com/foo/"),
            "",
            {},
            rdflib.URIRef("https://test.com/foo/"),
            id="empty path",
        ),
        pytest.param(
            rdflib.Namespace("https://test.com/foo/"),
            "bar",
            {},
            rdflib.URIRef("https://test.com/foo/bar"),
            id="static path",
        ),
        pytest.param(
            rdflib.Namespace("https://test.com/foo/"),
            "bar/{v}",
            {"v": "123"},
            rdflib.URIRef("https://test.com/foo/bar/123"),
            id="path with field to replace",
        ),
        pytest.param(
            rdflib.Namespace("https://test.com/foo/"),
            "bar/{v1}/cat/{v2}",
            {"v1": "123", "v2": "A B C?!"},
            rdflib.URIRef("https://test.com/foo/bar/123/cat/A%20B%20C%3F%21"),
            id="path with fields to replace with special chars",
        ),
    ],
)
def test_uri_quoted(
    namespace: rdflib.Namespace,
    path: str,
    fields: dict[str, str],
    expected: rdflib.URIRef,
) -> None:
    """Test the uri_quoted function.

    Args:
        namespace: The namespace for the uri_quoted function
        path: The path for the uri_quoted function
        fields: The fields to pass as kwargs to uri_quoted
        expected: The expected return for the uri_quoted function
    """
    result = utils.rdf.uri_quoted(namespace, path, **fields)
    assert result == expected


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
