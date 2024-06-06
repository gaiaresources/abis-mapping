"""Provides base class functionality for tablers."""

# Standard
import abc

# Local
from abis_mapping import base

# Typing
from typing import IO, Final


class Tabler(abc.ABC):
    def __init__(
        self,
        template_id: str
    ) -> None:
        """Constructor for Tabler.

        Args:
            template_id (str): Template ID.
        """
        self.template_id: Final[str] = template_id
        self.mapper: Final[type[base.mapper.ABISMapper]] = self._retrieve_mapper()

    @abc.abstractmethod
    def generate_table(
        self,
        dest: IO | None = None
    ) -> str:
        """Called by tools to generate a table.

        Args:
            dest (IO | None): Optional destination file to write the table.

        Returns:
            str: Table as csv.
        """

    def _retrieve_mapper(
        self,
    ) -> type[base.mapper.ABISMapper]:
        """Retrieves specified mapper if it exists

        Returns:
            base.mapper.ABISMapper: The specified mapper.

        Raises:
            ValueError: If template ID not a registered mapper.
        """
        # Check template exists, get mapper
        if (mapper := base.mapper.get_mapper(self.template_id)) is None:
            raise ValueError(f"mapper '{self.template_id}' not found.")

        # Return
        return mapper
