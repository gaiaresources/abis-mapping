"""Helper utilities for testing."""

# Standard Library
import collections.abc
import contextlib

# Third-party
import pydantic_settings

# Local
from abis_mapping import settings


@contextlib.contextmanager
def override_settings(**overrides: object) -> collections.abc.Iterator[None]:
    """Context manager to override any number of settings,
    and restore the original settings at the end.

    This is non-trivial since the settings object is frozen.

    Args:
        **overrides:
            Pass settings to override as keyword arguments.

    Returns:
        Context manager to override the settings.
    """
    # Get current settings.
    initial_settings = settings.SETTINGS
    # Make new settings object and override settings with it
    settings.SETTINGS = TestSettings(**(initial_settings.model_dump() | overrides))

    yield

    # Restore the original settings on context exit
    settings.SETTINGS = initial_settings


class TestSettings(settings._Settings):
    """Version of the settings to use in the test suite."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[pydantic_settings.BaseSettings],
        init_settings: pydantic_settings.PydanticBaseSettingsSource,
        env_settings: pydantic_settings.PydanticBaseSettingsSource,
        dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
        file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for loading the settings values.
        """
        # In the tests, ignore all env, dotenv and secrets settings.
        # This is so the test suite is deterministic and isolated,
        # and won't be effected by any settings a particular developer has set locally.
        return (init_settings,)
