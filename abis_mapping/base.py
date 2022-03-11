"""Provides ABIS Mapper Base Class"""


# Standard
import abc

# Third-Party
import rdflib

# Typing
from typing import final


class ABISMapper(abc.ABC):
    """ABIS Mapper Base Class"""

    # Concrete ABIS Mapper Registry
    registry: dict[str, type["ABISMapper"]] = {}

    @abc.abstractmethod
    def apply_mapping(self, data: bytes) -> rdflib.Graph:
        """Applies mapping from csv to ABIS conformant rdf

        Args:
            data (bytes): Raw csv data

        Returns:
            rdflib.Graph: ABIS conformant rdf graph
        """

    @final
    @classmethod
    def register_mapper(
        cls,
        mapper: type["ABISMapper"],
        template_id: str,
        ) -> None:
        """Registers a concrete ABIS Mapper with the Base Class

        Args:
            mapper (type[ABISMapper]): Mapper to be registered.
            template_id (str): Template ID to associate with the mapper.
        """
        # Register the mapper
        cls.registry[template_id] = mapper
