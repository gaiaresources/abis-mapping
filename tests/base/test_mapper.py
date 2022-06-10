"""Provides Unit Tests for the `abis_mapping.base` module"""


# Standard
import pathlib

# Local
from abis_mapping import base


# Constants
TEMPLATE_ID_REAL = "occurrence_data.csv"
TEMPLATE_ID_FAKE = "fake"
NUMBER_OF_TEMPLATES = 1


def test_base_get_mapper() -> None:
    """Tests that we can retrieve a mapper based on its template ID"""
    # Test Fake Template ID
    fake_mapper = base.mapper.get_mapper(TEMPLATE_ID_FAKE)
    assert fake_mapper is None

    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(TEMPLATE_ID_REAL)
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
    real_mapper = mappers.get(TEMPLATE_ID_REAL)
    assert real_mapper is not None
    assert issubclass(real_mapper, base.mapper.ABISMapper)


def test_base_get_template() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(TEMPLATE_ID_REAL)
    assert real_mapper is not None
    template = real_mapper.template()
    assert isinstance(template, pathlib.Path)
    assert template.is_file()


def test_base_get_metadata() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(TEMPLATE_ID_REAL)
    assert real_mapper is not None
    metadata = real_mapper.metadata()
    assert isinstance(metadata, dict)


def test_base_get_schema() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(TEMPLATE_ID_REAL)
    assert real_mapper is not None
    schema = real_mapper.schema()
    assert isinstance(schema, dict)


def test_base_get_instructions() -> None:
    """Tests the functionality of the base mapper"""
    # Test Real Template ID
    real_mapper = base.mapper.get_mapper(TEMPLATE_ID_REAL)
    assert real_mapper is not None
    instructions = real_mapper.instructions()
    assert isinstance(instructions, pathlib.Path)
    assert instructions.is_file()
