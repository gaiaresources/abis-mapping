"""Provides geometry related utilities."""

# Standard
import decimal
import re

# Third-party
import shapely
import shapely.ops
import pyproj
import rdflib

# Local
from abis_mapping import settings
from abis_mapping.utils import namespaces
from abis_mapping import utils

# Typing
from typing import NamedTuple


class LatLong(NamedTuple):
    """Named tuple representing coordinates."""
    latitude: float | int | decimal.Decimal
    longitude: float | int | decimal.Decimal


class Geometry:
    """Class for all geographical coordinate transformations."""

    def __init__(
        self,
        raw: LatLong | str | shapely.Geometry,
        datum: str,
    ) -> None:
        """Constructor for a Geometry object.

        Args:
            raw (LatLong | str | shapely.Geometry): Input geometry
            datum (str | None): Geodetic datum corresponding to input.

        Raises:
            TypeError: If unsupported type for raw supplied.
            GeometryError: If failure occurs with transforming using underlying libraries.
        """
        # Determine type of argument supplied and process.
        if isinstance(raw, LatLong):
            # Attempt to make shapely geometry and catch errors
            try:
                self._geometry: shapely.Geometry = shapely.Point(raw.longitude, raw.latitude)
            except shapely.errors.ShapelyError as exc:
                raise GeometryError from exc
        elif isinstance(raw, str):
            # Attempt to make shapely geometry and catch errors
            try:
                self._geometry = shapely.from_wkt(raw)
            except shapely.errors.ShapelyError as exc:
                raise GeometryError from exc
        elif isinstance(raw, shapely.Geometry):
            self._geometry = raw
        else:
            raise TypeError(f"unsupported raw type '{type(raw)}'")

        # Attempt to create a converter using proj.
        try:
            # Will raise if geodetic datum not supported
            self._crs = pyproj.CRS(datum)

            # Create a default CRS transformer
            self._transformer = pyproj.Transformer.from_crs(
                crs_from=datum,
                crs_to=settings.DEFAULT_TARGET_CRS,
                always_xy=True,
            )
        except pyproj.ProjError as exc:
            # Reraise as a GeometryError.
            raise GeometryError from exc

    @property
    def original_datum_name(self) -> str:
        """Getter for the original datum provided."""
        return self._crs.name.replace(" ", "")

    @property
    def original_datum_uri(self) -> rdflib.URIRef | None:
        """Getter for the original datum URI.

        Returns:
            rdflib.URIRef: Uri corresponding to original datum if known, else None.
        """
        # Retrieve vocab class
        if (vocab := utils.vocabs.get_vocab("GEODETIC_DATUM")) is not None:
            # Init with dummy graph and return corresponding URI
            return vocab(graph=rdflib.Graph()).get(self.original_datum_name)
        else:
            return None

    @property
    def _transformed_geometry(self) -> shapely.Geometry:
        """Getter for the transformed geometry.

        Returns:
            shapely.Geometry: Transformed geometry
        """
        return shapely.ops.transform(
            func=self._transformer.transform,
            geom=self._geometry,
        )

    @property
    def transformer_datum_uri(self) -> rdflib.URIRef | None:
        """Getter for the transformed datum URI.

        Returns:
            rdflib.URIRef: Uri corresponding to transformer datum if known, else None.
        """
        # Retrieve vocab class
        if (vocab := utils.vocabs.get_vocab("GEODETIC_DATUM")) is not None:
            # Init with dummy graph and return corresponding uri
            return vocab(graph=rdflib.Graph()).get(settings.DEFAULT_TARGET_CRS)

        # If vocab doesn't exist
        return None

    @classmethod
    def from_geosparql_wkt_literal(cls, literal: rdflib.Literal | str) -> "Geometry":
        """Converts a geosparql wkt literal to a Geometry object.

        GeoSPARQL spec located at,
            https://opengeospatial.github.io/ogc-geosparql/geosparql11/spec.html

        Args:
            literal (rdflib.Literal | str): RDF literal to convert.

        Raises:
            ValueError: If the supplied literal does not match GeoSPARQL
                format
        """
        # Compile regex
        regex = re.compile(r"^(?:<(\S+)>)? ?(.*)$")

        # Perform match
        match = regex.match(str(literal))
        if match is None:
            raise ValueError(f"supplied literal '{literal}' is not GeoSPARQL WKT format.")

        # Create and return Geometry object
        return Geometry(
            raw=match.group(2),
            datum=match.group(1) or "WGS84"
        )

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
            lexical_or_value=datum_string + wkt_string,
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


class GeometryError(BaseException):
    """Exception class for the geometry type."""
    pass
