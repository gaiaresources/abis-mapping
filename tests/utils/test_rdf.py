"""Provides Unit Tests for the `abis_mapping.utils.rdf` module"""


# Standard
import datetime

# Third-Party
import rdflib

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
    required_namespaces = [(name, rdflib.term.URIRef(uri)) for (name, uri) in utils.rdf.REQUIRED_NAMESPACES]
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


def test_rdf_inXSDSmart() -> None:
    """Tests the inXSDSmart() Function"""
    # Test Datetime with Timezone
    time = datetime.datetime.now().astimezone(datetime.timezone.utc)
    predicate = utils.rdf.inXSDSmart(time)
    assert predicate == rdflib.TIME.inXSDDateTimeStamp

    # Test Datetime without Timezone
    time = datetime.datetime.now()
    predicate = utils.rdf.inXSDSmart(time)
    assert predicate == rdflib.TIME.inXSDDateTime

    # Test Date
    date = datetime.date.today()
    predicate = utils.rdf.inXSDSmart(date)
    assert predicate == rdflib.TIME.inXSDDate


def test_rdf_toTimestamp() -> None:
    """Tests the toTimestamp() Function"""
    # Test Datetime with Timezone
    time = datetime.datetime.now().astimezone(datetime.timezone.utc)
    literal = utils.rdf.toTimestamp(time)
    assert literal == rdflib.Literal(time, datatype=rdflib.XSD.dateTimeStamp)

    # Test Datetime without Timezone
    time = datetime.datetime.now()
    literal = utils.rdf.toTimestamp(time)
    assert literal == rdflib.Literal(time, datatype=rdflib.XSD.dateTime)

    # Test Date
    date = datetime.date.today()
    literal = utils.rdf.toTimestamp(date)
    assert literal == rdflib.Literal(date, datatype=rdflib.XSD.date)


def test_rdf_toWKT() -> None:
    """Tests the toWKT() Function"""
    # Test Lat and Long
    wkt = utils.rdf.toWKT(
        latitude=-31.953512,
        longitude=115.857048,
    )
    assert wkt == rdflib.Literal(
        "POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Test Lat and Long with Datum
    wkt = utils.rdf.toWKT(
        latitude=-31.953512,
        longitude=115.857048,
        datum=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4283"),
    )
    assert wkt == rdflib.Literal(
        "<http://www.opengis.net/def/crs/EPSG/9.9.1/4283> POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )
