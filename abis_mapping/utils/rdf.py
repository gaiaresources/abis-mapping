"""Provides rdf utilities for the package"""

# Standard
import urllib.parse

# Third-Party
import rdflib
import slugify

# Local
from . import namespaces

# The required set of namespaces for the create_graph utility function
REQUIRED_NAMESPACES = [
    ("rdf", rdflib.RDF),
    ("rdfs", rdflib.RDFS),
    ("void", rdflib.VOID),
    ("sosa", rdflib.SOSA),
    ("dcterms", rdflib.DCTERMS),
    ("prov", rdflib.PROV),
    ("time", rdflib.TIME),
    ("xsd", rdflib.XSD),
    ("schema", rdflib.SDO),
    ("geo", namespaces.GEO),
    ("tern", namespaces.TERN),
    ("dwc", namespaces.DWC),
    ("bdr", namespaces.BDR),
    ("abis", namespaces.ABIS),
]


def create_graph() -> rdflib.Graph:
    """Utility function that creates a base rdflib.Graph with the required
    namespaces bound with their expected prefix.

    Returns:
        rdflib.Graph: Graph with expected namespaces bound.
    """
    # Create Graph
    graph = rdflib.Graph()

    # Bind Namespaces
    for ns in REQUIRED_NAMESPACES:
        graph.bind(*ns)

    # Return
    return graph


def uri(
    internal_id: str,
    namespace: rdflib.Namespace,
) -> rdflib.URIRef:
    """Generates an rdflib.URIRef using the supplied namespace

    The internal id is sanitised (slugified).

    Args:
        internal_id: ID to add to the namespace.
        namespace: Namespace for the uri.

    Returns:
        rdflib.URIRef: Generated URI for internal usage.
    """
    # Slugify
    # We split and re-join on the `/`, as forward-slashes are valid for our
    # internal URIs, but python-slugify removes them. This is the recommended
    # way to keep the slashes as per python-slugify GitHub issues.
    internal_id = "/".join(slugify_for_uri(part) for part in internal_id.split("/"))

    # Create URIRef and Return
    return namespace[internal_id]


def slugify_for_uri(string: str, /) -> str:
    """The standard way to slugify a string for use in an RDF URI.

    Slugify-ing is used when readability is more important than preserving the exact value.
    """
    return slugify.slugify(string, lowercase=False)


def uri_quoted(
    namespace: rdflib.Namespace,
    path: str,
    /,
    **kwargs: str,
) -> rdflib.URIRef:
    """Generates a rdflib.URIRef using the supplied namespace and path.

    The path string can contain fields to be replaced in braces, e.g "survey/{survey_id}"
    These fields are replaced by the contents of kwargs.
    Each kwarg value is sanitised by being url-quoted before being inserted in the path.
    Then the resulting path is then appended to the namespace to get the URI.

    Some examples:
    >>> uri_quoted(namespaces.EXAMPLE, "someField/{the_value}", the_value="foo")
    rdflib.URIRef("http://example.com/someField/foo")
    >>> uri_quoted(namespaces.EXAMPLE, "Type/{field}/{value}", field="foo", value="Hello There!")
    rdflib.URIRef("http://example.com/Type/foo/Hello%20There%21")

    url-quoting is used instead of slugify-ing;
        1. So that the exact original value can be determined from the URI.
           This is not possible with slugify-ing which will remove or replace chars with "-".
        2. Different input values always result in different final URIs.
           This is not always the case with slugify-ing, since chars can be dropped or replaced with "-".

    Args:
        namespace: Namespace for the uri.
        path: Path to append to the namespace.
            Can contain fields to be replaced, e.g. "survey/{survey_id}".
        kwargs: Fields and values to replace in the path string.

    Returns:
        Generated URI.
    Raises:
        KeyError: When the path string contains a field not specified in kwargs.
    """
    # fill in any {field} names in path with url-quoted kwargs.
    path = path.format_map({field: urllib.parse.quote(value, safe="") for field, value in kwargs.items()})

    # Create URIRef and Return
    return namespace[path]


def uri_or_string_literal(raw: str) -> rdflib.Literal:
    """Determines if supplied string is an uri or a string literal.

    Args:
        raw (str): Raw value to be converted.

    Returns:
        rdflib.Literal: With datatype xsd:anyURI for uri else xsd:string
    """
    # Parse the incoming string
    parsed_url = urllib.parse.urlparse(raw)

    # A valid url will have a host and protocol
    if parsed_url.scheme and parsed_url.netloc:
        return rdflib.Literal(raw, datatype=rdflib.XSD.anyURI)

    return rdflib.Literal(raw)
