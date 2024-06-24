"""Provides unit tests for the vocabs module."""

# Standard
import io
import unittest.mock

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
        'Template field name,Preferred label,Definition,Alternate label\r\n'
        'someName,SOME LABEL,Some description.,ANOTHER LABEL\r\n'
        '\n'
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
    tabler = tables.vocabs.VocabTabler("some_id")

    # Invoke
    actual = tabler.generate_table(as_markdown=True)

    # Assert
    assert actual == (
        '|Template field name|Preferred label|Definition|Alternate label|\n'
        '|:---|:---|:---|:---|\n'
        '|<a name="someName-vocabularies"></a>someName|SOME LABEL|Some description.|ANOTHER LABEL|\n'
    )
