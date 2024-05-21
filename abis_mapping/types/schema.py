"""Describes the models to define a schema."""

# Third-party
import pydantic

# Typing
from typing import Any


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


class Schema(pydantic.BaseModel):
    """Model for overall schema object of a schema definition."""
    fields: list[Field]
    primaryKey: str | None = None
    foreignKeys: list[dict[str, Any]] | None = None

    # Allow extra fields to be captured mainly to catch errors in json
    model_config = pydantic.ConfigDict(extra="allow")
