"""Defines the models to describe template metadata."""

# Standard
import urllib.parse

# Third-party
import pydantic

# Local
from abis_mapping import settings


class TemplateMetadata(pydantic.BaseModel):
    """Model for the template `metadata.json` file."""

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
    template_status: str

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
            base=str(settings.Settings().INSTRUCTIONS_BASE_URL),
            url="/".join([settings.Settings().INSTRUCTIONS_VERSION, self.id]),
        )
        # Perform validation
        pydantic.AnyUrl(str_url)

        # Return string
        return str_url
