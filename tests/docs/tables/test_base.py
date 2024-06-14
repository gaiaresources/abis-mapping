"""Provides unit tests for the tabler module"""

# Standard
import io

# Third party
import pytest

# Local
from docs import tables


def test_tabler_init_raises_invalid_template_id() -> None:
    """Tests initialisation raises on invalid template id."""

    with pytest.raises(ValueError):
        tables.fields.FieldTabler("FAKE_ID")


class TestMarkdownDictWriter:
    """Test suite for the MarkdownDictWriter class"""
    def test_writeheader(self) -> None:
        """Tests writeheader method."""
        # Create memory io to write to
        output = io.StringIO()

        # Create MarkdownDictWriter object
        writer = tables.base.MarkdownDictWriter(output, ["Some", "Header", "Fields"])

        # Invoke
        writer.writeheader()

        # Assert
        assert output.getvalue() == (
            "|Some|Header|Fields|\n"
            "|---|---|---|\n"
        )

    def test_writerow(self) -> None:
        """Tests writerow method."""
        # Create memory io to write to
        output = io.StringIO()

        # Create writer
        writer = tables.base.MarkdownDictWriter(output, ["Some", "Header", "Fields"])

        # Test data
        data = {"Some": "Value 1", "Header": 2.0, "Fields": True}

        # Invoke
        writer.writerow(data)

        # Assert
        assert output.getvalue() == (
            "|Value 1|2.0|True|\n"
        )
