"""Unit tests specific to the incidental_occurrence_data-v1.0.0.csv template."""

# Standard
import pathlib

# Local
import abis_mapping.templates.incidental_occurrence_data.mapping


def test_instructions() -> None:
    """Tests the instructions method."""
    # Get mapper and invoke
    mapper = abis_mapping.templates.incidental_occurrence_data.mapping.IncidentalOccurrenceMapper
    instructions = mapper.instructions()

    # Should return a file path
    assert isinstance(instructions, pathlib.Path)
    assert instructions.is_file()
