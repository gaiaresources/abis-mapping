"""Describes the models to define a schema."""


# Third-party
import pydantic

# Local
from abis_mapping import utils

# Typing
from typing import Any, Type


class Constraints(pydantic.BaseModel):
    """The constraints of a schema field primarily defined by frictionless."""
    required: bool
    minimum: float | int | None = None
    maximum: float | int | None = None
    enum: list[str] | None = None


class Field(pydantic.BaseModel):
    """Field model of a schema"""
    name: str
    title: str
    description: str
    example: str | None = None
    type: str
    format: str | None
    constraints: Constraints
    vocabularies: list[str] = []

    # Allow extra fields to be captured mainly to catch errors in json
    model_config = pydantic.ConfigDict(extra="allow")

    @pydantic.field_validator("vocabularies", mode="after")
    @classmethod
    def check_vocabularies(cls, values: list[str]) -> list[str]:
        """Custom validation of the vocabularies field.

        Args:
            values (list[str]): The provided vocabularies initial value.

        Returns:
            list[str]: The validated vocabulary ids.

        Raises:
            KeyError: A provided vocabulary id does not exist.
        """
        # Check each provided name to see if it exists in the registry
        for name in values:
            if utils.vocabs.get_vocab(name) is None:
                raise ValueError(f"Vocabulary id {name} does not exist.")

        # Return list
        return values

    def get_vocab(self, name: str | None = None) -> Type[utils.vocabs.Vocabulary]:
        """Retrieves the vocab for the field.

        Args:
            name (str | None, optional): The name of the vocab to retrieve. Will
                return first vocab if not provided.

        Returns:
            Type[utils.vocabs.Vocabulary]: Returns vocabulary for the field.

        Raises:
            ValueError: If name is not within the vocabularies field.
        """
        # Check if name exists
        if name is not None and name not in self.vocabularies:
            raise ValueError(f"Vocabulary '{name}' is not defined for field {self.name}.")

        # Retrieve
        if name is not None:
            return utils.vocabs.get_vocab(name)

        return utils.vocabs.get_vocab(self.vocabularies[0])

    @property
    def publishable_vocabularies(self) -> list[str]:
        """Returns a list of only those vocabularies that are publishable.

        Returns:
            list[str]: The publishable vocabularies.
        """
        # Filter and return
        return [v for v in self.vocabularies if self.get_vocab(v).publish]


class Schema(pydantic.BaseModel):
    """Model for overall schema object of a schema definition."""
    fields: list[Field]
    primaryKey: str | None = None
    foreignKeys: list[dict[str, Any]] | None = None

    # Allow extra fields to be captured mainly to catch errors in json
    model_config = pydantic.ConfigDict(extra="allow")
