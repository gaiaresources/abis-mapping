"""Holds contexts used for generating instructions."""

# Local
from abis_mapping import base


# Typing
from typing import Any


# Declare registry to hold all the contexts for callup via the instruction generators
_registry: dict[str, dict[str, Any]] = {}


def register(mapper_id: str, context: dict[str, Any]) -> None:
    """Handles registration of a document rendering context into the register.

    Args:
        mapper_id (str): The id of the mapper that the context
            relates to.
        context (dict[str, Any]): The context to register.

    Raises:
        KeyError: The context is already registered.
        ValueError: The mapper_id supplied has no associated
            mapper registered.
    """
    # Check id not already registered
    if mapper_id in _registry:
        raise KeyError(f"Context already registered for mapper '{mapper_id}'.")

    # Check mapper registered
    if base.mapper.get_mapper(mapper_id) is None:
        raise ValueError(f"Mapper '{mapper_id}' is not registered.")

    # Add to registry
    _registry[mapper_id] = context


def get_context(mapper_id: str) -> dict[str, Any] | None:
    """Handles retrieval of a document rendering context.

    Args:
        mapper_id (str): The id of the mapper that the context belongs to.

    Returns:
        dict[str, Any] | None: The context to be rendered or None if it
            does not exist.
    """
    # Return context
    return _registry.get(mapper_id, None)
