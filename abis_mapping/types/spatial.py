"""Provides geometry related utilities."""

# Standard
import decimal
import functools
import re

# Third-party
import shapely
import shapely.ops
import numpy as np
import pyproj
import rdflib

# Local
from abis_mapping import settings
from abis_mapping.utils import namespaces
from abis_mapping import utils

# Typing
from typing import NamedTuple


# Create cached lookup functions for pyproj.CRS and pyproj.Transformer objects,
# to avoid the cost of repeatedly creating them when mapping.
_CRS_cached = functools.cache(pyproj.CRS)
_transformer_from_crs_cached = functools.cache(pyproj.Transformer.from_crs)


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

        All internal geometries are created and stored in long-lat format
        until geosparql wkt string representations are made which will
        produce lat-long representations of coordinates if a datum is
        provided.

        Args:
            raw (LatLong | str | shapely.Geometry): Input geometry
            datum (str | None): Geodetic datum corresponding to input. Datum is assumed
                to be a lat-long coordinate system. This class should not be used
                for long-lat datums.

        Raises:
            TypeError: If unsupported type for raw supplied.
            GeometryError: If failure occurs with transforming using underlying libraries.
        """
        # Determine type of argument supplied and process.
        if isinstance(raw, LatLong):
            # Make shapely point
            self._geometry: shapely.Geometry = shapely.Point(raw.longitude, raw.latitude)
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
            self._crs = _CRS_cached(datum)

            # Create a default CRS transformer
            self._transformer = _transformer_from_crs_cached(
                crs_from=datum,
                crs_to=settings.SETTINGS.DEFAULT_TARGET_CRS,
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
            rdflib.URIRef: Uri corresponding to original datum.

        Raises:
            GeometryError: If the original datum name is not part
                of the GEODETIC_DATUM fixed vocab.
        """
        # Retrieve vocab class
        vocab = utils.vocabs.get_vocab("GEODETIC_DATUM")
        try:
            # Init with dummy graph and return corresponding URI
            return vocab(graph=rdflib.Graph()).get(self.original_datum_name)
        except utils.vocabs.VocabularyError as exc:
            raise GeometryError(
                f"CRS {self.original_datum_name} is " "not defined for the GEODETIC_DATUM fixed vocabulary."
            ) from exc

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
            rdflib.URIRef: Uri corresponding to transformer datum.

        Raises:
            GeometryError: If the project default CRS is not a part
                of the GEODETIC_DATUM fixed vocab.
        """
        # Retrieve vocab class
        vocab = utils.vocabs.get_vocab("GEODETIC_DATUM")
        default_crs = settings.Settings().DEFAULT_TARGET_CRS

        try:
            # Init with dummy graph and return corresponding uri
            return vocab(graph=rdflib.Graph()).get(default_crs)
        except utils.vocabs.VocabularyError as exc:
            raise GeometryError(
                f"Default CRS {default_crs} is " "not defined for the GEODETIC_DATUM fixed vocabulary."
            ) from exc

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
            # NOTE 11/11/2024 @jcrowleygaia: It is currently pretty impossible for a non-match to occur
            # however it may be necessary to keep this check in case of a change to the above
            # compiled regex in the future.
            raise ValueError(f"supplied literal '{literal}' is not GeoSPARQL WKT format.")

        # Attempt to make shapely geometry and catch errors
        try:
            raw = shapely.from_wkt(match.group(2))
        except shapely.errors.ShapelyError as exc:
            raise GeometryError from exc

        # Check to see if datum provided
        if datum := match.group(1):
            # Flip the coordinates from lat-long to long-lat
            # NOTE: Assumption is that the datum provided is of lat-long orientation.
            raw = _swap_coordinates(raw)

        # Create and return Geometry object
        return Geometry(
            raw=raw,
            datum=datum or "WGS84",
        )

    def to_rdf_literal(self) -> rdflib.Literal:
        """Generates a literal WKT representation of the supplied geometry.

        Returns:
            rdflib.Literal: RDF WKT literal for geometry.
        """
        # Construct Datum URI to be Embedded
        datum_string = f"<{self.original_datum_uri}> " if self.original_datum_uri is not None else ""

        # Manipulate geometry coordinates to suit datum string as per geosparql
        # literal requirements. NOTE: It is assumed all geodetic datums supplied are of
        # the lat-long orientation and not the default WKT representation of long-lat.
        geometry = _swap_coordinates(self._geometry) if datum_string else self._geometry

        # Construct  and return rdf literal
        wkt_string = shapely.to_wkt(
            geometry=geometry,
            rounding_precision=settings.Settings().DEFAULT_WKT_ROUNDING_PRECISION,
        )

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

        # Manipulate geometry coordinates to suit datum string as per geosparql
        # literal requirements. NOTE: It is assumed all geodetic datums supplied are of
        # the lat-long orientation and not the default WKT representation of long-lat.
        geometry = _swap_coordinates(self._transformed_geometry) if datum_string else self._transformed_geometry

        # Construct and return rdf literal
        wkt_string = shapely.to_wkt(
            geometry=geometry,
            rounding_precision=settings.Settings().DEFAULT_WKT_ROUNDING_PRECISION,
        )
        return rdflib.Literal(
            lexical_or_value=datum_string + wkt_string,
            datatype=namespaces.GEO.wktLiteral,
        )


def _swap_coordinates(original: shapely.Geometry) -> shapely.Geometry:
    """Swaps x,y coordinates to y,x.

    Args:
        original (shapely.Geometry): Original geometry
            with coords (x, y)

    Returns:
        shapely.Geometry: All coords now (y, x)

    Raises:
        GeometryError: If supplied original geometry is not
            2 dimensional.
    """
    # Check original is 2D
    if shapely.get_coordinate_dimension(original) != 2:
        raise GeometryError("Coordinate swapping is only supported for 2D geometries.")

    # Perform flip on coords
    txd = shapely.transform(original, np.fliplr)

    # Return transformed geometry
    return txd


class GeometryError(BaseException):
    """Exception class for the geometry type."""

    pass
