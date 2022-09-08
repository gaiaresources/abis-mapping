"""Provides Unit Tests for the `abis_mapping.plugins.list` module"""


# Third-Party
import frictionless
import pytest

# Local
from abis_mapping import plugins

# Typing
from typing import Any, Optional


@pytest.mark.parametrize(
    argnames=[
        "type",
        "valid",
        "delimiter",
    ],
    argvalues=[
        # Valid
        ("list", True, "|"),
        ("list[|]", True, "|"),
        ("list[ ]", True, " "),
        ("list[anything]", True, "anything"),

        # Invalid
        ("anything", False, None),
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


@pytest.mark.parametrize(
    argnames=[
        "format",
        "delimiter",
        "value",
        "expected",
    ],
    argvalues=[
        # Valid
        ("default", " ", "a b c", ["a", "b", "c"]),
        ("default", " ", "a   b   c", ["a", "b", "c"]),
        ("default", "|", "a|b|c", ["a", "b", "c"]),
        ("default", "|", "a | b | c", ["a", "b", "c"]),
        ("uri", " ", "https://a.com", ["https://a.com"]),
        ("uri", " ", "https://a.com https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", " ", "https://a.com  https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", " ", "https://a.com       https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", "|", "https://a.com", ["https://a.com"]),
        ("uri", "|", "https://a.com|https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", "|", "https://a.com|||https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", "|", "https://a.com | https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", "|", "https://a.com   |   https://b.com", ["https://a.com", "https://b.com"]),
        ("uri", "|", "https://a.com   ||||   https://b.com", ["https://a.com", "https://b.com"]),

        # Invalid
        ("uri", "|", 123, None),
        ("uri", "|", "a", None),
        ("uri", "|", "a|b|c", None),
    ]
)
def test_list_type_read(
    format: str,
    delimiter: str,
    value: Any,
    expected: Optional[list[str]],
) -> None:
    """Tests the List Type Read Cell Functionality.

    Args:
        format (str): Format of the string field to test.
        delimiter (str): Delimiter of the list type to test.
        value (Any): Value to read and test.
        expected (Optional[list[str]]): Expected outcome of reading the value.
    """
    # Instantiate the Type
    type = plugins.list.ListType(field=frictionless.Field(format=format))
    type.delimiter = delimiter

    # Read Cell
    result = type.read_cell(value)

    # Check Result
    assert result == expected


@pytest.mark.parametrize(
    argnames=[
        "format",
        "delimiter",
        "value",
        "expected",
    ],
    argvalues=[
        # Valid
        ("default", " ", ["a"], "a"),
        ("default", " ", ["a", "b", "c"], "a b c"),
        ("default", "|", ["a"], "a"),
        ("default", "|", ["a", "b", "c"], "a|b|c"),
        ("uri", " ", ["https://a.com"], "https://a.com"),
        ("uri", " ", ["https://a.com", "https://b.com"], "https://a.com https://b.com"),
        ("uri", "|", ["https://a.com"], "https://a.com"),
        ("uri", "|", ["https://a.com", "https://b.com"], "https://a.com|https://b.com"),
    ]
)
def test_list_type_write(
    format: str,
    delimiter: str,
    value: list[str],
    expected: str,
) -> None:
    """Tests the List Type Write Cell Functionality.

    Args:
        format (str): Format of the string field to test.
        delimiter (str): Delimiter of the list type to test.
        value (list[str]): Value to write and test.
        expected (str): Expected outcome of writing the value.
    """
    # Instantiate the Type
    type = plugins.list.ListType(field=frictionless.Field(format=format))
    type.delimiter = delimiter

    # Write Cell
    result = type.write_cell(value)

    # Check Result
    assert result == expected
