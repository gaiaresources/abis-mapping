"""Provides Unit Tests for the `abis_mapping.base` module"""


# Standard
import pathlib
import json
import csv
import io

# Third-party
import frictionless
import pytest
import rdflib
import pytest_mock

# Local
from abis_mapping import base
from abis_mapping import utils


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
    data = [
        {"A": 123, "B": 321, "C": 321.6546454654654, "D": True, "E": "something"}
    ]
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
            assert set(full_schema.field_names) == \
                   set(existing_schema.field_names) | expected_extra_fieldnames  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "template_id,file_path",
    [
        ("incidental_occurrence_data.csv",
         ("abis_mapping/templates/incidental_occurrence_data/examples/"
          "margaret_river_flora/margaret_river_flora_extra_cols.csv")),
        ("survey_occurrence_data.csv",
         ("abis_mapping/templates/survey_occurrence_data/examples/"
          "margaret_river_flora/margaret_river_flora_extra_cols.csv")),
        ("survey_metadata.csv",
         "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv"),
        ("survey_site_data.csv",
         "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols.csv"),
    ]
)
def test_extra_fields_schema_raw_data(template_id: str, file_path: str) -> None:
    """Tests extra fields schema gets extracted from row data."""
    # Expected extra field names
    expected_extra_fieldnames = {"extraInformation1", "extraInformation2"}

    # Get mapper
    mapper = base.mapper.get_mapper(template_id)
    assert mapper is not None

    # Get data
    data = pathlib.Path(file_path).read_bytes()

    # Construct official schema
    existing_schema = frictionless.Schema.from_descriptor(mapper().schema())

    # Extract extra columns schemas
    diff_schema = mapper.extra_fields_schema(data)
    full_schema = mapper.extra_fields_schema(data=data, full_schema=True)

    # Assert
    assert set(diff_schema.field_names) == expected_extra_fieldnames
    for field in diff_schema.fields:
        assert field.type == "string"
    assert set(full_schema.field_names) == \
           set(existing_schema.field_names) | expected_extra_fieldnames  # type: ignore[attr-defined]


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
    csv_string_io = io.StringIO()
    csv_writer = csv.DictWriter(csv_string_io, lineterminator="\n", fieldnames=data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(data)
    csv_data = csv_string_io.getvalue().encode("utf-8")

    # Construct base schema descriptor
    descriptor = {"fields": [{"name": "A", "type": "integer"}, {"name": "B", "type": "integer"}]}

    # Mock out the schema method to return the above descriptor
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Construct schema (includes extra fields)
    schema = base.mapper.ABISMapper.extra_fields_schema(csv_data, full_schema=True)

    # Construct resource
    resource = frictionless.Resource(data=csv_data, format="csv", schema=schema)

    # Open resource for row streaming
    with resource.open() as r:
        for row, expected in zip(r.row_stream, overall_expected):
            assert base.mapper.ABISMapper.extract_extra_fields(row) == expected


def test_add_extra_fields_json() -> None:
    """Tests addition of extra fields json string to graph."""
    # Create graph and base URI
    graph = rdflib.Graph()
    base_uri = utils.namespaces.EXAMPLE.someBaseUri

    # Expected json as dictionary
    expected_json = {
        "extraInformation2": "some more info",
        "extraInformation1": "some additional info"
    }

    # Create resource from raw data
    file_path = "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv"
    resource = frictionless.Resource(source=file_path)

    # Open resource for row streaming
    with resource.open() as r:
        # Only one row in the file
        row = next(r.row_stream)

    # Get mapper
    mapper = base.mapper.get_mapper("survey_metadata.csv")
    assert mapper is not None

    # Attach extra fields json to graph
    mapper.add_extra_fields_json(
        subject_uri=base_uri,
        row=row,
        graph=graph,
    )

    # Assert
    assert len(graph) == 1
    for (s, p, o) in graph:
        assert s == base_uri
        assert p == rdflib.RDFS.comment
        assert isinstance(o, rdflib.Literal)
        assert json.loads(str(o)) == expected_json
        assert o.datatype == rdflib.RDF.JSON


def test_add_extra_fields_json_no_data() -> None:
    """Tests functionality of json extra fields when none exists."""
    # Create graph and base URI
    graph = rdflib.Graph()
    base_uri = utils.namespaces.EXAMPLE.someBaseUri

    # Create resource from raw data
    file_path = "abis_mapping/templates/survey_metadata/examples/minimal.csv"
    resource = frictionless.Resource(source=file_path)

    # Open resource for row streaming
    with resource.open() as r:
        # Only one row in the file
        row = next(r.row_stream)

    # Get mapper
    mapper = base.mapper.get_mapper("survey_metadata.csv")
    assert mapper is not None

    # Attach extra fields json to graph (should have none).
    mapper.add_extra_fields_json(
        subject_uri=base_uri,
        row=row,
        graph=graph,
    )

    # Should have no triples
    assert len(graph) == 0
