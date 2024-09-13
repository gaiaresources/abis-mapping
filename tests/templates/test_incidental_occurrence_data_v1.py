"""Unit tests specific to the incidental_occurrence_data-v1.0.0.csv template."""

# Standard
import pathlib

# Local
import abis_mapping.templates.incidental_occurrence_data.mapping


# Alias mapper for the tests
mapper = abis_mapping.templates.incidental_occurrence_data.mapping.IncidentalOccurrenceMapper


def test_instructions() -> None:
    """Test the instructions method."""
    # Get mapper and invoke
    instructions = mapper.instructions()

    # Should return a file path
    assert isinstance(instructions, pathlib.Path)
    assert instructions.is_file()


def test_metadata() -> None:
    """Test the metadata method."""
    # Get mapper and invoke
    metadata = mapper.metadata()

    # Should return instructions path for instructions_url
    assert metadata["instructions_url"] == str(mapper.instructions())
