"""Provides Unit Tests for the `abis_mapping.plugins.list` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_list_plugin() -> None:
    """Tests the List Plugin"""
    # Instantiate the Plugin
    plugin = plugins.list.ListPlugin()

    # Incorrect Type
    field = frictionless.Field(type="any")
    result = plugin.create_type(field)
    assert result is None

    # Correct Type
    field = frictionless.Field(type="list")
    result = plugin.create_type(field)
    assert isinstance(result, plugins.list.ListType)


def test_list_type() -> None:
    """Tests the List Type"""
    # Instantiate the Type
    type = plugins.list.ListType(field=frictionless.Field(format="uri"))

    # Read Invalid Cells
    assert type.read_cell(123) is None
    assert type.read_cell("a") is None
    assert type.read_cell("a b c") is None

    # Read Valid Cells
    assert type.read_cell("https://a.com") == ["https://a.com"]
    assert type.read_cell("https://a.com|https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com | https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com   |   https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com   |||   https://b.com") == ["https://a.com", "https://b.com"]

    # Write Cell
    assert type.write_cell(["https://a.com"]) == "https://a.com"
    assert type.write_cell(["https://a.com", "https://b.com"]) == "https://a.com|https://b.com"
