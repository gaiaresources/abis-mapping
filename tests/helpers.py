"""Helper utilities for testing."""

# Standard Library
import collections.abc
import contextlib

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
