"""Provides unit tests for the instructions module."""

# Standard
import unittest.mock

# Third-party
import jinja2
import pytest

# Local
from docs import instructions


class TestMapperLoader:
    def test_get_source(
        self,
        mocked_mapper: unittest.mock.MagicMock,
    ) -> None:
        """Tests get_source method.

        Args:
            mocked_mapper (unittest.mock.MagicMock): Mocked mapper.
        """
        # Create jinja env
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"))

        # Invoke
        src, pth, rld = instructions.MapperLoader("some_id").get_source(environment=env, template="blank_template.md")

        # Assert
        assert isinstance(pth, str)
        assert pth.split("/")[-2:] == ["templates", "blank_template.md"]
        assert rld is not None
        assert rld() is True

    def test_get_source_invalid_template(
        self,
        mocked_mapper: unittest.mock.MagicMock,
    ) -> None:
        """Tests get_source method raises exception.

        Args:
            mocked_mapper (unittest.mock.MagicMock): Mocked mapper.
        """
        # Create jinja env
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"))

        with pytest.raises(jinja2.exceptions.TemplateNotFound):
            # Invoke
            instructions.MapperLoader("some_id").get_source(environment=env, template="FAKE.md")
