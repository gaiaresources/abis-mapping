"""Provided unit tests common across all templates."""

# Local
import abis_mapping
import abis_mapping.base
from tests.templates import conftest

# Third-party
import pytest
import frictionless

# Typing
from typing import Type


@pytest.mark.parametrize(
    argnames="test_params",
    argvalues=[tc for tc in conftest.TEST_CASES],
    ids=[tc.template_id for tc in conftest.TEST_CASES]
)
class TestTemplateBasicSuite:
    @pytest.fixture(scope="class")
    def mappers(self) -> dict[str, Type[abis_mapping.base.mapper.ABISMapper]]:
        """Test fixture that retrieves all mappers"""
        return abis_mapping.get_mappers()

    def test_template_registered(
        self,
        mappers: dict[str, abis_mapping.base.mapper.ABISMapper],
        test_params: conftest.TemplateTestParameters
    ) -> None:
        """Tests that the supplied template id is registered."""
        assert test_params.template_id in mappers

    def test_validation(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests the validation for the template"""
        # Load Data
        data = test_params.mapping_cases[0].data.read_bytes()

        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Validate
        report = mapper().apply_validation(data)
        assert report.valid

    def test_metadata_sampling_type(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests the metadata sampling type set correctly"""
        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get metadata
        metadata = mapper().metadata()

        # Confirm field set correctly
        assert metadata.get("sampling_type") == test_params.metadata_sampling_type

    def test_schema_is_valid(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests that the schema.json is a valid frictionless schema."""
        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get schema dictionary
        descriptor = mapper().schema()

        # Generate report
        report = frictionless.Schema.validate_descriptor(descriptor)

        # Assert valid
        assert report.valid

    def test_validation_empty_template(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests validation fails for empty template."""
        # Load data
        data = test_params.empty_template.read_bytes()

        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Validate
        report = mapper().apply_validation(data)
        assert not report.valid
        error_codes = [code for codes in report.flatten(['type']) for code in codes]
        assert "table-dimensions" in error_codes
