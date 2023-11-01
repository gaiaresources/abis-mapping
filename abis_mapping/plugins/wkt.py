"""Provides custom frictionless wkt plugin for the package."""


# Third-party
import frictionless
import shapely

# Typing
from typing import Optional, Any, Type


class WKTPlugin(frictionless.Plugin):
    """Custom WKT plugin."""

    # Class attributes
    code = "wkt"

    def select_field_class(
        self,
        type: Optional[str] = None
    ) -> Optional[Type[frictionless.Field]]:
        """Return the custom field class for the plugin.

        Args:
            type (str): Denotes the type passed int from the frictionless
                framework for a field.

        Returns:
            Optional[Type[frictionless.Field]]: Reference to WKTField if type
                matches code else None.
        """
        if type == self.code:
            return WKTField
        return None


class WKTField(frictionless.Field):
    """Custom WKT Type implementation."""

    # Class attributes
    type = "wkt"
    builtin = False
    supported_constraints = [
        "required",
    ]

    def create_value_reader(self) -> frictionless.schema.types.IValueReader:
        """Creates value reader callable."""

        def value_reader(cell: Any) -> Optional[shapely.Geometry]:
            """Convert cell (read direction).

            Args:
                cell (Any): Cell to convert

            Returns:
                Optional[shapely.Geometry]: Converted cell or None if invalid
            """
            # Expect the cell to be a string.
            if not isinstance(cell, str):
                return None

            # Attempt to convert the WKT string
            try:
                geometry = shapely.from_wkt(cell)
            except shapely.GEOSException:
                return None

            # Return the CRS object
            return geometry

        # Return value_reader callable
        return value_reader

    def create_value_writer(self) -> frictionless.schema.types.IValueWriter:
        """Creates value write callable."""

        def value_writer(cell: shapely.Geometry) -> str:
            """Convert cell (write direction).

            Args:
                cell (shapely.Geometry): Cell to convert.

            Returns:
                str: Converted cell.

            Raises:
                TypeError: if the returned value from the shapely
                    method to_wkt is not string.
            """
            # Serialize to default format for pyproj
            wkt_str = shapely.to_wkt(
                geometry=cell,
                rounding_precision=8,
            )

            # Type checking due to no types provided by the shapely package
            if isinstance(wkt_str, str):
                return wkt_str
            raise TypeError(f"expected str; got {type(wkt_str)}")

        # Return value writer callable
        return value_writer


# Register WKT Plugin
frictionless.system.register(
    name=WKTPlugin.code,
    plugin=WKTPlugin(),
)
