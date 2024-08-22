"""Provides fixtures and helpers for the unit tests."""

# Standard
import unittest.mock
import pathlib

# Third-party
import pytest
import pytest_mock


@pytest.fixture
def mocked_mapper(mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
    """Provides a mocked mapper fixture.

    Args:
        mocker (pytest_mock.MockerFixture): Pytest mocker fixture.

    Returns:
        unittest.mock.MagicMock: Mocked mapper fixture.
    """
    # Patch get_mapper
    mocked_mapper = mocker.patch("abis_mapping.base.mapper.get_mapper")

    # Patch schema
    mocked_mapper.return_value.schema.return_value = {
        "fields": [
            {
                "name": "someName",
                "title": "Some Title",
                "description": "Some description",
                "example": "SOME EXAMPLE",
                "type": "string",
                "format": "default",
                "constraints": {
                    "required": True,
                    "enum": [
                        "SOME EXAMPLE",
                        "Option 2",
                        "plan C",
                    ]
                },
                "vocabularies": [
                    "SOME_VOCAB",
                ],
            },
            {
                "name": "anotherName",
                "title": "Another Title",
                "description": "Another description",
                "example": "ANOTHER EXAMPLE",
                "type": "string",
                "format": "default",
                "url": "http://example.com",
                "constraints": {
                    "required": True,
                    "enum": [
                        "ANOTHER EXAMPLE",
                        "Option 22",
                        "plan CC",
                    ]
                },
            }
        ]
    }

    # Patch root_dir
    mocked_mapper.return_value.return_value.root_dir.return_value = pathlib.Path(__file__).parent / "data"

    # Return
    return mocked_mapper
