"""Provides unit tests for the `abis_mapping.plugins.wkt` module."""

# Third-party
import frictionless
import shapely

# Local
from abis_mapping import plugins


def test_wkt_plugin() -> None:
    """Tests the wkt plugin"""
    # Instantiate plugin
    plugin = plugins.wkt.WKTPlugin()

    # Incorrect type
    result = plugin.select_field_class("notAType")
    assert result is None

    # Correct Type
    result = plugin.select_field_class("wkt")
    assert result is plugins.wkt.WKTField


def test_wkt_registered() -> None:
    """Tests the wkt field type is registered."""
    # Create schema with wkt field
    schema: frictionless.Schema = frictionless.Schema.from_descriptor({
        'fields': [{'name': 'someWKT', 'type': 'wkt'}]
    })

    # Extract timestamp field
    field = schema.get_field('someWKT')

    # Will only reach this assertion if schema created (i.e. WKT type registered)
    assert not field.builtin


def test_wkt_type() -> None:
    """Tests the WKT type."""
    # Instantiate the field
    field = plugins.wkt.WKTField(
        name="TestField",
    )

    # Read invalid cells
    assert field.read_cell(123)[0] is None
    assert field.read_cell("hello world")[0] is None
    assert field.read_cell("POINT (2.0, abc)")[0] is None
    assert field.read_cell("POLYGON ((1 1, 1 4, 4 4, 4 1))")[0] is None

    # Read valid cells
    assert field.read_cell("POINT (2.0 3.0)")[0]
    assert field.read_cell("LINESTRING (1 1, 2 2, 3 3)")[0]
    assert field.read_cell("POLYGON ((1 1, 1 4, 4 4, 4 1, 1 1))")[0]
    assert field.read_cell("MULTIPOINT (2 3, 4 5, 6 7)")[0]
    assert field.read_cell("MULTILINESTRING ((1 1, 2 2, 3 3), (4 4, 5 5))")[0]
    assert field.read_cell("MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)), ((2 2, 2 3, 3 3, 3 2, 2 2)))")[0]
    assert field.read_cell("GEOMETRYCOLLECTION (POINT (2 3), LINESTRING (1 1, 2 2))")[0]

    # Write cell
    assert field.write_cell(shapely.Point(1, 2))[0]
    assert field.write_cell(shapely.LineString(((1, 1), (0, 0))))[0]
