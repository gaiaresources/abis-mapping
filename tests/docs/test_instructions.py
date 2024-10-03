"""Provides unit tests for the instructions module."""

# Standard
import pathlib
import unittest.mock

# Third-party
import jinja2
import pytest
import pytest_mock

# Local
from docs import contexts
from docs import instructions


def test_render_index() -> None:
    """Tests the render_index function."""
    # Invoke
    actual = instructions.render_index(pathlib.Path("some_page/some_markdown.md"))

    # Assert no double braces remaining in html
    assert "{{" not in actual
    assert "}}" not in actual

    # Assert page_name replaced
    assert "page_name" not in actual
    with open("docs/templates/index.html", "r") as f:
        template_contents = f.read()
    pn_count = template_contents.count("page_name")
    assert actual.count("some_markdown") == pn_count


def test_build_instructions(mocker: pytest_mock.MockFixture, mocked_mapper: unittest.mock.MagicMock) -> None:
    """Tests the build_instructions function.

    Args:
        mocker (pytest_mock.MockFixture): Pytest mocker fixture.
        mocked_mapper (unittest.mock.MagicMock): Mocked mapper.
    """
    # Patch get_context
    ctx_mock = mocker.patch.object(contexts.base, "get_context", return_value={"some": "value"})

    # Patch get_template
    template_mock = mocker.MagicMock()
    mocker.patch.object(jinja2.Environment, "get_template", return_value=template_mock)
    template_mock.render = mocker.MagicMock()

    # Invoke
    instructions.build_instructions("some id")

    # Assert project version set and template render called
    template_mock.render.assert_called()
    assert ctx_mock.return_value.get("project_version") is not None


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
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"), autoescape=True)

        # Invoke
        src, pth, rld = instructions.MapperLoader("some_id").get_source(environment=env, template="blank_template.md")

        # Assert
        assert isinstance(pth, str)
        assert pth.split("/")[-2:] == ["templates", "blank_template.md"]
        assert rld is not None
        assert rld() is True

    def test_get_source_invalid_mapper(self) -> None:
        """Tests get_source method raises exception for invalid mapper."""
        # Define bad mapper name and env
        bad_mapper_id = "NOT_A_MAPPER_ID"
        env = jinja2.Environment(loader=instructions.MapperLoader(bad_mapper_id), autoescape=True)

        # Should raise ValueError
        with pytest.raises(ValueError):
            instructions.MapperLoader(bad_mapper_id).get_source(env, bad_mapper_id)

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
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"), autoescape=True)

        # Invoke
        src, pth, rld = instructions.MapperLoader("some_id").get_source(
            environment=env, template="BASE_TEMPLATE blank_template.md"
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
        env = jinja2.Environment(loader=instructions.MapperLoader("some id"), autoescape=True)

        with pytest.raises(jinja2.exceptions.TemplateNotFound):
            # Invoke
            instructions.MapperLoader("some_id").get_source(environment=env, template="FAKE.md")
