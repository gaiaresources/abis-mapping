"""Provides rdf utilities for the package"""


# Standard
import datetime
import uuid

# Third-Party
import rdflib
import slugify
import shapely
import frictionless.fields
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


def inXSDSmart(timestamp: types.Timestamp) -> rdflib.URIRef:
    """Generates the correct TIME.inXSD<xxx> predicate for date or datetime.

    Args:
        timestamp (types.DateOrDateTime): Timestamp to generate a
            time:inXSD<Date/DateTime/DateTimeStamp> predicate for.

    Returns:
        rdflib.URIRef: The smartly generated predicate.

    Raises:
        TypeError: If the timestamp does not match one of the types.Timestamp types
    """
    # Check for Datetime with Time Zone
    if isinstance(timestamp, datetime.datetime) and timestamp.tzinfo is not None:
        # inXSDDateTimeStamp
        return rdflib.TIME.inXSDDateTimeStamp

    # Check for Datetime without Time Zone
    if isinstance(timestamp, datetime.datetime):
        # inXSDDateTime
        return rdflib.TIME.inXSDDateTime

    # Check Date
    if isinstance(timestamp, datetime.date):
        # inXSDDate
        return rdflib.TIME.inXSDDate

    # Check yearmonth
    if isinstance(timestamp, frictionless.fields.yearmonth.yearmonth):
        # inXSDgYearMonth
        return rdflib.TIME.inXSDgYearMonth

    # Check year
    if isinstance(timestamp, int):
        # inXSDgYear
        return rdflib.TIME.inXSDgYear

    # Shouldn't reach here if argument type annotations adhered to
    raise TypeError(f"expected one of {types.Timestamp}; got {type(timestamp)}.")


def to_timestamp(timestamp: types.Timestamp) -> rdflib.Literal:
    """Generates the correct rdflib.Literal for timestamp.

    The string that is chosen for the timestamp value will be derived from the optional
    supplied field, otherwise will revert to the default repr for the type.

    Args:
        timestamp (types.Timestamp): Timestamp to generate a
            rdflib.Literal for.

    Returns:
        rdflib.Literal: The smartly generated literal.

    Raises:
        TypeError: If the timestamp does not match one of the types.Timestamp types
    """
    # Check for Datetime with Time Zone
    if isinstance(timestamp, datetime.datetime) and timestamp.tzinfo is not None:
        # xsd:dateTimeStamp
        datatype = rdflib.XSD.dateTimeStamp

    # Check for Datetime without Time Zone
    elif isinstance(timestamp, datetime.datetime):
        # xsd:dateTime
        datatype = rdflib.XSD.dateTime

    # Check for Date
    elif isinstance(timestamp, datetime.date):
        # xsd:date
        datatype = rdflib.XSD.date

    # Check for YearMonth
    elif isinstance(timestamp, frictionless.fields.yearmonth.yearmonth):
        # xsd:gYearMonth
        datatype = rdflib.XSD.gYearMonth

    # Check for Year
    elif isinstance(timestamp, int):
        # xsd:gYear
        datatype = rdflib.XSD.gYear

    else:
        # Shouldn't reach here if argument type annotations adhered to
        raise TypeError(f"expected one of {types.Timestamp}; got {type(timestamp)}.")

    # Construct a timestamp field
    field = frictionless.Field.from_descriptor({"name": "tempField", "type": "timestamp"})

    # Use the cell writer method for the field to create the string
    return rdflib.Literal(field.write_cell(timestamp)[0], datatype=datatype)


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
