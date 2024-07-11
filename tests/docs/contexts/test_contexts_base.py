"""Provides unit tests for the contexts base module."""

# Standard
import unittest.mock

# Third-part
import pytest

# Local
from docs import contexts


def test_register(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests the register function.

    Args:
        mocked_mapper (unittest.mock.MagicMock): The mocked mapper.
    """
    # Invoke
    contexts.base.register("some_id", {"some": "context"})

    try:
        # Assert context exists in registry
        assert contexts.base._registry.get("some_id") is not None

    finally:
        # Cleanup registry
        contexts.base._registry.pop("some_id")


def test_register_duplicate_id(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests the register function raises an exception when a duplicate id is registered.

    Args:
        mocked_mapper (unittest.mock.MagicMock): The mocked mapper.
    """
    # Register context
    contexts.base.register("some_id", {"some": "context"})

    # Should raise attempting to register using same id
    with pytest.raises(KeyError):
        contexts.base.register("some_id", {"another": "context"})

    # Cleanup registry
    contexts.base._registry.pop("some_id")


def test_register_no_mapper() -> None:
    """Tests the register function raises an exception when no mapper is registered."""
    # Should raise ValueError
    with pytest.raises(ValueError):
        contexts.base.register("DOES_NOT_EXIST", {"some": "context"})


def test_get_context(mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests the get_context function.

    Args:
        mocked_mapper (unittest.mock.MagicMock): The mocked mapper.
    """
    # Register context
    contexts.base.register("some_id", {"some": "context"})

    try:
        # Invoke
        ctx = contexts.base.get_context("some_id")

        # Assert
        assert ctx is not None
        assert ctx["some"] == "context"

    finally:
        # Cleanup registry
        contexts.base._registry.pop("some_id")
