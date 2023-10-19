"""Provides Unit Tests for the `abis_mapping.base` module"""

# Standard
import pathlib

import pytest

# Local
from abis_mapping import base

# Constants
TEMPLATE_ID_REAL = ["incidental_occurrence_data.csv", "survey_occurrence_data.csv", "survey_metadata.csv"]
TEMPLATE_ID_FAKE = "fake"
NUMBER_OF_TEMPLATES = len(TEMPLATE_ID_REAL)


def test_base_get_mapper() -> None:
    """Tests that we can retrieve a mapper based on its template ID"""
    # Test Fake Template ID
    fake_mapper = base.mapper.get_mapper(TEMPLATE_ID_FAKE)
    assert fake_mapper is None

    # Test Real Template IDs
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = base.mapper.get_mapper(template_id)
        assert real_mapper is not None
        assert issubclass(real_mapper, base.mapper.ABISMapper)


def test_base_get_mappers() -> None:
    """Tests that we can retrieve a dictionary of all mappers"""
    # Test All Mappers
    mappers = base.mapper.get_mappers()
    assert len(mappers) == NUMBER_OF_TEMPLATES

    # Test Fake Template ID
    fake_mapper = mappers.get(TEMPLATE_ID_FAKE)
    assert fake_mapper is None

    # Test Real Template ID
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = mappers.get(template_id)
        assert real_mapper is not None
        assert issubclass(real_mapper, base.mapper.ABISMapper)


def test_base_get_template() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = base.mapper.get_mapper(template_id)
        assert real_mapper is not None
        template = real_mapper.template()
        assert isinstance(template, pathlib.Path)
        assert template.is_file()


def test_base_get_metadata() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = base.mapper.get_mapper(template_id)
        assert real_mapper is not None
        metadata = real_mapper.metadata()
        assert isinstance(metadata, dict)


def test_metadata_id_match() -> None:
    """Tests the metadata id matches the mapper id"""
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = base.mapper.get_mapper(template_id)
        assert real_mapper is not None
        metadata = real_mapper.metadata()
        assert metadata.get("id") == real_mapper.template_id


def test_base_get_schema() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    for template_id in TEMPLATE_ID_REAL:
        real_mapper = base.mapper.get_mapper(template_id)
        assert real_mapper is not None
        schema = real_mapper.schema()
        assert isinstance(schema, dict)


def test_base_get_instructions() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    for template_id in TEMPLATE_ID_REAL:
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
