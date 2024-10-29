"""Provides tests for the model_json module."""

# Standard
import json

# Third-party
import pydantic
import pytest
import pytest_mock

# Local
from docs import model_json


class FakeModel(pydantic.BaseModel):
    name: str


class InvalidModel:
    name: str


def test_import_model() -> None:
    """Tests the import_model function."""
    # Invoke
    result = model_json.import_model(f"{__name__}.FakeModel")

    # Should be a pydantic model and FakeModel above
    assert issubclass(result, pydantic.BaseModel)
    assert result is FakeModel


def test_import_model_invalid_path() -> None:
    """Tests import_model function with invalid path."""
    # Should raise ValueError
    with pytest.raises(ValueError, match=r"^Invalid path:"):
        model_json.import_model("NOT/A/PATH")


def test_import_model_invalid_model() -> None:
    """Tests import_model function with invalid model."""
    # Should raise ValueError with no cause
    with pytest.raises(ValueError, match=r"does not resolve to a pydantic model") as exc:
        model_json.import_model(f"{__name__}.InvalidModel")

    assert exc.value.__cause__ is None


def test_import_model_invalid_module() -> None:
    """Tests import_model function with invalid module."""
    # Should raise ValueError caused by ModuleNotFoundError
    with pytest.raises(ValueError) as exc:
        model_json.import_model("not.a.module")

    assert exc.value.__cause__.__class__ is ModuleNotFoundError


def test_import_model_invalid_attr() -> None:
    """Tests import_model function with invalid attribute."""
    # Should raise ValueError caused by AttributeError
    with pytest.raises(ValueError) as exc:
        model_json.import_model(f"{__name__}.NotAnAttr")

    assert exc.value.__cause__.__class__ is AttributeError


def test_create_json_schema(mocker: pytest_mock.MockerFixture) -> None:
    """Tests the create_json_schema function.

    Args:
        mocker: The mocker fixture.
    """
    # Patch open
    mocked_open = mocker.mock_open()
    mocker.patch("docs.model_json.open", mocked_open)

    # Invoke
    result = model_json.create_json_schema(FakeModel, "some/fake/path")

    # Assert
    assert result == json.dumps(FakeModel.model_json_schema(), indent=2)
    mocked_open.assert_called_with("some/fake/path", "w")
    handle = mocked_open()
    handle.write.assert_called_once()
