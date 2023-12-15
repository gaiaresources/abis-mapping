"""Provides Unit Tests for the `abis_mapping.utils.rdf` module"""


# Standard
import datetime

# Third-Party
import rdflib
import shapely
import pytest
import frictionless.fields

# Local
from abis_mapping import utils
from abis_mapping.utils import types


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


@pytest.mark.parametrize(
    "time,expected",
    [
        # Test Datetime with Timezone
        (datetime.datetime.now().astimezone(datetime.timezone.utc), rdflib.TIME.inXSDDateTimeStamp),
        # Test Datetime without Timezone
        (datetime.datetime.now(), rdflib.TIME.inXSDDateTime),
        # Test Date
        (datetime.date.today(), rdflib.TIME.inXSDDate),
        # Test Yearmonth
        (frictionless.fields.yearmonth.yearmonth(year=2022, month=12), rdflib.TIME.inXSDgYearMonth),
        # Test Year
        (2022, rdflib.TIME.inXSDgYear),
    ]
)
def test_rdf_inXSDSmart(time: types.Timestamp, expected: rdflib.URIRef) -> None:
    """Tests the inXSDSmart() Function

    Args:
        time (types.Timestamp): input timestamp.
        expected (rdflib.URIRef): expected output.
    """
    # Call function and assert
    predicate = utils.rdf.inXSDSmart(time)
    assert predicate == expected


def test_rdf_inXSDSmart_invalid() -> None:
    """Tests the inXSDSmart() function raises exception on invalid type arg."""
    # Call should raise TypeError
    with pytest.raises(TypeError):
        utils.rdf.inXSDSmart(None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "time,expected_datatype",
    [
        # Test Datetime with Timezone
        (datetime.datetime.now().astimezone(datetime.timezone.utc), rdflib.XSD.dateTimeStamp),
        # Test Datetime without Timezone
        (datetime.datetime.now(), rdflib.XSD.dateTime),
        # Test Date
        (datetime.date.today(), rdflib.XSD.date),
        # Test Year month
        (frictionless.fields.yearmonth.yearmonth(year=2022, month=4), rdflib.XSD.gYearMonth),
        # Test year only
        (2022, rdflib.XSD.gYear)
    ]
)
def test_rdf_to_timestamp(time: types.Timestamp, expected_datatype: rdflib.Literal) -> None:
    """Tests the to_timestamp() Function."""
    # Test Datetime with Timezone
    literal = utils.rdf.to_timestamp(time)

    # Construct dummy field
    field: frictionless.Field = frictionless.Field.from_descriptor({"name": "testField", "type": "timestamp"})

    # Use field to output string and assert
    assert literal == rdflib.Literal(field.write_cell(time)[0], datatype=expected_datatype)


def test_rdf_to_timestamp_invalid() -> None:
    """Tests the to_timestamp() function raises exception on invalid arg type."""
    with pytest.raises(TypeError):
        utils.rdf.to_timestamp(None)  # type: ignore[arg-type]


def test_rdf_to_wkt_point_literal() -> None:
    """Tests the to_wkt_point_literal() Function."""
    # Test Lat and Long
    wkt = utils.rdf.to_wkt_point_literal(
        latitude=-31.953512,
        longitude=115.857048,
    )
    assert wkt == rdflib.Literal(
        "POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Test Lat and Long with Datum
    wkt = utils.rdf.to_wkt_point_literal(
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
    wkt = utils.rdf.to_wkt_literal(point)
    assert wkt == rdflib.Literal(
        "POINT (115.857048 -31.953512)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Test with Datum
    wkt = utils.rdf.to_wkt_literal(
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
    wkt = utils.rdf.to_wkt_literal(point)
    assert wkt == rdflib.Literal(
        "POINT (115.85704811 -31.95351255)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )
