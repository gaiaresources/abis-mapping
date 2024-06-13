"""Provides fixtures and helpers for the unit tests."""

# Standard
import unittest.mock

# Third-party
import pytest
import pytest_mock
import rdflib

# Local
from abis_mapping import utils


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
            }
        ]
    }

    # Return
    return mocked_mapper


@pytest.fixture
def mocked_vocab(mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
    """Provides a mocked term fixture.

    Args:
        mocker (pytest_mock.MockerFixture): Pytest mocker fixture.

    Returns:
        unittest.mock.MagicMock: Mocked term fixture.
    """
    # Patch get_vocab
    mocked_vocab = mocker.patch("abis_mapping.utils.vocabs.get_vocab")

    # Patch terms
    mocked_vocab.return_value.terms = (
        utils.vocabs.Term(
            labels=("SOME LABEL", "ANOTHER LABEL", ),
            iri=rdflib.URIRef("https://example.org/some-term"),
            description="Some description.",
        ),
    )

    # Return
    return mocked_vocab
