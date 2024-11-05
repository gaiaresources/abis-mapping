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
    ("namespace", "path", "fields", "expected"),
    [
        (rdflib.Namespace("https://test.com/foo/"), "", {}, rdflib.URIRef("https://test.com/foo/")),
        (rdflib.Namespace("https://test.com/foo/"), "bar", {}, rdflib.URIRef("https://test.com/foo/bar")),
        (
            rdflib.Namespace("https://test.com/foo/"),
            "bar/{v}",
            {"v": "123"},
            rdflib.URIRef("https://test.com/foo/bar/123"),
        ),
        (
            rdflib.Namespace("https://test.com/foo/"),
            "bar/{v1}/cat/{v2}",
            {"v1": "123", "v2": "A B C?!"},
            rdflib.URIRef("https://test.com/foo/bar/123/cat/A%20B%20C%3F%21"),
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

    * different length paths
    * with/without special chars
    * with/without replacement fields
    """
    result = utils.rdf.uri_quoted(namespace, path, **fields)
    assert result == expected


@pytest.mark.parametrize(
    ("base", "extension", "expected"),
    [
        (rdflib.URIRef("https://test.com/foo"), ["bar"], rdflib.URIRef("https://test.com/foo/bar")),
        (rdflib.URIRef("https://test.com/foo/"), ["bar"], rdflib.URIRef("https://test.com/foo/bar")),
        (rdflib.URIRef("https://test.com/foo"), ["bar", "cc"], rdflib.URIRef("https://test.com/foo/bar/cc")),
        (rdflib.URIRef("https://test.com/foo/"), ["bar", "cc"], rdflib.URIRef("https://test.com/foo/bar/cc")),
        (rdflib.URIRef("https://test.com/foo"), ["a a", "/c?d:"], rdflib.URIRef("https://test.com/foo/a-a/c-d")),
    ],
)
def test_extend_uri(
    base: rdflib.URIRef,
    extension: list[str],
    expected: rdflib.URIRef,
) -> None:
    """Test the extend_uri function.

    * with/without trailing / in base
    * with/without special chars
    * different length extensions
    """
    result = utils.rdf.extend_uri(base, *extension)
    assert result == expected


@pytest.mark.parametrize(
    ("base", "extension", "expected"),
    [
        (rdflib.URIRef("https://test.com/foo"), ["bar"], rdflib.URIRef("https://test.com/foo/bar")),
        (rdflib.URIRef("https://test.com/foo/"), ["bar"], rdflib.URIRef("https://test.com/foo/bar")),
        (rdflib.URIRef("https://test.com/foo"), ["bar", "cc"], rdflib.URIRef("https://test.com/foo/bar/cc")),
        (rdflib.URIRef("https://test.com/foo/"), ["bar", "cc"], rdflib.URIRef("https://test.com/foo/bar/cc")),
        (
            rdflib.URIRef("https://test.com/foo"),
            ["a a", "/c?d:"],
            rdflib.URIRef("https://test.com/foo/a%20a/%2Fc%3Fd%3A"),
        ),
    ],
)
def test_extend_uri_quoted(
    base: rdflib.URIRef,
    extension: list[str],
    expected: rdflib.URIRef,
) -> None:
    """Test the extend_uri function.

    * with/without trailing / in base
    * with/without special chars
    * different length extensions
    """
    result = utils.rdf.extend_uri_quoted(base, *extension)
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
