"""Provides utilities for the package"""


# Standard
import uuid

# Third-Party
import pandas as pd
import rdflib
import slugify

# Local
from . import base

# Typing
from typing import Optional


# Constants
GEO = rdflib.Namespace("http://www.opengis.net/ont/geosparql#")
TERN = rdflib.Namespace("https://w3id.org/tern/ontologies/tern/")
DWC = rdflib.Namespace("http://rs.tdwg.org/dwc/terms/")
EXAMPLE = rdflib.Namespace("http://example.org/")


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
    graph.bind("geo", GEO)
    graph.bind("tern", TERN)
    graph.bind("dwc", DWC)
    graph.bind("ex", EXAMPLE)

    # Return
    return graph


def uri(
    internal_id: Optional[str] = None,
    namespace: rdflib.Namespace = EXAMPLE,
    ) -> rdflib.URIRef:
    """Generates an rdflib.URIRef using the EXAMPLE namespace

    The internal id is sanitised (slugified), or if not a provided a uuidv4 is
    generated instead.

    Args:
        internal_id (Optional[str]): Optional human readable id

    Returns:
        rdflib.URIRef: Generated URI for internal usage.
    """
    # Check for Internal ID
    if internal_id is None:
        # Generate a UUID
        internal_id = str(uuid.uuid4())

    # Slugify
    # We split and re-join on the `/`, as forward-slashes are valid for our
    # internal URIs, but python-slugify removes them. This is the recommended
    # way to keep the slashes as per python-slugify GitHub issues.
    internal_id = "/".join(slugify.slugify(part, lowercase=False) for part in internal_id.split("/"))

    # Create URIRef and Return
    return namespace[internal_id]


def read_csv(data: base.CSVType) -> pd.DataFrame:
    """Reads raw csv data into a pandas DataFrame

    Args:
        data (CSVType): Pandas readable CSV type.
            i.e., `FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]`.
            See: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

    Returns:
        pd.DataFrame: Pandas DataFrame containing CSV data.
    """
    # Read CSV and Return
    return pd.read_csv(data, keep_default_na=False)
