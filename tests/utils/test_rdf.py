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

    # Check Graph
    assert isinstance(graph, rdflib.Graph)
    assert len(list(graph.namespaces())) == 31


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
    # Test Date
    date = datetime.date.today()
    predicate = utils.rdf.inXSDSmart(date)
    assert predicate == rdflib.TIME.inXSDDate

    # Test Datetime
    time = datetime.datetime.now()
    predicate = utils.rdf.inXSDSmart(time)
    assert predicate == rdflib.TIME.inXSDDateTimeStamp


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
