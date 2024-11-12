"""Provides unit tests for the schema module."""

# Third-party
import pydantic
import pytest

# Local
from abis_mapping import models

# Typing
from typing import Any


class TestField:
    @pytest.fixture
    def field_d(self) -> dict[str, Any]:
        """Returns a field definition.

        Returns:
            dict[str, Any]: The field definition.
        """

        return {
            "name": "fieldA",
            "title": "titleA",
            "description": "descriptionA",
            "example": "exampleA",
            "type": "typeA",
            "format": None,
            "constraints": {
                "required": False,
            },
            "vocabularies": ["SEX"],
        }

    def test_check_vocabularies(self, field_d: dict[str, Any]) -> None:
        """Tests the check vocabularies method with valid vocab.

        Args:
            field_d (dict[str, Any]): The field definition.
        """
        # Perform validation
        field = models.schema.Field.model_validate(field_d)

        # Assert
        assert field.vocabularies == ["SEX"]

    def test_check_vocabularies_invalid_vocab(self, field_d: dict[str, Any]) -> None:
        """Tests the custom vocabularies validator method with invalid input.

        Args:
            field_d (dict[str, Any]): Field definition fixture
        """
        # Modify the field fixture to have invalid vocab
        field_d["vocabularies"] = ["AFAKEVOCAB123"]

        with pytest.raises(pydantic.ValidationError) as exc:
            # Create field
            models.schema.Field.model_validate(field_d)

        # Should have been raised through catching a ValueError only
        assert len(exc.value.errors()) == 1
        assert exc.value.errors()[0]["type"] == "value_error"

    def test_get_vocab(self, field_d: dict[str, Any]) -> None:
        """Tests the get vocab method.

        Args:
            field_d dict[str, Any]: The field definition fixture.
        """
        # Create field
        field = models.schema.Field.model_validate(field_d)

        # Invoke
        vocab = field.get_vocab()

        # Assert
        assert vocab.vocab_id == "SEX"

    def test_get_vocab_invalid_id(self, field_d: dict[str, Any]) -> None:
        """Test the get_vocab method with invalid id.

        Args:
            field_d (dict[str, Any]): The field definition fixture.
        """
        # Create field
        field = models.schema.Field.model_validate(field_d)

        with pytest.raises(ValueError):
            # Invoke
            field.get_vocab("AFAKEVOCAB123")

    def test_get_vocab_no_vocabs(self, field_d: dict[str, Any]) -> None:
        """Test the get_vocab method with no vocabs on field.

        Args:
            field_d (dict[str, Any]): The field definition fixture.
        """
        # Modify field d
        field_d["vocabularies"] = []

        # Create field
        field = models.schema.Field.model_validate(field_d)

        # Should raise index error
        with pytest.raises(IndexError):
            # Invoke
            field.get_vocab()
