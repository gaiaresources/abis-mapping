"""Provides unit tests for the geometry module."""

# Third-party
import shapely
import pytest
import rdflib

# Local
from abis_mapping import settings
from abis_mapping import types
from abis_mapping import utils
from abis_mapping import vocabs

# Typing
from typing import Type


def test_geometry_init_wkt_string_valid() -> None:
    """Tests the creation of a Geometry object from a WKT string."""
    # Create geometry
    geometry = types.spatial.Geometry(
        raw="POINT(1 1)",
        datum="WGS84",
    )

    # Assert geometry created
    assert geometry is not None


def test_geometry_init_shapely_geometry() -> None:
    """Tests the creation of a Geometry object from a shapely geometry."""
    # Create input shapely geometry
    s_geom = shapely.Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))

    # Create geometry
    geometry = types.spatial.Geometry(raw=s_geom, datum="WGS84")

    # Assert geometry created
    assert geometry is not None


def test_geometry_init_latlong() -> None:
    """Tests the creation of a Geometry object from a LatLong."""
    # Create latlong
    lat_long = types.spatial.LatLong(0, 0)

    # Create geometry
    geometry = types.spatial.Geometry(
        raw=lat_long,
        datum="WGS84",
    )

    # Assert geometry created
    assert geometry is not None


def test_geometry_init_type_invalid() -> None:
    """Tests that Geometry object raises TypeError on invalid types."""
    with pytest.raises(TypeError):
        types.spatial.Geometry(raw=123, datum="WGS84")


def test_geometry_init_wkt_string_invalid() -> None:
    """Tests that Geometry object raises error on invalid WKT string."""
    with pytest.raises(types.spatial.GeometryError):
        types.spatial.Geometry(
            raw="not wkt",
            datum="WGS84",
        )


def test_geometry_init_datum_invalid() -> None:
    """Tests that Geometry raises error on invalid datum."""
    with pytest.raises(types.spatial.GeometryError):
        types.spatial.Geometry(raw="POINT(0 0)", datum="NOTADATUM000")


@pytest.mark.parametrize(
    "datum_in, datum_out",
    [
        ("WGS84", "WGS84"),
        ("http://www.opengis.net/def/crs/EPSG/0/7844", "GDA2020"),
        ("wgs 84", "WGS84"),
    ],
)
def test_geometry_original_datum_name(datum_in: str, datum_out: str) -> None:
    """Tests the original_datum_name property."""
    geometry = types.spatial.Geometry(
        raw="POINT(0 0)",
        datum=datum_in,
    )

    assert geometry.original_datum_name == datum_out


@pytest.mark.parametrize(
    "datum, uri",
    [
        ("WGS84", "http://www.opengis.net/def/crs/EPSG/0/4326"),
    ],
)
def test_geometry_original_datum_uri(datum: str, uri: str) -> None:
    """Tests the original_datum_uri property."""
    # Create geometry
    geometry = types.spatial.Geometry(
        raw="POINT(0 0)",
        datum="WGS84",
    )

    # Create expected output
    expected = rdflib.URIRef(uri)

    # Assert
    assert geometry.original_datum_uri == expected


def test_geometry_transformer_datum_uri() -> None:
    """Tests the transformer_datum_uri property."""
    # Create geometry
    geometry = types.spatial.Geometry(
        raw="POINT(0 0)",
        datum="AGD66",
    )
    # Retrieve geodetic datum vocab
    vocab = utils.vocabs.get_vocab("GEODETIC_DATUM")

    # Assert default datum
    assert vocab is not None
    assert geometry.transformer_datum_uri == vocab(graph=rdflib.Graph()).get(settings.Settings().DEFAULT_TARGET_CRS)


@pytest.mark.parametrize(
    "literal_in, expected_name",
    [
        ("<http://www.opengis.net/def/crs/EPSG/0/7844> POINT(0 0)", "GDA2020"),
        ("POINT(0 0)", "WGS84"),
        (
            rdflib.Literal(
                lexical_or_value="<http://www.opengis.net/def/crs/EPSG/0/4326> POINT(0 0)",
                datatype=utils.namespaces.GEO.wktLiteral,
            ),
            "WGS84",
        ),
    ],
)
def test_geometry_from_geosparql_wkt_literal_valid(
    literal_in: str | rdflib.Literal,
    expected_name: str,
) -> None:
    """Tests the geometry from_geosparql_wkt_literal method."""
    # Create geometry
    geometry = types.spatial.Geometry.from_geosparql_wkt_literal(literal_in)

    # Assert
    assert geometry.original_datum_name == expected_name


@pytest.mark.parametrize(
    "literal_in, expected_error",
    [
        ("<http://www.opengis.net/def/crs/EPSG/0/NOTADATUM> POINT(0 0)", types.spatial.GeometryError),
        ("<http://www.opengis.net/def/crs/EPSG/0/7844> NOTAGEOMETRY(0 0)", types.spatial.GeometryError),
    ],
)
def test_geometry_from_geosparql_wkt_literal_invalid(
    literal_in: str | rdflib.Literal,
    expected_error: Type[Exception],
) -> None:
    """Tests the geometry from_geosparql_wkt_literal method."""
    with pytest.raises(expected_error):
        types.spatial.Geometry.from_geosparql_wkt_literal(literal_in)


def test_geometry_to_rdf_literal() -> None:
    """Tests the Geometry to_rdf_literal method."""
    # Create geometry
    geometry = types.spatial.Geometry(raw=types.spatial.LatLong(0, 0), datum="GDA2020")

    # Expected output
    expected = rdflib.Literal(
        "<http://www.opengis.net/def/crs/EPSG/0/7844> POINT (0 0)",
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Assert
    assert geometry.to_rdf_literal() == expected


@pytest.mark.parametrize(
    "raw,datum,expected_str",
    [
        (
            "POINT (571666.4475041276 5539109.815175673)",
            "EPSG:26917",
            f"<{vocabs.geodetic_datum.GeodeticDatum(rdflib.Graph()).get(settings.Settings().DEFAULT_TARGET_CRS)}> POINT (-80 50)",  # noqa: E501
        ),
    ],
)
def test_geometry_to_tranformed_crs_rdf_literal(raw: str, datum: str, expected_str: str) -> None:
    """Tests the Geometry to_transformed_crs_rdf_literal method."""
    # Create geometry
    geometry = types.spatial.Geometry(
        raw=raw,
        datum=datum,
    )

    # Expected output
    expected = rdflib.Literal(
        lexical_or_value=expected_str,
        datatype=utils.namespaces.GEO.wktLiteral,
    )

    # Assert
    assert geometry.to_transformed_crs_rdf_literal() == expected
