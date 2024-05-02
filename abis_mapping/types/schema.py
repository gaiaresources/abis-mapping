"""Describes the objects used in defining a schema."""

# Standard
import decimal

# Third-party
import pydantic

# Typing
from typing import Any

class Constraints(pydantic.BaseModel):
    required: bool
    minimum: float | int | None = None
    maximum: float | int | None = None
    enum: list[str] | None = None


class Field(pydantic.BaseModel):
    name: str
    title: str
    description: str
    example: str | None = None
    type: str
    format: str | None
    constraints: Constraints
