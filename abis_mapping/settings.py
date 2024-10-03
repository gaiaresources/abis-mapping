"""All non-sensitive project-wide configuration parameters"""

# Standard
import importlib.metadata

# Third-party
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Model for defining default project-wide settings."""

    # Default precision for rounding WKT coordinates when serializing.
    DEFAULT_WKT_ROUNDING_PRECISION: int = 8

    # Default CRS to transform all input geometry to.
    DEFAULT_TARGET_CRS: str = "GDA2020"

    # Base url for the instructions site
    INSTRUCTIONS_BASE_URL: str = "https://gaiaresources.github.io/abis-mapping/"

    # The version of the documents to be selected
    INSTRUCTIONS_VERSION: str = "dev"

    # Version parts
    MAJOR_VERSION: int = int(importlib.metadata.version("abis-mapping").split(".", 1)[0])

    # If changing via environment variable prefix name with 'ABIS_MAPPING_'
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="ABIS_MAPPING_")


SETTINGS = Settings()
