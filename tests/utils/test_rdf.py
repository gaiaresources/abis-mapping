"""Provides Unit Tests for the `abis_mapping.utils.rdf` module"""


# Third-Party
import rdflib
import shapely

import abis_mapping.utils.geometry
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


def test_rdf_to_wkt_point_literal() -> None:
    """Tests the to_wkt_point_literal() Function."""
    # Test Lat and Long
    wkt = abis_mapping.utils.geometry.to_wkt_point_literal(
        latitude=-31.953512,
        longitude=115.857048,
    )
    assert wkt == rdflib.Literal(
        "POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Test Lat and Long with Datum
    wkt = abis_mapping.utils.geometry.to_wkt_point_literal(
        latitude=-31.953512,
        longitude=115.857048,
        datum=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4283"),
    )
    assert wkt == rdflib.Literal(
        "<http://www.opengis.net/def/crs/EPSG/9.9.1/4283> POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )


def test_rdf_to_wkt_literal() -> None:
    """Tests the to_wkt_literal() Function"""
    # Create shapely geometry
    point = shapely.Point(115.857048, -31.953512)

    # Test only geometry
    wkt = abis_mapping.utils.geometry.to_wkt_literal(point)
    assert wkt == rdflib.Literal(
        "POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Test with Datum
    wkt = abis_mapping.utils.geometry.to_wkt_literal(
        geometry=point,
        datum=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4283"),
    )
    assert wkt == rdflib.Literal(
        "<http://www.opengis.net/def/crs/EPSG/9.9.1/4283> POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Check rounding
    point = shapely.Point(115.8570481111111, -31.95351254545)

    # Test only geometry rounds correctly
    wkt = abis_mapping.utils.geometry.to_wkt_literal(point)
    assert wkt == rdflib.Literal(
        "POINT (115.85704811 -31.95351255)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )
