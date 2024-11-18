"""Provides Unit Tests for the `abis_mapping.base` module"""

# Standard
import csv
import copy
import io
import json
import pathlib
import unittest.mock

# Third-party
import frictionless
import rdflib
import pytest_mock

# Local
from abis_mapping import base
from abis_mapping import utils

# Typing
from typing import Any, Optional, Iterator

from abis_mapping.base import types as base_types


class ContextualStringIO(io.StringIO):
    """An implementation to allow examining the final value of a StringIO prior to close."""

    final_buffer: str

    def close(self) -> None:
        """Sets the final_buffer prior to close."""
        self.final_buffer = self.getvalue()
        super().close()


class StubMapper(base.mapper.ABISMapper):
    def apply_mapping(
        self,
        data: base_types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        yield from []

    def apply_validation(  # type: ignore[empty-body]
        self, data: base_types.ReadableType, **kwargs: Any
    ) -> frictionless.Report:
        pass


def data_to_csv(data: list[dict[str, Any]]) -> bytes:
    """Converts list of dictionaries with common keys to a csv.

    Args:
        data (list[dict[str, Any]]): Dataset to be converted to csv string

    Returns:
        bytes: CSV encoded utf-8.

    Raises:
        ValueError: If any of the dictionary keys are not equal to other list entries.
    """
    # Ensure all keys of dictionary are equal
    if len(data) > 1 and any([set(data[0].keys()) != set(d.keys()) for d in data[1:]]):
        raise ValueError("Keys not the same for all data rows.")

    # Create in memory stream writer
    csv_string_io = io.StringIO()
    csv_writer = csv.DictWriter(csv_string_io, lineterminator="\n", fieldnames=data[0].keys())

    # Write header to stream
    csv_writer.writeheader()

    # Write data
    csv_writer.writerows(data)

    # Retrieve result from stream and encode utf-8
    return csv_string_io.getvalue().encode("utf-8")


def test_schema(mocker: pytest_mock.MockerFixture) -> None:
    """Tests the schema method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Define fake schema
    raw_schema = {
        "fields": [
            {
                "name": "providerRecordID",
                "title": "Provider Record ID",
                "description": "Unique (within provider) identifier for the record.",
                "example": "8022FSJMJ079c5cf",
                "type": "string",
                "format": "default",
                "constraints": {"required": True},
            },
            {
                "name": "providerRecordIDSource",
                "title": "Provider Record ID Source",
                "description": "Person or Organisation that generated the providerRecordID.",
                "example": "Western Australian Biodiversity Information Office",
                "type": "string",
                "format": "default",
                "constraints": {
                    "required": True,
                },
            },
            {
                "name": "locality",
                "title": "Locality",
                "description": "The specific description of the place.",
                "example": "Cowaramup Bay Road",
                "type": "string",
                "format": "default",
                "url": "https://dwc.tdwg.org/terms/#dwc:locality",
                "constraints": {"required": False},
            },
        ]
    }
    # Patch the pathlib.Path.read_text method
    mocker.patch.object(pathlib.Path, "read_text", return_value=json.dumps(raw_schema))

    # Create mapper
    mapper = StubMapper()

    # Invoke
    actual = mapper.schema()

    # Expected
    expected = copy.deepcopy(raw_schema)

    # Add any changes from the raw_schema below
    for f in expected["fields"]:
        if f.get("vocabularies") is None:
            f["vocabularies"] = []

    # Assert
    assert actual == expected


def test_generate_blank_template(mocker: pytest_mock.MockerFixture) -> None:
    """Tests the generate_blank_template method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Create and assign mock for pathlib.Path.read_text method
    return_value = {
        "fields": [
            {
                "name": "col1",
            },
            {
                "name": "col2",
            },
        ],
    }
    mocked_read_text = mocker.patch.object(pathlib.Path, "read_text")
    mocked_read_text.return_value = json.dumps(return_value)

    # Create and assign mock for pathlib.Path.open method
    mocked_open = mocker.patch.object(pathlib.Path, "open")
    output_stream = ContextualStringIO()
    mocked_open.return_value = output_stream

    # Patch the metadata method
    mocker.patch.object(base.mapper.ABISMapper, "metadata", return_value={"name": "some_template", "file_type": "CSV"})

    # Invoke
    base.mapper.ABISMapper.generate_blank_template()

    # Confirm result
    assert output_stream.final_buffer == "col1,col2\r\n"


def test_base_get_mapper_fake() -> None:
    """Tests that we can't retrieve a mapper with an invalid ID"""
    # Test Fake Template ID
    fake_mapper = base.mapper.get_mapper("fake")
    assert fake_mapper is None


def test_extra_fields_schema_row_data(mocker: pytest_mock.MockerFixture) -> None:
    """Tests extra fields schema gets extracted from row data.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Construct dataset
    data = [{"A": 123, "B": 321, "C": 321.6546454654654, "D": True, "E": "something"}]
    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Expected field names
    expected_extra_fieldnames = {"C", "D", "E"}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor
    existing_schema = frictionless.Schema.from_descriptor(descriptor)

    # Construct resource
    resource = frictionless.Resource(source=data)

    # Open resource for row streaming
    with resource.open() as r:
        for row in r.row_stream:
            # Extract extra columns schema
            diff_schema = base.mapper.ABISMapper.extra_fields_schema(row)

            # Extract full schema
            full_schema = base.mapper.ABISMapper.extra_fields_schema(row, full_schema=True)

            # Verify
            assert set(diff_schema.field_names) == expected_extra_fieldnames
            for field in diff_schema.fields:
                assert field.type == "string"
            assert set(full_schema.field_names) == set(existing_schema.field_names) | expected_extra_fieldnames


def test_extra_fields_schema_raw_data(mocker: pytest_mock.MockerFixture) -> None:
    """Tests extra fields schema gets extracted from raw data.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Create raw data
    data = [
        {"A": 123, "B": 321, "extraInformation1": "some extra information", "extraInformation2": ""},
        {"A": 321, "B": 123, "extraInformation1": "", "extraInformation2": "some more extra information"},
    ]

    # Expected extra field names
    expected_extra_fieldnames = {"extraInformation1", "extraInformation2"}

    # Get mapper
    mapper = base.mapper.ABISMapper
    assert mapper is not None

    # Get data
    csv_data = data_to_csv(data)

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Construct official schema
    existing_schema = frictionless.Schema.from_descriptor(mapper.schema())

    # Extract extra columns schemas
    diff_schema = mapper.extra_fields_schema(csv_data)
    full_schema = mapper.extra_fields_schema(data=csv_data, full_schema=True)

    # Assert
    assert set(diff_schema.field_names) == expected_extra_fieldnames
    for field in diff_schema.fields:
        assert field.type == "string"
    assert set(full_schema.field_names) == set(existing_schema.field_names) | expected_extra_fieldnames


def test_extract_extra_fields(mocker: pytest_mock.MockerFixture) -> None:
    """Tests extraction of extra fields from a row.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture
    """
    # Construct dataset
    data = [
        {"A": 123, "B": 321, "C": 321.6546454654654, "D": True, "E": "something"},
        {"A": 321, "B": 123, "C": 6.54654e-15, "D": False, "E": "another thing"},
    ]
    # Expected results
    overall_expected = [
        {"C": "321.6546454654654", "D": "True", "E": "something"},
        {"C": "6.54654e-15", "D": "False", "E": "another thing"},
    ]

    # Serialize data to csv
    csv_data = data_to_csv(data)

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Construct schema (includes extra fields)
    schema = base.mapper.ABISMapper.extra_fields_schema(csv_data, full_schema=True)
    # construct schema just for extra fields
    extra_schema = base.mapper.ABISMapper.extra_fields_schema(csv_data, full_schema=False)

    # Construct resource
    resource = frictionless.Resource(
        source=csv_data,
        format="csv",
        schema=schema,
        encoding="utf-8",
    )

    # Open resource for row streaming
    with resource.open() as r:
        # Iterate over rows and expected outputs for validation.
        for row, expected in zip(r.row_stream, overall_expected, strict=True):
            assert base.mapper.ABISMapper.extract_extra_fields(row, extra_schema) == expected


def test_add_extra_fields_json(mocker: pytest_mock.MockerFixture) -> None:
    """Tests addition of extra fields json string to graph.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Create graph and base URI
    graph = rdflib.Graph()
    base_uri = utils.namespaces.EXAMPLE.someBaseUri

    # Create raw data
    data = [
        {"A": 123, "B": 321, "extraInformation1": "some additional info", "extraInformation2": "some more info"},
    ]

    # Get data
    csv_data = data_to_csv(data)

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # construct schema just for extra fields
    extra_schema = base.mapper.ABISMapper.extra_fields_schema(csv_data, full_schema=False)

    # Expected json as dictionary
    expected_json = {"extraInformation2": "some more info", "extraInformation1": "some additional info"}

    # Create resource from raw data with derived schema
    resource = frictionless.Resource(
        source=csv_data,
        format="csv",
        encoding="utf-8",
    )

    # Open resource for row streaming
    with resource.open() as r:
        # Only one row in the file
        row = next(r.row_stream)

    # Get mapper
    mapper = base.mapper.ABISMapper

    # Attach extra fields json to graph
    mapper.add_extra_fields_json(
        subject_uri=base_uri,
        row=row,
        graph=graph,
        extra_schema=extra_schema,
    )

    # Assert
    assert len(graph) == 1
    for s, p, o in graph:
        assert s == base_uri
        assert p == rdflib.RDFS.comment
        assert isinstance(o, rdflib.Literal)
        assert json.loads(str(o)) == expected_json
        assert o.datatype == rdflib.RDF.JSON


def test_add_extra_fields_json_no_data(mocker: pytest_mock.MockerFixture) -> None:
    """Tests functionality of json extra fields when none exists."""
    # Create graph and base URI
    graph = rdflib.Graph()
    base_uri = utils.namespaces.EXAMPLE.someBaseUri

    # Create raw data - no extra fields
    data = [{"A": 123, "B": 321}]

    # Get data
    csv_data = data_to_csv(data)

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # construct schema just for extra fields
    extra_schema = base.mapper.ABISMapper.extra_fields_schema(csv_data, full_schema=False)

    # Create resource from raw data with derived schema
    resource = frictionless.Resource(
        source=csv_data,
        format="csv",
        encoding="utf-8",
    )

    # Open resource for row streaming
    with resource.open() as r:
        # Only one row in the file
        row = next(r.row_stream)

    # Get mapper
    mapper = base.mapper.ABISMapper

    # Attach extra fields json to graph (should have none).
    mapper.add_extra_fields_json(
        subject_uri=base_uri,
        row=row,
        graph=graph,
        extra_schema=extra_schema,
    )

    # Should have no triples
    assert len(graph) == 0


def test_extra_fields_middle(mocker: pytest_mock.MockerFixture) -> None:
    """Tests that extra fields in middle fails validation even with extra fields allowed.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Create raw data - no extra fields
    data = [{"A": 123, "C": 333, "B": 321}]

    # Get data
    csv_data = data_to_csv(data)

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Create resource from raw data with derived schema
    resource = frictionless.Resource(
        source=csv_data,
        format="csv",
        schema=frictionless.Schema.from_descriptor(descriptor),
        encoding="utf-8",
    )

    # These errors must be skipped to enable extra columns
    skip_errors = ["extra-label", "extra-cell"]

    # Perform validation
    report = resource.validate(checklist=frictionless.Checklist(skip_errors=skip_errors))

    # Assert
    assert not report.valid
    error_codes = [code for codes in report.flatten(["type"]) for code in codes]
    assert error_codes == ["incorrect-label"]


def test_fields(
    mocker: pytest_mock.MockerFixture,
    mocked_vocab: unittest.mock.MagicMock,
) -> None:
    """Tests the fields method.

    Args:
        mocker (pytest_mock.MockerFixture): Pytest mocker fixture
        mocked_vocab (unittest.mock.MagicMock): Patched get_vocab and resulting mock.
    """
    # Patch schema method
    descriptor = {
        "fields": [
            {
                "name": "fieldA",
                "title": "Title A",
                "description": "Description A",
                "example": "Example A",
                "type": "typeA",
                "format": "formatA",
                "constraints": {
                    "required": False,
                },
                "vocabularies": ["vocabularyA"],
            },
            {
                "name": "fieldB",
                "title": "Title B",
                "description": "Description B",
                "example": "Example B",
                "type": "typeB",
                "format": "formatB",
                "constraints": {
                    "required": False,
                },
                "vocabularies": ["vocabularyB"],
            },
        ]
    }
    mocker.patch.object(base.mapper.ABISMapper, "schema", return_value=descriptor)

    # Create mapper
    mapper = StubMapper()

    # Assert
    assert list(mapper.fields().keys()) == ["fieldA", "fieldB"]
