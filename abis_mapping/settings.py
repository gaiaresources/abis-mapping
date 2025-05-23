"""All non-sensitive project-wide configuration parameters"""

# Third-party
import pydantic_settings


class _Settings(pydantic_settings.BaseSettings):
    """Model for defining default project-wide settings."""

    model_config = pydantic_settings.SettingsConfigDict(
        # Don't let settings object be mutated, since it is stored globally on the module
        frozen=True,
    )

    # Default precision for rounding WKT coordinates when serializing.
    DEFAULT_WKT_ROUNDING_PRECISION: int = 8

    # Default CRS to transform all input geometry to.
    DEFAULT_TARGET_CRS: str = "GDA2020"

    # Base url for the instructions site
    INSTRUCTIONS_BASE_URL: str = "https://gaiaresources.github.io/abis-mapping/"

    # The version of the documents to be selected
    INSTRUCTIONS_VERSION: str = "dev"


# If changing via environment variable or .env file prefix name with 'ABIS_MAPPING_'
SETTINGS = _Settings(
    _env_prefix="ABIS_MAPPING_",
    _env_file="abis_mapping.env",
)
# NOTE environment variables and .env files are ignored when running the test suite.
