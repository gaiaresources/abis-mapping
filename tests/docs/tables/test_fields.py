"""Provides unit tests for the fields module."""

# Standard
import io
import unittest.mock

# Third-party
import pytest
import frictionless

# Local
from docs import tables
from abis_mapping import types
from abis_mapping import plugins

# Typing
from typing import Any


@pytest.mark.parametrize(
    argnames="field, expected",
    argvalues=[
        (
            {
                "name": "someName",
                "title": "Some Title",
                "description": "Some description",
                "example": "SOME EXAMPLE",
                "type": "string",
                "format": "default",
                "constraints": {
                    "required": False,
                    "enum": [
                        "SOME EXAMPLE",
                        "Option 2",
                        "plan C",
                    ]
                }
            },
            {
                "Field Name": "someName",
                "Description": "Some description",
                "Mandatory / Optional": "Optional",
                "Datatype Format": "String",
                "Examples": "SOME EXAMPLE",
            },
        ),
        (
            {
                "name": "someName",
                "title": "Some Title",
                "description": "Some description",
                "example": "SOME EXAMPLE",
                "type": "string",
                "format": "default",
                "constraints": {
                    "required": True,
                    "enum": [
                        "SOME EXAMPLE",
                        "Option 2",
                        "plan C",
                    ]
                }
            },
            {
                "Field Name": "someName",
                "Description": "Some description",
                "Mandatory / Optional": "Mandatory",
                "Datatype Format": "String",
                "Examples": "SOME EXAMPLE",
            }
        ),
    ],
)
def test_generate_row(field: dict[str, Any], expected: dict[str, Any]) -> None:
    """Tests generate_row function

    Args:
        field (dict[str, Any]): Field dictionary.
        expected (dict[str, Any]): Expected dictionary.
    """
    # Create field from input
    f = types.schema.Field.model_validate(field)

    # Invoke function
    result = tables.fields.FieldTabler.generate_row(f)

    # Assert
    assert result.model_dump(by_alias=True) == expected


def test_determine_checklist() -> None:
    """Tests the determine_checklist method."""
    # Create tabler
    tabler = tables.fields.FieldTabler("incidental_occurrence_data-v2.0.0.csv")

    # Invoke function
    checklist = tabler.determine_checklist()

    # Assert
    assert checklist is not None
    assert len(checklist.checks) == 6


def test_generate_table(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests generate_table method.

    Args:
        mocked_mapper (pytest_mock.mocker.mock.MagicMock): Mocked mapper fixture.
    """
    # Create an in memory io
    dest = io.StringIO()

    # Create a tabler
    tabler = tables.fields.FieldTabler("some_id")

    # Invoke
    tabler.generate_table(
        dest=dest,
    )

    # Assert
    assert dest.getvalue() == (
        'Field Name,Description,Mandatory / Optional,Datatype Format,Examples\r\n'
        'someName,Some description,Mandatory,String,SOME EXAMPLE\r\n\n'
    )


def test_generate_table_markdown(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests generate_table method with markdown format.

    Args:
        mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
    """
    # Create a tabler
    tabler = tables.fields.FieldTabler("some_id")

    # Invoke
    actual = tabler.generate_table(as_markdown=True)

    # Assert
    assert actual == (
        '|Field Name|Description|Mandatory / Optional|Datatype Format|Examples|\r\n'
        '|---|---|---|---|---|\r\n'
        '|someName|Some description|Mandatory|String|SOME EXAMPLE|\r\n'
    )


def test_mutual_inclusivity() -> None:
    """Tests the mutual_inclusivity method."""
    # Create checklist
    checklist = frictionless.Checklist(
        checks=[
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["fieldA", "fieldB"]
            ),
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["fieldB", "fieldC"]
            )
        ]
    )

    # Invoke function
    fields = tables.fields.FieldTabler.mutual_inclusivity(field_name="fieldB", checklist=checklist)

    # Assert
    assert fields == {"fieldA", "fieldC"}
