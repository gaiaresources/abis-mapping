"""Provides base class functionality for tablers."""

# Standard
import abc
import csv
import re

# Local
from abis_mapping import base

# Typing
from typing import IO, Final, Any


class BaseTabler(abc.ABC):
    def __init__(
        self,
        template_id: str
    ) -> None:
        """Constructor for BaseTabler.

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
        """Called by tables to generate a table.

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


class MarkdownDialect(csv.excel):
    """Custom dialect for markdown tables."""
    delimiter = '|'
    escapechar = '\\'
    quoting = csv.QUOTE_NONE


# Register the dialect with the csv module
csv.register_dialect("markdown", MarkdownDialect)


class MarkdownDictWriter(csv.DictWriter):
    """Custom CSV writer that produces """
    def __init__(
        self,
        f: IO,
        fieldnames: list[str],
        *args: list[Any],
        **kwargs: dict[str, Any]
    ) -> None:
        """Constructor for the MarkdownDictWriter.

        Args:
            *args (list): Positional arguments to csv.DictWriter.:
            **kwargs (dict): Keyword arguments to csv.DictWriter.:
        """
        # Create dummy first and last fields to create leading and trailing pipes
        fieldnames.insert(0, "__start__")
        fieldnames.append("__end__")

        # Assign dialect attribute
        self.dialect: Final[csv.Dialect] = csv.get_dialect("markdown")

        # Call parent constructor
        super().__init__(f, fieldnames, dialect="markdown", *args, **kwargs)

    @property
    def first_field(self) -> str:
        """Returns name of first field."""
        return self.fieldnames[0]

    @property
    def last_field(self) -> str:
        """Returns name of last field."""
        return self.fieldnames[-1]

    def writeheader(self) -> Any:
        """Writes the first row of the markdown table.

        Returns:
            Any: Result from final underlying file write method call.
        """
        # Create header row
        header = dict(zip(self.fieldnames, self.fieldnames))
        self.writerow(header)

        # Create horizontal line
        header_break = dict(zip(self.fieldnames, ["---"] * len(self.fieldnames)))
        return self.writerow(header_break)

    def writerow(self, rowdict: dict[str, Any]) -> Any:
        """Writes a row of the markdown table.

        Args:
            rowdict (dict[str, Any]): Dictionary to convert.

        Returns:
            Any: Value returned from underlying file write method.
        """
        # Add the first and last blank values to allow beginning and trailing pipes
        rowdict[self.first_field] = None
        rowdict[self.last_field] = None

        # Call parent writerow and return
        return super().writerow(rowdict)

    def _clean_cell(self, contents: str) -> str:
        """Cleans cell content, quoting delimiter characters.

        Args:
            contents (str): Content to clean.

        Returns:
            str: Cleaned content.
        """
        # Perform replacement
        return contents.replace(
            self.dialect.delimiter,
            f"{self.dialect.quotechar}{self.dialect.delimiter}{self.dialect.quotechar}",
        )

    def writerows(self, rowdicts: list[dict[str, Any]]) -> None:
        """Writes rows of the markdown table.

        Raises:
            NotImplementedError: Method is not implemented for
                the markdown dict writer
        """
        # Raise
        raise NotImplementedError(
            "writerows functionality not implemented for markdown table writer."
        )
