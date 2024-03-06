"""Provides geometry related utilities."""

# Standard
import decimal
import functools

# Third-party
import shapely
import pyproj
import rdflib

# Local
from abis_mapping import settings
from abis_mapping.utils import namespaces
from abis_mapping import vocabs

# Typing
from typing import NamedTuple, Optional


class LatLong(NamedTuple):
    """Named tuple representing coordinates."""
    latitude: float | int | decimal.Decimal
    longitude: float | int | decimal.Decimal


class Geometry:
    """Class for all geographical coordinate transformations."""

    def __init__(
        self,
        raw: LatLong | str,
        geodetic_datum: str
    ):
        """Constructor for a Geometry object.

        Args:
            raw (LatLong | str):
            geodetic_datum (str | None):
        """
        if isinstance(raw, LatLong):
            self._geometry: shapely.Geometry = shapely.Point(raw.longitude, raw.latitude)
        else:
            self._geometry = shapely.from_wkt(raw)

        # Will raise if geodetic datum not supported
        self._crs = pyproj.CRS(geodetic_datum)

        # Create a default CRS transformer
        self._transformer = pyproj.Transformer.from_crs(
            crs_from=geodetic_datum,
            crs_to=settings.DEFAULT_TARGET_CRS,
            always_xy=True,
        )

        # Create transformed geometry
        self._transformed_geometry = shapely.transform(
            geometry=self._geometry,
            transformation=self._transformer.transform,
        )

    @property
    def original_datum(self) -> str:
        """Getter for the original datum provided."""
        return self._crs.name

    @property
    def original_datum_uri(self) -> rdflib.URIRef | None:
        """Getter for the original datum URI.

        Returns:
            rdflib.URIRef: Uri corresponding to original datum if known, else None.
        """
        return vocabs.geodetic_datum.GEODETIC_DATUM.get(self.original_datum)

    @property
    def transformer_datum_uri(self) -> rdflib.URIRef | None:
        """Getter for the transformed datum URI.

        Returns:
            rdflib.URIRef: Uri corresponding to transformer datum if known, else None.
        """
        return vocabs.geodetic_datum.GEODETIC_DATUM.get(settings.DEFAULT_TARGET_CRS)

    def to_rdf_literal(self) -> rdflib.Literal:
        """Generates a literal WKT representation of the supplied geometry.

        Returns:
            rdflib.Literal: RDF WKT literal for geometry.
        """
        # Construct Datum URI to be Embedded
        datum_string = f"<{self.original_datum_uri}> " if self.original_datum_uri is not None else ""

        # Construct  and return rdf literal
        wkt_string = shapely.to_wkt(self._geometry, rounding_precision=settings.DEFAULT_WKT_ROUNDING_PRECISION)
        return rdflib.Literal(
            datum_string + wkt_string,
            datatype=namespaces.GEO.wktLiteral,
        )

    def to_transformed_crs_rdf_literal(self) -> rdflib.Literal:
        """Generates a literal WKT representation converted to another CRS.

        Returns:
            rdflib.Literal: RDF WKT literal.
        """
        # Construct Datum URI to be embedded
        datum_string = f"<{self.transformer_datum_uri}> " if self.transformer_datum_uri is not None else ""

        # Construct and return rdf literal
        wkt_string = shapely.to_wkt(
            geometry=self._transformed_geometry,
            rounding_precision=settings.DEFAULT_WKT_ROUNDING_PRECISION
        )
        return rdflib.Literal(
            lexical_or_value=datum_string + wkt_string,
            datatype=namespaces.GEO.wktLiteral,
        )


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
