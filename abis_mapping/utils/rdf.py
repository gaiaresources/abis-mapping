"""Provides rdf utilities for the package"""


# Standard
import uuid

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


