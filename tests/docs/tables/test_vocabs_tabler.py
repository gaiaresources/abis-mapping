"""Provides unit tests for the vocabs module."""

# Standard
import io
import unittest.mock

# Third-party
import pytest
import pytest_mock

# Local
from docs import tables


def test_generate_table(
    mocked_mapper: unittest.mock.MagicMock,
    mocked_vocab: unittest.mock.MagicMock,
) -> None:
    """Tests generate_table method.

    Args:
        mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
        mocked_vocab (unittest.mock.MagicMock): Mocked vocab fixture.
    """
    # Create an in memory io
    dest = io.StringIO()

    # Create a tabler
    tabler = tables.vocabs.VocabTabler("some_id")

    # Invoke
    tabler.generate_table(
        dest=dest,
    )

    # Assert
    assert dest.getvalue() == (
        "Template field name,Preferred label,Definition,Alternate label\r\n"
        "someName,SOME LABEL,Some description.,ANOTHER LABEL\r\n"
        "\n"
    )


def test_generate_table_markdown(
    mocked_mapper: unittest.mock.MagicMock,
    mocked_vocab: unittest.mock.MagicMock,
) -> None:
    """Tests generate_table method with markdown output.

    Args:
        mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
        mocked_vocab (unittest.mock.MagicMock): Mocked vocab fixture.
    """
    # Create a tabler
    tabler = tables.vocabs.VocabTabler("some_id", format="markdown")

    # Invoke
    actual = tabler.generate_table()

    # Assert
    assert actual == (
        "|Template field name|Preferred label|Definition|Alternate label|\n"
        "|:---|:---|:---|:---|\n"
        '|<a name="someName-vocabularies"></a>someName|SOME LABEL|Some description.|ANOTHER LABEL|\n'
    )


class TestTBC:
    """Tests the table generation for vocabs with no terms."""

    @pytest.fixture
    def mocked_vocab(self, mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
        """Provides a mocked term fixture.

        Args:
            mocker (pytest_mock.MockerFixture): Pytest mocker fixture.

        Returns:
            unittest.mock.MagicMock: Mocked term fixture.
        """
        # Patch get_vocab
        mocked_vocab = mocker.patch("abis_mapping.utils.vocabs.get_vocab")

        # Patch terms - simulating a vocab with no terms
        mocked_vocab.return_value.terms = ()

        # Return
        return mocked_vocab

    def test_generate_table_tbc(
        self,
        mocked_mapper: unittest.mock.MagicMock,
        mocked_vocab: unittest.mock.MagicMock,
    ) -> None:
        """Tests generate_table method.

        Args:
            mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
            mocked_vocab (unittest.mock.MagicMock): Mocked vocab fixture.
        """
        # Create an in memory io
        dest = io.StringIO()

        # Create a tabler
        tabler = tables.vocabs.VocabTabler("some_id")

        # Invoke
        tabler.generate_table(
            dest=dest,
        )

        # Assert
        assert dest.getvalue() == (
            "Template field name,Preferred label,Definition,Alternate label\r\n" "someName,TBC,TBC,\r\n" "\n"
        )

    def test_generate_table_markdown(
        self,
        mocked_mapper: unittest.mock.MagicMock,
        mocked_vocab: unittest.mock.MagicMock,
    ) -> None:
        """Tests generate_table method with markdown output.

        Args:
            mocked_mapper (unittest.mock.MagicMock): Mocked mapper fixture.
            mocked_vocab (unittest.mock.MagicMock): Mocked vocab fixture.
        """
        # Create a tabler
        tabler = tables.vocabs.VocabTabler("some_id", format="markdown")

        # Invoke
        actual = tabler.generate_table()

        # Assert
        assert actual == (
            "|Template field name|Preferred label|Definition|Alternate label|\n"
            "|:---|:---|:---|:---|\n"
            '|<a name="someName-vocabularies"></a>someName|TBC|TBC||\n'
        )
