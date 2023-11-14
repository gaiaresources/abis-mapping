"""Provides Unit Tests for the `abis_mapping.base` module"""
import dataclasses
# Standard
import pathlib
import json

# Third-party
import frictionless
import pytest
import rdflib

# Local
from abis_mapping import base
from abis_mapping import utils

# Constants
TEMPLATE_ID_REAL = [
    "incidental_occurrence_data.csv",
    "survey_occurrence_data.csv",
    "survey_metadata.csv",
    "survey_site_data.csv",
]
TEMPLATE_ID_FAKE = "fake"

def test_base_get_mapper_fake() -> None:
    """Tests that we can't retrieve a mapper with an invalid ID"""
    # Test Fake Template ID
    fake_mapper = base.mapper.get_mapper(TEMPLATE_ID_FAKE)
    assert fake_mapper is None


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_mapper(template_id: str) -> None:
    """Tests that we can retrieve a mapper based on its template ID"""
    # Test Real Template IDs
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    assert issubclass(real_mapper, base.mapper.ABISMapper)


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_mappers(template_id: str) -> None:
    """Tests that we can retrieve a dictionary of all mappers"""
    # Test All Mappers
    mappers = base.mapper.get_mappers()
    assert len(mappers) == len(TEMPLATE_ID_REAL)

    # Test Fake Template ID
    fake_mapper = mappers.get(TEMPLATE_ID_FAKE)
    assert fake_mapper is None

    # Test Real Template ID
    real_mapper = mappers.get(template_id)
    assert real_mapper is not None
    assert issubclass(real_mapper, base.mapper.ABISMapper)


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_template(template_id: str) -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    template = real_mapper.template()
    assert isinstance(template, pathlib.Path)
    assert template.is_file()


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_metadata(template_id: str) -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    metadata = real_mapper.metadata()
    assert isinstance(metadata, dict)


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_metadata_id_match(template_id: str) -> None:
    """Tests the metadata id matches the mapper id"""
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    metadata = real_mapper.metadata()
    assert metadata.get("id") == real_mapper.template_id


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_schema(template_id: str) -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    schema = real_mapper.schema()
    assert isinstance(schema, dict)


@pytest.mark.parametrize(
    "template_id",
    TEMPLATE_ID_REAL,
)
def test_base_get_instructions(template_id: str) -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(template_id)
    assert real_mapper is not None
    instructions = real_mapper.instructions()
    assert isinstance(instructions, pathlib.Path)
    assert instructions.is_file()


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
def test_apply_validation_extra_columns(template_id: str, file_path: str) -> None:
    """Tests that extra columns pass validation"""
    # Get mapper
    mapper = base.mapper.get_mapper(template_id)
    assert mapper is not None

    # Ingest extra column data
    data = pathlib.Path(file_path).read_bytes()

    # Perform validation
    report = mapper().apply_validation(data)

    # Assert
    assert report.valid


@pytest.mark.parametrize(
    "template_id,file_path",
    [
        ("incidental_occurrence_data.csv",
         ("abis_mapping/templates/incidental_occurrence_data/examples/"
          "margaret_river_flora/margaret_river_flora_extra_cols_mid.csv")),
        ("survey_occurrence_data.csv",
         ("abis_mapping/templates/survey_occurrence_data/examples/"
          "margaret_river_flora/margaret_river_flora_extra_cols_mid.csv")),
        ("survey_metadata.csv",
         "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols_mid.csv"),
        ("survey_site_data.csv",
         "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols_mid.csv"),
    ]
)
def test_apply_validation_extra_columns_middle(template_id: str, file_path: str) -> None:
    """Tests that extra columns in the middle of the data fails validation."""
    # Get mapper
    mapper = base.mapper.get_mapper(template_id)
    assert mapper is not None

    # Ingest invalid extra column data
    data = pathlib.Path(file_path).read_bytes()

    # Perform validation
    report = mapper().apply_validation(data)

    # Assert
    assert not report.valid
    error_codes = [code for codes in report.flatten(['type']) for code in codes]
    assert "incorrect-label" in error_codes


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
def test_extra_fields_schema_row_data(template_id: str, file_path: str) -> None:
    """Tests extra fields schema gets extracted from row data."""
    # Expected extra field names
    expected_extra_fieldnames = {"extraInformation1", "extraInformation2"}

    # Get mapper
    mapper = base.mapper.get_mapper(template_id)
    assert mapper is not None

    # Create resource from raw data
    resource = frictionless.Resource(source=file_path)

    # Construct official schema
    existing_schema = frictionless.Schema.from_descriptor(mapper().schema())

    # Open resource for row streaming
    with resource.open() as r:
        for row in r.row_stream:
            # Extract extra columns schema
            diff_schema = mapper.extra_fields_schema(row)
            full_schema = mapper.extra_fields_schema(data=row, full_schema=True)

            # Assert
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


def test_extract_extra_fields() -> None:
    """Tests extraction of extra fields from a row."""
    # Get mapper
    mapper = base.mapper.get_mapper("survey_metadata.csv")
    assert mapper is not None

    # Create resource from raw data
    file_path = "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv"
    resource = frictionless.Resource(source=file_path)

    # Expected result
    expected = {
        "extraInformation1": "some additional info",
        "extraInformation2": "some more info",
    }

    # Open resource for row streaming
    with resource.open() as r:
        # Only one row in the file
        row = next(r.row_stream)
        assert mapper().extract_extra_fields(row) == expected


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
