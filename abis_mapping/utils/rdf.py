"""Provides rdf utilities for the package"""


# Standard
import datetime
import uuid

# Third-Party
import rdflib
import slugify
import shapely

# Local
from . import namespaces
from . import types
from abis_mapping import settings

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


def inXSDSmart(timestamp: types.DateOrDatetime) -> rdflib.URIRef:
    """Generates the correct TIME.inXSD<xxx> predicate for date or datetime.

    Args:
        timestamp (types.DateOrDateTime): Timestamp to generate a
            time:inXSD<Date/DateTime/DateTimeStamp> predicate for.

    Returns:
        rdflib.URIRef: The smartly generated predicate.
    """
    # Check for Datetime with Time Zone
    if isinstance(timestamp, datetime.datetime) and timestamp.tzinfo is not None:
        # inXSDDateTimeStamp
        predicate = rdflib.TIME.inXSDDateTimeStamp

    # Check for Datetime without Time Zone
    elif isinstance(timestamp, datetime.datetime):
        # inXSDDateTime
        predicate = rdflib.TIME.inXSDDateTime

    # Just Date
    else:
        # inXSDDate
        predicate = rdflib.TIME.inXSDDate

    # Return
    return predicate


def toTimestamp(timestamp: types.DateOrDatetime) -> rdflib.Literal:
    """Generates the correct rdflib.Literal for date or datetime.

    Args:
        timestamp (types.DateOrDateTime): Timestamp to generate a
            rdflib.Literal for.

    Returns:
        rdflib.Literal: The smartly generated literal.
    """
    # Check for Datetime with Time Zone
    if isinstance(timestamp, datetime.datetime) and timestamp.tzinfo is not None:
        # xsd:dateTimeStamp
        literal = rdflib.Literal(timestamp, datatype=rdflib.XSD.dateTimeStamp)

    # Check for Datetime without Time Zone
    elif isinstance(timestamp, datetime.datetime):
        # xsd:dateTime
        literal = rdflib.Literal(timestamp, datatype=rdflib.XSD.dateTime)

    # Just Date
    else:
        # xsd:date
        literal = rdflib.Literal(timestamp, datatype=rdflib.XSD.date)

    # Return
    return literal


def to_wkt_point_literal(
    latitude: float,
    longitude: float,
    datum: Optional[rdflib.URIRef] = None,
) -> rdflib.Literal:
    """Generates a Literal WKT Point Representation of Latitude and Longitude.

    Args:
        latitude (float): Latitude to generate WKT.
        longitude (float): Longitude to generate WKT.
        datum (Optional[rdflib.URIRef]): Optional geodetic datum to include.

    Returns:
        rdflib.Literal: Literal WKT Point.
    """
    # Construct point from latitude and longitude
    point = shapely.Point(longitude, latitude)

    # Create and Return WKT rdf literal
    return to_wkt_literal(point, datum)


def to_wkt_literal(
    geometry: shapely.Geometry,
    datum: Optional[rdflib.URIRef] = None,
) -> rdflib.Literal:
    """Generates a literal WKT representation of the supplied geometry.

    Args:
        geometry (shapely.Geometry): Geometry object to construct WKT text from.
        datum (Optional[rdflib.URIRef]): Geodetic datum that geometry is based
            upon.

    Returns:
        rdflib.Literal: RDF WKT literal for geometry
    """
    # Construct Datum URI to be Embedded
    datum_string = f"<{datum}> " if datum else ""

    # Construct  and return rdf literal
    wkt_string = shapely.to_wkt(geometry, rounding_precision=settings.DEFAULT_WKT_ROUNDING_PRECISION)
    return rdflib.Literal(
        datum_string + wkt_string,
        datatype=namespaces.GEO.wktLiteral,
    )
