"""Provides unit tests for the tabler module"""

# Standard
import io
import unittest.mock

# Third party
import pytest

# Local
from docs import tables


class TestBaseTabler:
    """Test suite for the BaseTabler class"""

    def test_init_raises_invalid_template_id(self) -> None:
        """Tests initialisation raises on invalid template id."""
        with pytest.raises(ValueError):
            tables.fields.FieldTabler("FAKE_ID")

    def test_init_raises_invalid_format(
        self,
        mocked_mapper: unittest.mock.MagicMock,
    ) -> None:
        """Tests constructor raises on invalid format.

        Args:
            mocked_mapper (unittest.mock.MagicMock): mocked mapper fixture.
        """
        # Shouldn't raise now using mocked mapper
        tables.fields.FieldTabler("some_id")
        with pytest.raises(ValueError):
            tables.fields.FieldTabler("some_id", format="notAFormat")  # type: ignore[arg-type]

    def test_supported_formats(self) -> None:
        """Tests supported_formats property method."""
        # Invoke
        result = tables.base.BaseTabler.supported_formats

        # Should be list of strings
        assert result == ["markdown", "csv"]


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
        assert output.getvalue() == "|Some|Header|Fields|\n|:---|:---|:---|\n"

    def test_writeheader_with_alignment(self) -> None:
        """Tests writeheader method with alignment."""
        # Create memory io to write to
        output = io.StringIO()

        # Create MarkdownDictWriter object
        writer = tables.base.MarkdownDictWriter(
            f=output,
            fieldnames=["Some", "Header", "Fields"],
            alignment=["left", "center", "right"],
        )

        # Invoke
        writer.writeheader()

        # Assert
        assert output.getvalue() == "|Some|Header|Fields|\n|:---|:---:|---:|\n"

    def test_writeheader_invalid_alignment_length(self) -> None:
        """Tests writeheader method with invalid alignment length."""
        # Create memory io to write to
        output = io.StringIO()

        # Create MarkdownDictWriter object should raise
        with pytest.raises(ValueError):
            tables.base.MarkdownDictWriter(
                f=output,
                fieldnames=["Some", "Header", "Fields"],
                alignment=["left", "center", "right", "right"],
            )

    def test_writeheader_invalid_alignment_type(self) -> None:
        """Tests writeheader method with invalid alignment type."""
        # Create memory io to write to
        output = io.StringIO()

        # Create MarkdownDictWriter object should raise
        with pytest.raises(ValueError):
            tables.base.MarkdownDictWriter(
                f=output,
                fieldnames=["Some", "Header", "Fields"],
                alignment=["everywhere", "center", "right"],
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
        assert output.getvalue() == ("|Value 1|2.0|True|\n")

    def test_writerows(self) -> None:
        """Tests the writerows method."""
        # Create memory io to write to
        output = io.StringIO()

        # Create writer
        writer = tables.base.MarkdownDictWriter(output, ["Some", "Header", "Fields"])

        # Test data
        data = [
            {"Some": "Value 1", "Header": 2.0, "Fields": True},
            {"Some": "Value 2", "Header": 3.0, "Fields": False},
        ]

        # Should raise
        with pytest.raises(NotImplementedError):
            writer.writerows(data)
