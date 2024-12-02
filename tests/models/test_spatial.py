"""Provides unit tests for the geometry module."""

# Standard
import copy

# Third-party
import shapely
import pytest
import rdflib

# Local
from abis_mapping import settings
from abis_mapping import models
from abis_mapping import utils
from abis_mapping import vocabs
from tests import helpers


def test_geometry_init_wkt_string_valid() -> None:
    """Tests the creation of a Geometry object from a WKT string."""
    # Create geometry
    geometry = models.spatial.Geometry(
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
    geometry = models.spatial.Geometry(raw=s_geom, datum="WGS84")

    # Assert geometry created
    assert geometry is not None


def test_geometry_init_latlong() -> None:
    """Tests the creation of a Geometry object from a LatLong."""
    # Create latlong
    lat_long = models.spatial.LatLong(0, 0)

    # Create geometry
    geometry = models.spatial.Geometry(
        raw=lat_long,
        datum="WGS84",
    )

    # Assert geometry created
    assert geometry is not None


def test_geometry_init_type_invalid() -> None:
    """Tests that Geometry object raises TypeError on invalid types."""
    with pytest.raises(TypeError):
        models.spatial.Geometry(raw=123, datum="WGS84")


def test_geometry_init_wkt_string_invalid() -> None:
    """Tests that Geometry object raises error on invalid WKT string."""
    with pytest.raises(models.spatial.GeometryError):
        models.spatial.Geometry(
            raw="not wkt",
            datum="WGS84",
        )


def test_geometry_init_datum_invalid() -> None:
    """Tests that Geometry raises error on invalid datum."""
    with pytest.raises(models.spatial.GeometryError):
        models.spatial.Geometry(raw="POINT(0 0)", datum="NOTADATUM000")


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
    geometry = models.spatial.Geometry(
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
    geometry = models.spatial.Geometry(
        raw="POINT(0 0)",
        datum=datum,
    )

    # Create expected output
    expected = rdflib.URIRef(uri)

    # Assert
    assert geometry.original_datum_uri == expected


def test_geometry_transformer_datum_uri() -> None:
    """Tests the transformer_datum_uri property."""
    # Create geometry
    geometry = models.spatial.Geometry(
        raw="POINT(0 0)",
        datum="AGD66",
    )
    # Retrieve geodetic datum vocab
    vocab = utils.vocabs.get_vocab("GEODETIC_DATUM")

    # Assert default datum
    assert vocab is not None
    assert geometry.transformer_datum_uri == vocab(graph=rdflib.Graph()).get(settings.SETTINGS.DEFAULT_TARGET_CRS)


def test_geometry_transformer_datum_uri_invalid() -> None:
    """Tests the transformer_datum_uri with unrecognised default crs."""
    # Create geometry
    geometry = models.spatial.Geometry(
        raw="POINT(0 0)",
        datum="OSGB36",
    )

    # Set temp default crs
    with helpers.override_settings(DEFAULT_TARGET_CRS="NOTADATUM"):
        # Should raise exception on invalid CRS not in fixed datum vocabulary
        with pytest.raises(models.spatial.GeometryError, match=r"NOTADATUM .+ GEODETIC_DATUM") as exc:
            _ = geometry.transformer_datum_uri

    # Should have been raised from VocabularyError
    assert exc.value.__cause__.__class__ is utils.vocabs.VocabularyError


def test_geometry_original_datum_uri_invalid() -> None:
    """Tests the transformer_datum_uri with unrecognised default crs."""
    # Create geometry
    geometry = models.spatial.Geometry(
        raw="POINT(0 0)",
        datum="OSGB36",
    )

    # Should raise exception on invalid CRS not in fixed datum vocabulary
    with pytest.raises(models.spatial.GeometryError, match=r"OSGB36 .+ GEODETIC_DATUM"):
        _ = geometry.original_datum_uri


@pytest.mark.parametrize(
    "literal_in, expected_name, expected_geometry",
    [
        ("<http://www.opengis.net/def/crs/EPSG/0/7844> POINT(1 2)", "GDA2020", shapely.Point(2, 1)),
        ("POINT(1 2)", "WGS84", shapely.Point(1, 2)),
        (
            rdflib.Literal(
                lexical_or_value="<http://www.opengis.net/def/crs/EPSG/0/4326> POINT(1 2)",
                datatype=utils.namespaces.GEO.wktLiteral,
            ),
            "WGS84",
            shapely.Point(2, 1),
        ),
    ],
)
def test_geometry_from_geosparql_wkt_literal_valid(
    literal_in: str | rdflib.Literal,
    expected_name: str,
    expected_geometry: shapely.Geometry,
) -> None:
    """Tests the geometry from_geosparql_wkt_literal method."""
    # Create geometry
    geometry = models.spatial.Geometry.from_geosparql_wkt_literal(literal_in)

    # Assert
    assert geometry.original_datum_name == expected_name
    assert geometry._geometry == expected_geometry


@pytest.mark.parametrize(
    "literal_in, expected_error",
    [
        ("<http://www.opengis.net/def/crs/EPSG/0/NOTADATUM> POINT(0 0)", models.spatial.GeometryError),
        ("<http://www.opengis.net/def/crs/EPSG/0/7844> NOTAGEOMETRY(0 0)", models.spatial.GeometryError),
    ],
)
def test_geometry_from_geosparql_wkt_literal_invalid(
    literal_in: str | rdflib.Literal,
    expected_error: type[Exception],
) -> None:
    """Tests the geometry from_geosparql_wkt_literal method."""
    with pytest.raises(expected_error):
        models.spatial.Geometry.from_geosparql_wkt_literal(literal_in)


def test_geometry_to_rdf_literal() -> None:
    """Tests the Geometry to_rdf_literal method."""
    # Create geometry
    geometry = models.spatial.Geometry(raw=models.spatial.LatLong(0, 0), datum="GDA2020")

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
            f"<{vocabs.geodetic_datum.GDA2020.iri}> POINT (50 -80)",
        ),
        (
            "LINESTRING (1 2, 3 4)",
            "WGS84",
            f"<{vocabs.geodetic_datum.GDA2020.iri}> LINESTRING (2 1, 4 3)",
        ),
    ],
)
def test_geometry_to_tranformed_crs_rdf_literal(raw: str, datum: str, expected_str: str) -> None:
    """Tests the Geometry to_transformed_crs_rdf_literal method."""
    # Create geometry
    geometry = models.spatial.Geometry(
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


@pytest.mark.parametrize(
    "geometry,expected",
    [
        (shapely.LineString([(2, 3), (3, 4)]), shapely.LineString([(3, 2), (4, 3)])),
        (shapely.Point(1, 2), shapely.Point(2, 1)),
        (
            shapely.Polygon([(1, 2), (2, 3), (1, 4), (0, 3), (1, 2)]),
            shapely.Polygon([(2, 1), (3, 2), (4, 1), (3, 0), (2, 1)]),
        ),
    ],
)
def test_swap_coordinates(geometry: shapely.Geometry, expected: shapely.Geometry) -> None:
    """Tests the _swap_coordinates module function.

    Args:
        geometry (shapely.Geometry): Input geometry to be transformed.
        expected (shapely.Geometry): Expected result.
    """
    # Copy original
    original = copy.deepcopy(geometry)

    # Invoke and assert
    assert models.spatial._swap_coordinates(geometry) == expected

    # Ensure no changing in place
    assert geometry == original


def test_swap_coordinates_3d() -> None:
    """Tests _swap_coordinates module function with 3d geometry supplied"""
    # Create geometry
    geometry = shapely.LineString([(2, 3, 4), (5, 6, 7)])

    # Should raise GeometryError
    with pytest.raises(models.spatial.GeometryError):
        models.spatial._swap_coordinates(geometry)
