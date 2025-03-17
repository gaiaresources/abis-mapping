"""Provided unit tests common across all templates."""

# Standard
import pathlib
import unittest.mock

# Third-party
import pytest
import pytest_mock
import frictionless
import pyproj

# Local
import abis_mapping
import abis_mapping.base
import abis_mapping.models
from tests.templates import conftest

# Typing
from collections.abc import Mapping


def test_registered_templates() -> None:
    """Test to check/document which templates are registered."""
    assert sorted(abis_mapping.registered_ids()) == [
        "incidental_occurrence_data-v3.0.0.csv",
        "incidental_occurrence_delete-v1.0.0.csv",
        "survey_metadata-v3.0.0.csv",
        "survey_occurrence_data-v3.0.0.csv",
        "survey_site_data-v3.0.0.csv",
        "survey_site_visit_data-v3.0.0.csv",
    ]


@pytest.fixture(scope="module")
def case_template_ids() -> list[str]:
    """Test fixture that returns all test case template ids."""
    return [tc.template_id for tc in conftest.TEST_CASES]


@pytest.mark.parametrize(
    argnames="mapper_id",
    argvalues=sorted(abis_mapping.registered_ids()),
)
def test_registered_has_test_case(mapper_id: str, case_template_ids: list[str]) -> None:
    """Tests all registered mapper has a corresponding test case."""
    assert mapper_id in case_template_ids


@pytest.mark.parametrize(
    argnames="test_params",
    argvalues=[tc for tc in conftest.TEST_CASES],
    ids=[tc.template_id for tc in conftest.TEST_CASES],
)
class TestTemplateBasicSuite:
    def test_template_registered(
        self,
        test_params: conftest.TemplateTestParameters,
    ) -> None:
        """Tests that the supplied template id is registered."""
        assert test_params.template_id in abis_mapping.registered_ids()

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
        assert isinstance(metadata, abis_mapping.models.metadata.TemplateMetadata)

    def test_metadata_id_match(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests the metadata id matches the mapper id"""
        # Retrieve mapper
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None

        # Retrieve metadata
        metadata = real_mapper.metadata()
        assert metadata.id == real_mapper().template_id

    def test_get_schema(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests able to retrieve template schema."""
        # Test Real Template ID
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None

        # Retrieve schema
        schema = real_mapper.schema()
        assert isinstance(schema, dict)

    def test_geodetic_datum_proj_supported(self, test_params: conftest.TemplateTestParameters) -> None:
        """Test that all enumerated values for geodeticDatum are supported by proj."""
        # Get mapper
        real_mapper = abis_mapping.base.mapper.get_mapper(test_params.template_id)
        assert real_mapper is not None

        # Get descriptor
        desc = real_mapper().schema()

        # Filter out geodetic datum fields and their enumerable values
        gd_field = [gd for gd in desc["fields"] if gd["name"] == "geodeticDatum"]
        if len(gd_field) > 0:
            assert len(gd_field) == 1
            gds = {gd for gd in gd_field[0]["constraints"]["enum"]}
            for gd in gds:
                # Ensure geodetic datum string supported by pyproj
                assert pyproj.CRS(gd) is not None

    def test_metadata_sampling_type(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests the metadata sampling type set correctly"""
        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get metadata
        metadata = mapper().metadata()

        # Confirm field set correctly
        assert metadata.sampling_type == test_params.metadata_sampling_type

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

    def test_schema_validation(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests that the schema method produces valid pydantic model."""
        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get schema dictionary
        descriptor = mapper().schema()

        # Overall schema check
        valid_schema = abis_mapping.models.schema.Schema.model_validate(descriptor)
        assert valid_schema
        # Should have no extra fields defined but if it does then needs to
        # be reviewed and decided to be added to model
        assert valid_schema.__pydantic_extra__ == {}

        # Iterate through fields and ensure they validate
        for field in descriptor["fields"]:
            valid_field = abis_mapping.models.schema.Field.model_validate(field, strict=True)
            assert valid_field

    def test_fields(self, test_params: conftest.TemplateTestParameters) -> None:
        """Test that the fields() method works"""
        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # This should raise an error if there are any errors in the field json.
        fields = mapper.fields()
        assert isinstance(fields, Mapping)

        for key, field in fields.items():
            assert isinstance(key, str)
            assert isinstance(field, abis_mapping.models.schema.Field)

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
        error_codes = [code for codes in report.flatten(["type"]) for code in codes]
        assert "table-dimensions" in error_codes

    def test_blank_template(self, test_params: conftest.TemplateTestParameters) -> None:
        """Tests blank templates are free of errors."""
        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Load data
        data = mapper.template().read_bytes()

        # Perform validation
        report = mapper().apply_validation(data)
        error_codes = [code for codes in report.flatten(["type"]) for code in codes]

        # Confirm header is as expected
        assert "extra-label" not in error_codes
        assert "missing-label" not in error_codes
        assert "blank-label" not in error_codes
        assert "duplicate-label" not in error_codes
        assert "incorrect-label" not in error_codes
        assert "blank-header" not in error_codes

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

        # Mock both methods for getting schema
        mocked_extra_fields_schema = mocker.patch.object(
            target=abis_mapping.base.mapper.ABISMapper,
            attribute="extra_fields_schema",
        )
        mocked_regular_fields_schema = mocker.patch.object(
            target=abis_mapping.base.mapper.ABISMapper,
            attribute="regular_fields_schema",
        )
        schema = frictionless.Schema()
        mocked_extra_fields_schema.return_value = schema
        mocked_regular_fields_schema.return_value = schema

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

        # The following asserts determine that the extra fields schema was used in creating the resource
        if test_params.allows_extra_cols:
            mocked_extra_fields_schema.assert_called_once()
        # Or if the template doesn't allow extra, check the regular method was called
        else:
            mocked_regular_fields_schema.assert_called_once()

        mocked_resource.assert_any_call(source=data, schema=schema, format="csv", encoding="utf-8")
