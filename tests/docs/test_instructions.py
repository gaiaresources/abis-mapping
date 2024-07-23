"""Provides unit tests for the instructions module."""

# Standard
import unittest.mock

# Third-party
import jinja2
import pytest
import pytest_mock

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

    def test_get_source_base_template(
        self,
        mocked_mapper: unittest.mock.MagicMock,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests get_source using BASE_TEMPLATE keyword.

        Args:
            mocked_mapper (unittest.mock.MagicMock): Mocked mapper.
            mocker (pytest_mock.MockerFixture): The pytest MockerFixture.
        """
        # Patch and get mock for the Filesystem loader get_source method
        mocked_fs_get_source = mocker.patch.object(jinja2.FileSystemLoader, "get_source")
        mocked_fs_get_source.return_value = ("some src", "some_file.md", lambda: True)

        # Create jinja env
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"))

        # Invoke
        src, pth, rld = instructions.MapperLoader("some_id").get_source(
            environment=env,
            template="BASE_TEMPLATE blank_template.md"
        )

        # Should call mock with the BASE_TEMPLATE keyword stripped.
        mocked_fs_get_source.assert_called_with(env, "blank_template.md")
        assert src == "some src"
        assert pth == "some_file.md"
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
