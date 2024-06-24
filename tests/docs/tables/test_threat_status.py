"""Provides unit tests for the threat_status module."""

# Standard
import unittest.mock
import io

# Third-party
import rdflib
import pytest

# Local
from docs import tables
from abis_mapping import utils


class TestThreatStatusTabler:
    @pytest.fixture
    def mocked_mapper(self, mocked_mapper: unittest.mock.MagicMock) -> unittest.mock.MagicMock:
        """Modifies and returns a mocked mapper.

        Args:
            mocked_mapper (unittest.mock.MagicMock): mocked mapper.

        Returns:
            unittest.mock.MagicMock: mocked mapper.
        """
        # Modify the mocked mapper schema
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
                        # Threat status required for tabler to work
                        "THREAT_STATUS",
                    ],
                }
            ]
        }

        return mocked_mapper

    @pytest.fixture
    def mocked_vocab(self, mocked_vocab: unittest.mock.MagicMock) -> unittest.mock.MagicMock:
        """Modifies and returns a mocked vocabulary.

        Args:
            mocked_vocab (unittest.mock.MagicMock): Mocked vocabulary.

        Returns:
            unittest.mock.MagicMock: Mocked vocabulary.
        """
        # Modify the mocked vocab terms
        mocked_vocab.return_value.terms = (
            utils.vocabs.Term(
                labels=("SOME JURISDICTION/SOME STATUS", "SJUR/SSTAT", ),
                iri=rdflib.URIRef("https://example.org/some-term"),
                description="Some description.",
            ),
        )

        return mocked_vocab

    def test_generate_table(
        self,
        mocked_mapper: unittest.mock.MagicMock,
        mocked_vocab: unittest.mock.MagicMock,
    ) -> None:
        """Tests generation of table.

        Args:
            mocked_mapper (unittest.mock.MagicMock): The mocked mapper object.
            mocked_vocab (unittest.mock.MagicMock): The mocked vocab object.
        """
        # Create tabler
        tabler = tables.threat_status.ThreatStatusTabler("some id")

        # Create in memory io
        dest = io.StringIO()

        # Generate table
        tabler.generate_table(dest)

        # Assert
        assert dest.getvalue() == (
            "conservationJurisdiction,threatStatus,threatStatus alternative labels\r\n"
            "SOME JURISDICTION,SOME STATUS,SSTAT\r\n"
            "\n"
        )

    def test_generate_table_markdown(
        self,
        mocked_mapper: unittest.mock.MagicMock,
        mocked_vocab: unittest.mock.MagicMock,
    ) -> None:
        """Tests generation of a markdown table.

        Args:
            mocked_mapper (unittest.mock.MagicMock): The mocked mapper object.
            mocked_vocab (unittest.mock.MagicMock): The mocked vocab object.
        """
        # Create tabler
        tabler = tables.threat_status.ThreatStatusTabler("some id")

        # Generate table
        actual = tabler.generate_table(as_markdown=True)

        # Assert
        assert actual == (
            "|conservationJurisdiction|threatStatus|threatStatus alternative labels|\n"
            "|:---|:---|:---|\n"
            "|SOME JURISDICTION|SOME STATUS|SSTAT|\n"
        )


def test_tabler_raises_no_threat_status(
    mocked_mapper: unittest.mock.MagicMock,
) -> None:
    """Tests exception raised for mapper with no threat status vocab fields.

    Args:
        mocked_mapper (unittest.mock.MagicMock): The mocked mapper object.
    """
    # Catch expected error
    with pytest.raises(ValueError):
        # Create tabler
        tables.threat_status.ThreatStatusTabler("some id")
