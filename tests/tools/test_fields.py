"""Provides unit tests for the fields module."""

# Standard
import sys
import io

# Third-party
import pytest
import pytest_mock
import frictionless

# Local
import tools.fields
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
    result = tools.fields.generate_row(f)

    # Assert
    assert result.model_dump(by_alias=True) == expected


def test_compile_fields_raises_invalid_template_id() -> None:
    """Tests that compile_fields function raises on invalid template id."""

    with pytest.raises(ValueError):
        tools.fields.compile_fields(template_id="FAKE_ID", dest=sys.stdout)


def test_compile_fields(mocker: pytest_mock.MockerFixture) -> None:
    """Tests compile_fields function.

    Args:
        mocker (pytest_mock.MockerFixture): Mocker fixture.
    """
    # Patch get_mapper
    mocked_mapper = mocker.patch("abis_mapping.base.mapper.get_mapper")

    # Patch schema
    mocked_mapper.return_value.schema.return_value = {
        "fields": [
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
            }
        ]
    }

    # Create an in memory io
    dest = io.StringIO()

    # Invoke
    tools.fields.compile_fields(
        template_id="some_id",
        dest=dest,
    )

    # Assert
    assert dest.getvalue() == (
        'Field Name,Description,Mandatory / Optional,Datatype Format,Examples\r\n'
        'someName,Some description,Mandatory,String,SOME EXAMPLE\r\n\n'
    )


def test_determine_checklist() -> None:
    """Tests the determine_checklist function."""
    # Invoke function
    checklist = tools.fields.determine_checklist("incidental_occurrence_data-v2.0.0.csv")

    # Assert
    assert len(checklist.checks) == 6


def test_mutual_inclusivity() -> None:
    """Tests the mutual_inclusivity function."""
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
    fields = tools.fields.mutual_inclusivity(field_name="fieldA", checklist=checklist)

    # Assert
    assert fields == {"fieldB"}
