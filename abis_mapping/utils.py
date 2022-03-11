"""Provides utilities for the package"""


# Local
from . import base


def get_mapper(template_id: str) -> type[base.ABISMapper]:
    """Retrieves ABIS Mapper class for the specified template ID.

    Args:
        template_id (str): Template ID to retrieve the mapper for

    Returns:
        type[ABISMapper]: ABIS mapper associated with the template ID.

    Raises:
        KeyError: Raised if the template ID supplied cannot be found
    """
    # Retrieve and return the mapper
    return base.ABISMapper.registry[template_id]


def get_mappers() -> dict[str, base.ABISMapper]:
    """Retrieves the full registry of ABIS Mappers.

    Returns:
        dict[str, base.ABISMapper]: Dictionary of template ID to ABIS Mapper.
    """
    # Retrieve and return the mappers
    return base.ABISMapper.registry
