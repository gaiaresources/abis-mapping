"""Provides Unit Tests for the `abis_mapping.plugins.list` module"""

# Third-Party
import frictionless
import pytest

# Local
from abis_mapping import plugins

# Typing
from typing import Any, Optional


def test_list_type_registered() -> None:
    """Tests the list field type is registered and delimiter property works."""
    # Create schema with list field
    schema: frictionless.Schema = frictionless.Schema.from_descriptor(
        {"fields": [{"name": "someList", "type": "list", "delimiter": " "}]}
    )

    # Extract list field
    field = schema.get_field("someList")

    # Will only reach this assertion if schema created (won't create if list not registered)
    assert not field.builtin
    # Assert delimiter set as per descriptor
    assert field.__getattribute__("delimiter") == " "


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
    ],
)
def test_list_type_read(
    format: str,  # noqa: A002
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
    # Instantiate the field
    field = plugins.list_field.ListField(
        name="testField",
        format=format,
        delimiter=delimiter,
    )

    # Read Cell
    result = field.read_cell(value)[0]

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
    ],
)
def test_list_type_write(
    format: str,  # noqa: A002
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
    # Instantiate the Field
    field = plugins.list_field.ListField(
        name="testField",
        format=format,
        delimiter=delimiter,
    )

    # Write Cell
    result = field.write_cell(value)[0]

    # Check Result
    assert result == expected
