"""Provides base class functionality for tablers."""

# Standard
import abc
import csv
import io

# Local
from abis_mapping import base

# Typing
from typing import IO, Final, Any, Mapping, Iterable, Literal


class BaseTabler(abc.ABC):
    """Base class for tablers.

    Attributes:
        alignment (list[str] | None): Optional alignment of table columns.
    """
    # Class attributes
    alignment: list[str] | None = None

    def __init__(
        self,
        template_id: str,
        format: str = "csv",
    ) -> None:
        """Constructor for BaseTabler.

        Args:
            template_id (str): Template ID.
            format (str, optional): Format of output table. Defaults to "markdown".

        Raises:
            ValueError: If format is not supported.
        """
        # Define and check for supported formats
        supported_formats: Final[list[str]] = ["markdown", "csv"]
        if format not in supported_formats:
            raise ValueError(f"unsupported format '{format}', must be one of {supported_formats}")

        # Assign object attributes
        self.format = format
        self.template_id: Final[str] = template_id
        self.mapper: Final[type[base.mapper.ABISMapper]] = self._retrieve_mapper()

        # Create an in-memory io
        self.output: Final[io.StringIO] = io.StringIO()

        # Create writer
        if format == "markdown":
            # MarkdownDictWriter is a subclass of DictWriter hence the type hint.
            self.writer: csv.DictWriter = MarkdownDictWriter(
                f=self.output,
                fieldnames=self.header,
                alignment=self.alignment,
            )
        else:
            self.writer = csv.DictWriter(self.output, fieldnames=self.header)

    @property
    @abc.abstractmethod
    def header(self) -> list[str]:
        """Need to define a header property."""

    @abc.abstractmethod
    def generate_table(
        self,
        dest: IO | None = None,
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
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE
    quotechar = None


# Register the dialect with the csv module
csv.register_dialect("markdown", MarkdownDialect)


class MarkdownDictWriter(csv.DictWriter):
    """Custom CSV writer that produces """
    def __init__(
        self,
        f: IO,
        fieldnames: list[str],
        restval: str = "",
        extrasaction: Literal["raise", "ignore"] = "raise",
        *,
        alignment: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructor for the MarkdownDictWriter.

        Args:
            f (IO): File to be written out.
            fieldnames (list[str]): List of fieldnames.
            restval (str): The value to be written if the dictionary is missing a key
                in fieldnames.
            extrasaction: (str): The action to take if the dictionary has a key not
                found in fieldnames.
            alignment (list[str], optional): List of alignment options,
                for each field. Defaults to None, in which case all fields are
                are left-aligned. The length of the list must match the length
                of fieldnames. Allowed alignment values are "l", "r", "c", "left",
                "right", and "center".
            **kwargs (dict): Extra kwargs for the underlying csv.writer instance.

        Raises:
            ValueError: If alignment list length doesn't match fieldnames or
                an invalid alignment option is provided.
        """
        # Check alignment list length
        if alignment is not None and len(alignment) != len(fieldnames):
            raise ValueError(f"The alignment list length ({len(alignment)}) must match fieldnames ({len(fieldnames)}).")

        # Check alignment values
        if alignment is not None:
            for i, align in enumerate(alignment):
                if align not in ["l", "r", "c", "left", "right", "center"]:
                    raise ValueError(f"Unknown alignment value provided '{align}' at index {i}")

        # Create dummy first and last fields to create leading and trailing pipes
        fieldnames.insert(0, "__start__")
        fieldnames.append("__end__")

        # Assign attributes
        self.alignment: Final[list[str] | None] = ["l", *alignment, "l"] if alignment is not None else None

        # Call parent constructor
        super().__init__(f, fieldnames, restval, extrasaction, dialect="markdown", **kwargs)

    @property
    def first_field(self) -> Any:
        """Returns name of first field."""
        return self.fieldnames[0]  # type: ignore[index]

    @property
    def last_field(self) -> Any:
        """Returns name of last field."""
        return self.fieldnames[-1]  # type: ignore[index]

    def writeheader(self) -> Any:
        """Writes the first row of the markdown table.

        Returns:
            Any: Result from final underlying file write method call.
        """
        # Create header row
        header = dict(zip(self.fieldnames, self.fieldnames))
        self.writerow(header)

        # Create horizontal line
        if self.alignment is not None:
            divider = []
            for align in self.alignment:
                match align:
                    case "l" | "left":
                        divider.append(":---")
                    case "r" | "right":
                        divider.append("---:")
                    case "c" | "center":
                        divider.append(":---:")
        else:
            divider = [":---"] * len(self.fieldnames)

        header_break = dict(zip(self.fieldnames, divider))
        return self.writerow(header_break)

    def writerow(self, rowdict: Mapping[Any, Any]) -> Any:
        """Writes a row of the markdown table.

        Args:
            rowdict (Mapping[Any, Any]): Dictionary to convert.

        Returns:
            Any: Value returned from underlying file write method.
        """
        # Add the first and last blank values to allow beginning and trailing pipes
        rowdict[self.first_field] = None  # type: ignore[index]
        rowdict[self.last_field] = None  # type: ignore[index]

        # Clean cells
        for fieldname in self.fieldnames:
            if isinstance(rowdict[fieldname], str):
                rowdict[fieldname] = self._clean_cell(rowdict[fieldname])  # type: ignore[index]

        # Call parent writerow and return
        return super().writerow(rowdict)

    def _clean_cell(self, contents: str) -> str:
        """Cleans cell content

        Args:
            contents (str): Content to clean.

        Returns:
            str: Cleaned content.
        """
        # Perform replacement
        return contents.replace('\n', "<br>")

    def writerows(self, rowdicts: Iterable[Mapping[Any, Any]]) -> None:
        """Writes rows of the markdown table.

        Raises:
            NotImplementedError: Method is not implemented for
                the markdown dict writer
        """
        # Raise
        raise NotImplementedError(
            "writerows functionality not implemented for markdown table writer."
        )
