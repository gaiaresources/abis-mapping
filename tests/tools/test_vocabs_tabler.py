"""Provides unit tests for the vocabs module."""

# Standard
import io
import unittest.mock

# Local
import tools.vocabs


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
    tabler = tools.vocabs.VocabTabler("some_id")

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

