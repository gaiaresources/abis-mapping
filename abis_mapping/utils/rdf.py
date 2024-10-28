"""Provides rdf utilities for the package"""

# Standard
import uuid
import urllib.parse

# Third-Party
import rdflib
import slugify

# Local
from . import namespaces

# Typing
from typing import Optional

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
    internal_id: Optional[str] = None,
    namespace: Optional[rdflib.Namespace] = None,
) -> rdflib.URIRef:
    """Generates an rdflib.URIRef using the supplied namespace

    The internal id is sanitised (slugified), or if not a provided a uuidv4 is
    generated instead.

    Args:
        internal_id (Optional[str]): Optional human readable id.
        namespace (Optional[rdflib.Namespace]): Optional namespace for the uri.

    Returns:
        rdflib.URIRef: Generated URI for internal usage.
    """
    # Check for Internal ID
    if internal_id is None:
        # Generate a UUID
        internal_id = str(uuid.uuid4())

    # Check for namespace
    if namespace is None:
        # Set Default Namespace
        namespace = namespaces.CREATEME

    # Slugify
    # We split and re-join on the `/`, as forward-slashes are valid for our
    # internal URIs, but python-slugify removes them. This is the recommended
    # way to keep the slashes as per python-slugify GitHub issues.
    internal_id = "/".join(slugify.slugify(part, lowercase=False) for part in internal_id.split("/"))

    # Create URIRef and Return
    return namespace[internal_id]


def extend_uri(
    base: rdflib.URIRef,
    *parts: str,
) -> rdflib.URIRef:
    """Extends the base URI with the provided extensions separated by /

    >>> extend_uri(rdflib.URIRef("https://example.com/foo"), "bar", "Some value")
    >>> rdflib.URIRef("https://example.com/foo/bar/Some-value")

    Args:
        base: Base uri
        *parts: URl parts to add to the base uri. Will be slugified.

    Returns:
        Extended URI
    """
    # slugify each part of the extension and join with /
    extension = "/".join(slugify.slugify(part, lowercase=False) for part in parts)
    joiner = "" if base[-1] == "/" else "/"
    return base + joiner + extension


def extend_uri_quoted(
    base: rdflib.URIRef,
    *parts: str,
) -> rdflib.URIRef:
    """Extends the base URI with the result of url-quoting the provided extension.

    >>> extend_uri(rdflib.URIRef("https://example.com/foo"), "bar", "Some value")
    >>> rdflib.URIRef("https://example.com/foo/bar/Some%20value")

    Each extension part is url-quoted to ensure no url-unsafe chars are included in the final URI.
    url-quoting is used instead of slugifying;
        1. So that the exact original value can be determined from the URI.
           This is not possible with slugifying which will remove or replace chars with "-".
        2. Different input values always result in different final URIs.
           This is not always the case with slugifying, since chars can be dropped or replaced with "-".

    Args:
        base: Base uri
        *parts: URl parts to add to the base uri. Will be url-quoted.

    Returns:
        Extended URI
    """
    # url-quote each part of the extension and join with /
    extension = "/".join(urllib.parse.quote(part, safe="") for part in parts)
    joiner = "" if base[-1] == "/" else "/"
    return base + joiner + extension


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
