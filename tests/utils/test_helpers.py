"""Tests for the test helpers themselves"""

# Third-party
import pydantic
import pytest

# Local
from abis_mapping import settings
from tests import helpers


def test_override_settings() -> None:
    """Test override_settings helper."""
    # initial value
    assert settings.SETTINGS.DEFAULT_TARGET_CRS == "GDA2020"
    # start first override
    with helpers.override_settings(DEFAULT_TARGET_CRS="A1"):
        # first override value
        assert settings.SETTINGS.DEFAULT_TARGET_CRS == "A1"
    # initial value should be restored
    assert settings.SETTINGS.DEFAULT_TARGET_CRS == "GDA2020"

    # override multiple settings
    with helpers.override_settings(
        DEFAULT_WKT_ROUNDING_PRECISION=99,
        DEFAULT_TARGET_CRS="B2",
    ):
        assert settings.SETTINGS.DEFAULT_WKT_ROUNDING_PRECISION == 99
        assert settings.SETTINGS.DEFAULT_TARGET_CRS == "B2"
    # initial settings are restored
    assert settings.SETTINGS.DEFAULT_WKT_ROUNDING_PRECISION == 8
    assert settings.SETTINGS.DEFAULT_TARGET_CRS == "GDA2020"


def test_override_settings_nested() -> None:
    """Test override_settings helper with nested usage."""
    # initial value
    assert settings.SETTINGS.DEFAULT_TARGET_CRS == "GDA2020"
    # start first override
    with helpers.override_settings(DEFAULT_TARGET_CRS="A1"):
        # first override value
        assert settings.SETTINGS.DEFAULT_TARGET_CRS == "A1"
        # nested override
        with helpers.override_settings(DEFAULT_TARGET_CRS="B2"):
            # nested override value
            assert settings.SETTINGS.DEFAULT_TARGET_CRS == "B2"
        # first override value should be restored
        assert settings.SETTINGS.DEFAULT_TARGET_CRS == "A1"
    # initial value should be restored
    assert settings.SETTINGS.DEFAULT_TARGET_CRS == "GDA2020"


def test_override_settings_invalid() -> None:
    """Test override_settings helper with bad inputs."""
    # unknown setting
    with pytest.raises(pydantic.ValidationError) as error:
        with helpers.override_settings(NOT_A_SETTING="foo"):
            pass
    assert error.value.error_count() == 1
    assert error.value.errors()[0]["type"] == "extra_forbidden"

    # bad value for setting
    with pytest.raises(pydantic.ValidationError) as error:
        with helpers.override_settings(DEFAULT_WKT_ROUNDING_PRECISION="not_an_int"):
            pass
    assert error.value.error_count() == 1
    assert error.value.errors()[0]["type"] == "int_parsing"
