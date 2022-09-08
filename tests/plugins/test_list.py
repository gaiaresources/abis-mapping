"""Provides Unit Tests for the `abis_mapping.plugins.list` module"""


# Third-Party
import frictionless
import pytest

# Local
from abis_mapping import plugins

# Typing
from typing import Optional


@pytest.mark.parametrize(
    argnames=[
        "type",
        "valid",
        "delimiter",
    ],
    argvalues=[
        # Valid
        ("list", True, " "),
        ("list[ ]", True, " "),
        ("list[|]", True, "|"),

        # Invalid
        ("any", False, None),
        ("list[]", False, None),
        ("list[", False, None),
        ("list]", False, None),
        ("list[ ", False, None),
        ("list ]", False, None),
        ("list[|", False, None),
        ("list|]", False, None),
    ]
)
def test_list_plugin(
    type: str,
    valid: bool,
    delimiter: Optional[str],
) -> None:
    """Tests the List Plugin.

    Args:
        type (str): Type of the field to test.
        valid (bool): Whether it is expected to be valid and succeed.
        delimiter (Optional[str]): Possible expected delimiter.
    """
    # Instantiate the Plugin
    plugin = plugins.list.ListPlugin()

    # Create Field
    field = frictionless.Field(type=type)
    result = plugin.create_type(field)

    # Check Results
    if valid:
        # Valid
        assert isinstance(result, plugins.list.ListType)
        assert result.delimiter == delimiter

    else:
        # Invalid
        assert result is None


def test_list_type_uris_space() -> None:
    """Tests the List Type with URIs and Space Delimiter"""
    # Instantiate the Type
    type = plugins.list.ListType(field=frictionless.Field(format="uri"))
    type.delimiter = " "  # Space Delimiter

    # Read Invalid Cells
    assert type.read_cell(123) is None
    assert type.read_cell("a") is None
    assert type.read_cell("a b c") is None

    # Read Valid Cells
    assert type.read_cell("https://a.com") == ["https://a.com"]
    assert type.read_cell("https://a.com https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com  https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com       https://b.com") == ["https://a.com", "https://b.com"]

    # Write Cell
    assert type.write_cell(["https://a.com"]) == "https://a.com"
    assert type.write_cell(["https://a.com", "https://b.com"]) == "https://a.com https://b.com"


def test_list_type_uris_pipe() -> None:
    """Tests the List Type with URIs and Pipe Delimiter"""
    # Instantiate the Type
    type = plugins.list.ListType(field=frictionless.Field(format="uri"))
    type.delimiter = "|"  # Pipe Delimiter

    # Read Invalid Cells
    assert type.read_cell(123) is None
    assert type.read_cell("a") is None
    assert type.read_cell("a b c") is None

    # Read Valid Cells
    assert type.read_cell("https://a.com") == ["https://a.com"]
    assert type.read_cell("https://a.com|https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com|||https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com | https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com   |   https://b.com") == ["https://a.com", "https://b.com"]
    assert type.read_cell("https://a.com   ||||   https://b.com") == ["https://a.com", "https://b.com"]

    # Write Cell
    assert type.write_cell(["https://a.com"]) == "https://a.com"
    assert type.write_cell(["https://a.com", "https://b.com"]) == "https://a.com|https://b.com"
