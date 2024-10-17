"""Provides unit tests for the metadata module."""

# Standard
import json

# Third-party
import pytest

# Local
from abis_mapping import settings
from abis_mapping import types
from abis_mapping.types.metadata import TemplateMetadataLifecycleStatus


class TestTemplateMetadata:
    """Test suite for the TemplateMetadata model."""

    @pytest.fixture
    def template_metadata(self) -> types.metadata.TemplateMetadata:
        """Provides a template metadata model."""
        # Create and return
        return types.metadata.TemplateMetadata(
            name="someName",
            label="someLabel",
            version="someVersion",
            description="Some description",
            biodiversity_type="someBiodiversityType",
            spatial_type="someSpatialType",
            file_type="SOMETYPE",
            sampling_type="someSamplingType",
            template_url="http://example.com/some_template_url",
            schema_url="http://example.com/some_schema_url",
            template_lifecycle_status=TemplateMetadataLifecycleStatus.CURRENT,
        )

    def test_id(
        self,
        template_metadata: types.metadata.TemplateMetadata,
    ) -> None:
        """Tests the id computed property.

        Args:
            template_metadata (types.metadata.TemplateMetadata): TemplateMetadata model
                instance fixture.
        """
        # Expected id value
        expected = "someName-vsomeVersion.sometype"

        # Assert
        assert template_metadata.id == expected

    def test_instructions_url(
        self,
        template_metadata: types.metadata.TemplateMetadata,
    ) -> None:
        """Tests the instructions url computed property.

        Args:
              template_metadata (types.metadata.TemplateMetadata): TemplateMetadata model
                instance fixture.
        """
        # Expected instructions url
        expected = f"{settings.Settings().INSTRUCTIONS_BASE_URL}{settings.Settings().INSTRUCTIONS_VERSION}/{template_metadata.id}"

        # Assert as expected
        assert template_metadata.instructions_url == expected
        assert template_metadata.model_dump()["instructions_url"] == expected

    def test_serialization(
        self,
        template_metadata: types.metadata.TemplateMetadata,
    ) -> None:
        """Tests the serialization method."""
        # json encode/decode
        python_val = json.loads(template_metadata.model_dump_json())
        # compare pydantic models
        assert types.metadata.TemplateMetadata(**python_val) == template_metadata
