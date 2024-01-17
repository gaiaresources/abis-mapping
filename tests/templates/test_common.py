"""Provided unit tests common across all templates."""
import pytest_mock

# Local
import abis_mapping
import abis_mapping.base
from tests.templates import conftest

# Standard
import pathlib
import unittest.mock

# Third-party
import pytest
import frictionless

# Typing
from typing import Type


@pytest.fixture(scope="module")
def case_template_ids() -> list[str]:
    """Test fixture that returns all test case template ids."""
    return [tc.template_id for tc in conftest.TEST_CASES]


@pytest.mark.parametrize(
    argnames="mapper_id",
    argvalues=[mapper_id for mapper_id in abis_mapping.get_mappers()],
)
def test_registered_has_test_case(mapper_id: str, case_template_ids: list[str]) -> None:
    """Tests all registered mapper has a corresponding test case."""
    assert mapper_id in case_template_ids


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

    def test_get_mapper(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests that we can retrieve a mapper based on its template ID"""
        # Test Real Template IDs
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None
        assert issubclass(real_mapper, abis_mapping.base.mapper.ABISMapper)

    def test_get_template(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests able to retrieve template file."""
        # Test Real Template ID
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None
        template = real_mapper.template()
        assert isinstance(template, pathlib.Path)
        assert template.is_file()

    def test_get_metadata(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests able to retrieve template metadata"""
        # Test Real Template ID
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None
        metadata = real_mapper.metadata()
        assert isinstance(metadata, dict)

    def test_metadata_id_match(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests the metadata id matches the mapper id"""
        # Retrieve mapper
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None

        # Retrieve metadata
        metadata = real_mapper.metadata()
        assert metadata.get("id") == real_mapper.template_id

    def test_get_schema(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests able to retrieve template schema."""
        # Test Real Template ID
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None

        # Retrieve schema
        schema = real_mapper.schema()
        assert isinstance(schema, dict)

    def test_get_instructions(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests able to retrieve template instructions."""
        # Test Real Template ID
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None
        instructions = real_mapper.instructions()
        assert isinstance(instructions, pathlib.Path)
        assert instructions.is_file()

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

    def test_allows_extra_cols(
        self,
        test_params: conftest.TemplateTestParameters,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests to make sure that all required checks are in place to allow extra columns.

        Args:
            test_params (conftest.TemplateTestParameters): Test parameters for template
                under test.
            mocker (pytest_mock.MockerFixture): The mocker fixture.
        """
        # Patch validate
        mocked_resource = mocker.patch("frictionless.Resource")
        mocked_validate: unittest.mock.Mock = mocked_resource.return_value.validate

        # Load data
        data = test_params.mapping_cases[0].data.read_bytes()

        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper is not None

        # Validate
        _ = mapper().apply_validation(data)

        # Assert called
        mocked_resource.assert_called()
        mocked_validate.assert_called_once()

        if test_params.allows_extra_cols:
            # Check to ensure that appropriate arguments set during call to validate method.
            checklist: frictionless.Checklist = mocked_validate.call_args.kwargs.get("checklist")
            assert set(checklist.skip_errors) == {"extra-label", "extra-cell"}
