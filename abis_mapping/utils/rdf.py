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


def create_graph() -> rdflib.Graph:
    """Utility function that creates a base rdflib.Graph with the required
    namespaces bound with their expected prefix.

    Returns:
        rdflib.Graph: Graph with expected namespaces bound.
    """
    # Create Graph
    graph = rdflib.Graph()

    # Bind Namespaces
    graph.bind("rdf", rdflib.RDF)
    graph.bind("rdfs", rdflib.RDFS)
    graph.bind("void", rdflib.VOID)
    graph.bind("sosa", rdflib.SOSA)
    graph.bind("dcterms", rdflib.DCTERMS)
    graph.bind("prov", rdflib.PROV)
    graph.bind("time", rdflib.TIME)
    graph.bind("xsd", rdflib.XSD)
    graph.bind("sdo", rdflib.SDO)
    graph.bind("geo", namespaces.GEO)
    graph.bind("tern", namespaces.TERN)
    graph.bind("dwc", namespaces.DWC)

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
    return namespace[internal_id]  # type: ignore[no-any-return]
