"""Defines the models to describe template metadata."""

# Standard
import urllib.parse
import enum

# Third-party
import pydantic

# Local
from abis_mapping import settings

# Typing


class TemplateMetadataLifecycleStatus(enum.StrEnum):
    BETA = "beta"
    CURRENT = "current"
    DEPRECATED = "deprecated"


class TemplateMetadata(pydantic.BaseModel):
    """Model for the template `metadata.json` file."""

    model_config = pydantic.ConfigDict(
        # Frozen because this class is returned by the cached ABISMapper.metadata() method
        frozen=True,
    )

    name: str
    label: str
    version: str
    description: str
    biodiversity_type: str
    spatial_type: str
    file_type: str
    sampling_type: str
    template_url: str
    schema_url: str
    template_lifecycle_status: TemplateMetadataLifecycleStatus

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        """Getter for the `id` field."""
        return f"{self.name}-v{self.version}.{self.file_type.lower()}"

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def instructions_url(self) -> str:
        """Getter for the `instructions_url` field.

        Returns:
            str: URL for instructions of the template

        Raises:
            pydantic.ValidationError: If url is not valid to
                AnyUrl spec.
        """
        # Create string representation
        str_url = urllib.parse.urljoin(
            base=settings.SETTINGS.INSTRUCTIONS_BASE_URL,
            url="/".join([settings.SETTINGS.INSTRUCTIONS_VERSION, self.id]),
        )
        # Perform validation
        pydantic.AnyUrl(str_url)

        # Return string
        return str_url
