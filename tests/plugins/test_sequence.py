"""Provides Unit Tests for the `abis_mapping.plugins.sequence` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_sequence_plugin() -> None:
    """Tests the Sequence Plugin"""
    # Instantiate the Plugin
    plugin = plugins.sequence.SequencePlugin()

    # Incorrect Type
    field = frictionless.Field(type="any")
    result = plugin.create_type(field)
    assert result is None

    # Correct Type
    field = frictionless.Field(type="sequence")
    result = plugin.create_type(field)
    assert isinstance(result, plugins.sequence.SequenceType)


def test_sequence_type() -> None:
    """Tests the Sequence Type"""
    # Instantiate the Type
    type = plugins.sequence.SequenceType(field=frictionless.Field())

    # Read Invalid Cells
    assert type.read_cell(123) is None

    # Read Valid Cells
    assert type.read_cell("a") == ["a"]
    assert type.read_cell(["a"]) == ["a"]
    assert type.read_cell("a b c") == ["a", "b", "c"]
    assert type.read_cell(["a", "b", "c"]) == ["a", "b", "c"]

    # Write Cell
    assert type.write_cell(["a"]) == "a"
    assert type.write_cell(["a", "b", "c"]) == "a b c"
