"""Provides unit tests for the fields module."""

# Standard
import io
import unittest.mock

# Third-party
import pytest
import frictionless
import pytest_mock

# Local
from docs import tables
from abis_mapping import types
from abis_mapping import plugins

# Typing
from typing import Any, Type


@pytest.fixture
def mocked_checklist(mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
    """Mocked FieldTabler.checklist method.

    Args:
        mocker (pytest_mock.MockerFixture): Mocker fixture.

    Returns:
        unittest.mock.MagicMock: mocked method.
    """
    # Create a checklist to return from the mocked method.
    checklist = frictionless.Checklist(
        checks=[
            plugins.mutual_inclusion.MutuallyInclusive(field_names=["FieldA", "FieldB"]),
            plugins.mutual_inclusion.MutuallyInclusive(field_names=["abc", "123"]),
            plugins.mutual_inclusion.MutuallyInclusive(field_names=["abc", "NotAField", "FakeField"]),
        ]
    )
    # Patch and return mock
    return mocker.patch.object(
        target=tables.fields.FieldTabler,
        attribute="checklist",
        return_value=checklist,
    )


@pytest.fixture
def mocked_mapper(
    mocked_mapper: unittest.mock.MagicMock,
) -> unittest.mock.MagicMock:
    """Mocked mapper with more fields.

    Args:
        mocked_mapper: Mapper fixture.

    Returns:
        Modified mocked mapper.
    """
    new_fields = [
        {
            "name": "abc",
            "title": "Abc",
            "description": "Alphabet",
            "example": "Alphabet EXAMPLE",
            "type": "string",
            "format": "default",
            "url": "http://example.com/abc",
            "constraints": {
                "required": False,
            },
        },
        {
            "name": "123",
            "title": "123",
            "description": "Numbers",
            "example": "Numbers EXAMPLE",
            "type": "string",
            "format": "default",
            "url": "http://example.com/123",
            "constraints": {
                "required": False,
            },
        },
        {
            "name": "threatStatus",
            "title": "Threat Status",
            "description": "The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific authority.",
            "example": "VU",
            "type": "string",
            "format": "default",
            "constraints": {"required": False},
            "vocabularies": ["THREAT_STATUS"],
        },
    ]
    # Schema
    descriptor = {"fields": [*mocked_mapper().schema()["fields"], *new_fields]}
    # Patch current schema with more fields
    mocked_mapper.return_value.schema.return_value = descriptor

    # Return
    return mocked_mapper


@pytest.fixture
def mocked_vocab(mocked_vocab: unittest.mock.MagicMock) -> unittest.mock.MagicMock:
    """Mocked vocab with details specific to this module.

    Args:
        mocked_vocab: Vocab fixture.

    Returns:
        Modified mocked vocab.
    """
    # Add threat status id since it is looked for by the occurrence tablers
    mocked_vocab.return_value.vocab_id = "THREAT_STATUS"
    # Return
    return mocked_vocab


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
                    ],
                },
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
                "checklist": frictionless.Checklist(),
                "constraints": {
                    "required": True,
                    "enum": [
                        "SOME EXAMPLE",
                        "Option 2",
                        "plan C",
                    ],
                },
            },
            {
                "Field Name": "someName",
                "Description": "Some description",
                "Mandatory / Optional": "Mandatory",
                "Datatype Format": "String",
                "Examples": "SOME EXAMPLE",
            },
        ),
    ],
)
def test_field_table_row(field: dict[str, Any], expected: dict[str, Any]) -> None:
    """Tests FieldTableRow serialization.

    Args:
        field (dict[str, Any]): Field dictionary.
        expected (dict[str, Any]): Expected dictionary.
    """
    # Create field from input
    f = types.schema.Field.model_validate(field)

    # Create field table row
    ftr = tables.fields.FieldTableRow(field=f, checklist=None)

    # Assert
    assert ftr.model_dump(by_alias=True) == expected


def test_header(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests the FieldTabler.header property.

    Args:
        mocked_mapper: Mocked mapper fixture.
    """
    # Create tabler
    tabler = tables.fields.FieldTabler("some_id")

    # Assert
    # Confirm mocks were of consequence
    mocked_mapper.assert_called()

    # Confirm expected output
    assert tabler.header == ["Field Name", "Description", "Mandatory / Optional", "Datatype Format", "Examples"]


def test_determine_checklist() -> None:
    """Tests the determine_checklist method."""
    # Create tabler
    tabler = tables.fields.FieldTabler("incidental_occurrence_data-v2.0.0.csv")

    # Invoke function
    checklist = tabler.checklist()

    # Assert
    assert checklist is not None
    assert len(checklist.checks) == 6


@pytest.mark.parametrize(
    "tabler_class, expected",
    [
        (
            tables.fields.FieldTabler,
            (
                "Field Name,Description,Mandatory / Optional,Datatype Format,Examples\r\n"
                "someName,Some description,Mandatory,String,SOME EXAMPLE\r\n"
                "anotherName,Another description,Mandatory,String,ANOTHER EXAMPLE\r\n"
                'abc,Alphabet,"Conditionally mandatory with 123, FakeField and NotAField",String,Alphabet EXAMPLE\r\n'
                "123,Numbers,Conditionally mandatory with abc,String,Numbers EXAMPLE\r\n"
                "threatStatus,The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific authority.,Optional,String,VU\r\n\n"
            ),
        ),
        (
            tables.fields.OccurrenceFieldTabler,
            (
                "Field Name,Description,Mandatory / Optional,Datatype Format,Examples\r\n"
                "someName,Some description,Mandatory,String,SOME EXAMPLE\r\n"
                "anotherName,Another description,Mandatory,String,ANOTHER EXAMPLE\r\n"
                'abc,Alphabet,"Conditionally mandatory with 123, FakeField and NotAField",String,Alphabet EXAMPLE\r\n'
                "123,Numbers,Conditionally mandatory with abc,String,Numbers EXAMPLE\r\n"
                "threatStatus,The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific authority.,Optional,String,VU\r\n\n"
            ),
        ),
    ],
    ids=["FieldTabler", "OccurrenceFieldTabler"],
)
def test_generate_table(
    tabler_class: Type[tables.fields.FieldTabler],
    expected: str,
    mocked_mapper: unittest.mock.MagicMock,
    mocked_vocab: unittest.mock.MagicMock,
    mocked_checklist: unittest.mock.MagicMock,
) -> None:
    """Tests generate_table method.

    Args:
        table_class: The type of FieldTabler under test
        expected: The expected generated output.
        mocked_mapper: Mocked mapper fixture.
        mocked_vocab: Mocked vocab fixture.
        mocked_checklist: Mocked FieldTabler.checklist method.
    """
    # Create an in memory io
    dest = io.StringIO()

    # Create a tabler
    tabler = tabler_class("some_id")

    # Invoke
    tabler.generate_table(
        dest=dest,
    )

    # Assert
    # Ensure the mocks were of consequence
    mocked_vocab.assert_called()
    mocked_mapper.assert_called()
    mocked_checklist.assert_called()

    # Confirm expected value
    assert dest.getvalue() == expected


@pytest.mark.parametrize(
    "tabler_class, expected",
    [
        pytest.param(
            tables.fields.FieldTabler,
            (
                "|Field Name|Description|Mandatory / Optional|Datatype Format|Examples|\n"
                "|:---|:---|:---:|:---:|:---|\n"
                '|<a name="someName-field"></a>someName|Some description|**<font color="Crimson">Mandatory</font>**|String|SOME EXAMPLE<br>([Vocabulary link](#someName-vocabularies))|\n'
                '|<a name="anotherName-field"></a>[anotherName](http://example.com/)|Another description|**<font color="Crimson">Mandatory</font>**|String|ANOTHER EXAMPLE|\n'
                '|<a name="abc-field"></a>[abc](http://example.com/abc)|Alphabet|**<font color="DarkGoldenRod">Conditionally mandatory with 123, FakeField and NotAField</font>**|String|Alphabet EXAMPLE|\n'
                '|<a name="123-field"></a>[123](http://example.com/123)|Numbers|**<font color="DarkGoldenRod">Conditionally mandatory with abc</font>**|String|Numbers EXAMPLE|\n'
                '|<a name="threatStatus-field"></a>threatStatus|The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific authority.|Optional|String|VU<br>([Vocabulary link](#threatStatus-vocabularies))|\n'
            ),
            id="FieldTabler",
        ),
        pytest.param(
            tables.fields.OccurrenceFieldTabler,
            (
                "|Field Name|Description|Mandatory / Optional|Datatype Format|Examples|\n"
                "|:---|:---|:---:|:---:|:---|\n"
                '|<a name="someName-field"></a>someName|Some description|**<font color="Crimson">Mandatory</font>**|String|SOME EXAMPLE<br>([Vocabulary link](#someName-vocabularies))|\n'
                '|<a name="anotherName-field"></a>[anotherName](http://example.com/)|Another description|**<font color="Crimson">Mandatory</font>**|String|ANOTHER EXAMPLE|\n'
                '|<a name="abc-field"></a>[abc](http://example.com/abc)|Alphabet|**<font color="DarkGoldenRod">Conditionally mandatory with 123, FakeField and NotAField</font>**|String|Alphabet EXAMPLE|\n'
                '|<a name="123-field"></a>[123](http://example.com/123)|Numbers|**<font color="DarkGoldenRod">Conditionally mandatory with abc</font>**|String|Numbers EXAMPLE|\n'
                '|<a name="threatStatus-field"></a>threatStatus|The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific authority.|Optional|String|VU<br>([Vocabulary link](#threatStatus-vocabularies))|\n'
            ),
            id="OccurrenceFieldTabler",
        ),
    ],
)
def test_generate_table_markdown(
    tabler_class: Type[tables.fields.FieldTabler],
    expected: str,
    mocked_mapper: unittest.mock.MagicMock,
    mocked_vocab: unittest.mock.MagicMock,
    mocked_checklist: unittest.mock.MagicMock,
) -> None:
    """Tests generate_table method with markdown format.

    Args:
        table_class: The type of FieldTabler under test
        expected: The expected generated output.
        mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
        mocked_vocab (unittest.mock.MagicMock): Mocked vocab fixture.
    """
    # Create a tabler
    tabler = tabler_class("some_id", format="markdown")

    # Invoke
    actual = tabler.generate_table()

    # Assert
    # Ensure the mocks were of consequence
    mocked_mapper.assert_called()
    mocked_vocab.assert_called()
    mocked_checklist.assert_called()

    # Confirm expected value
    assert actual == expected


def test_mutual_inclusivity() -> None:
    """Tests the mutual_inclusivity method."""
    # Create checklist
    checklist = frictionless.Checklist(
        checks=[
            plugins.mutual_inclusion.MutuallyInclusive(field_names=["fieldA", "fieldB"]),
            plugins.mutual_inclusion.MutuallyInclusive(field_names=["fieldB", "fieldC"]),
        ]
    )

    # Invoke function
    fields = tables.fields.mutual_inclusivity(field_name="fieldB", checklist=checklist)

    # Assert
    assert fields == ["fieldA", "fieldC"]
