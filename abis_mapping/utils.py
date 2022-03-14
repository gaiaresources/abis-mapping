"""Provides utilities for the package"""


# Local
from . import base

# Typing
from typing import Optional


def get_mapper(template_id: str) -> Optional[type[base.ABISMapper]]:
    """Retrieves ABIS Mapper class for the specified template ID.

    Args:
        template_id (str): Template ID to retrieve the mapper for.

    Returns:
        Optional[type[base.ABISMapper]]: ABIS mapper class associated with the
            specified template ID if found, otherwise `None`.
    """
    # Retrieve and return the mapper
    return base.ABISMapper.registry.get(template_id)


def get_mappers() -> dict[str, base.ABISMapper]:
    """Retrieves the full registry of ABIS Mappers.

    Returns:
        dict[str, base.ABISMapper]: Dictionary of template ID to ABIS Mapper.
    """
    # Retrieve and return the mappers
    return base.ABISMapper.registry
