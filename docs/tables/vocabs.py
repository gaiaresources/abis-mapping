"""Tool for extracting vocabularies from the mappers."""

# Standard
import argparse
import sys

# Third-party
import pydantic

# Local
from docs import tables
from abis_mapping import types
from abis_mapping import utils

# Typing
from typing import Iterator, IO


class VocabTableRow(pydantic.BaseModel):
    """Model for a vocab table row."""
    field_name: str = pydantic.Field(serialization_alias="Template field name")
    preferred_label: str = pydantic.Field(serialization_alias="Preferred label")
    definition: str = pydantic.Field(serialization_alias="Definition")
    alternate_label: str = pydantic.Field(serialization_alias="Alternate label")


class VocabTabler(tables.base.BaseTabler):

    @property
    def header(self) -> list[str]:
        """Getter for the header row."""
        # Get serialization title or fall back to given title for each field.
        raw_hdr = (hdr.serialization_alias or hdr.title for hdr in VocabTableRow.model_fields.values())
        # Assert all values as not None
        return [hdr for hdr in raw_hdr if hdr is not None]

    def generate_table(
        self,
        dest: IO | None = None,
    ) -> str:
        """Generates vocabulary table.

        Args:
            dest (IO, optional): Destination file. Defaults to None.

        Returns:
            str: Table either in markdown or csv.
        """
        # Write header
        self.writer.writeheader()

        # Get all fields that have associated vocabularies.
        dict_fields = self.mapper.schema()["fields"]
        fields: list[types.schema.Field] = [
            types.schema.Field.model_validate(f) for f in dict_fields if f.get("vocabularies") is not None
        ]
        fields = sorted(fields, key=lambda f: f.name)

        # Iterate through fields
        for field in fields:
            # Create a row per vocab term adding anchor to first row
            for vocab_table_row in self.generate_vocab_rows(field):
                # Write row to csv
                self.writer.writerow(vocab_table_row.model_dump(by_alias=True))

        # Write to destination
        if dest is not None:
            print(self.output.getvalue(), file=dest)

        # Return
        return self.output.getvalue()

    def generate_vocab_rows(
        self,
        field: types.schema.Field,
    ) -> Iterator[VocabTableRow]:
        """Generates a set of rows based on a field's vocabulary.

        Args:
            field (types.schema.Field): Field the vocabulary is related to.
            as_markdown (bool): True to generate a markdown table. Defaults to False, as csv.

        Yields:
            VocabTableRow: Vocabulary table rows.
        """
        # Retrieve publishable vocabs for field
        vocabs = (utils.vocabs.get_vocab(v) for v in field.vocabularies)
        publishable_vocabs = (v for v in vocabs if v.publish)

        # Map terms based on their preferred label
        grouped_terms = (v.terms for v in publishable_vocabs)
        publishable_terms = (t for ts in grouped_terms for t in ts)
        terms_map: dict[str, utils.vocabs.Term] = {
            t.preferred_label: t for t in publishable_terms if t.preferred_label is not None
        }

        # Sort terms and turn into a generator
        sorted_terms: Iterator[str] = (t for t in sorted(terms_map))

        # If markdown then the first row must contain an anchor
        if self.format == "markdown" and (term_key := next(sorted_terms, None)) is not None:
            yield self.generate_row(
                field=field.model_copy(update={'name': f'<a name="{field.name}-vocabularies"></a>{field.name}'}),
                term=terms_map[term_key],
            )
        # Iterate through terms and yield each row.
        for term_key in sorted_terms:
            yield self.generate_row(
                field=field,
                term=terms_map[term_key],
            )

    @staticmethod
    def generate_row(
        field: types.schema.Field,
        term: utils.vocabs.Term,
    ) -> VocabTableRow:
        """Generates a single row for the table.

        Args:
            field (types.schema.Field): Field the vocabulary is related to.
            term (utils.vocabs.Term): Term corresponding to the vocab and field.

        Returns:
            VocabTableRow: Vocabulary table row for the given term.
        """
        # Perform mapping
        row = VocabTableRow(
            field_name=field.name,
            preferred_label=term.preferred_label or "",
            definition=term.description,
            alternate_label=", ".join(term.alternative_labels),
        )

        # Return
        return row


if __name__ == "__main__":
    """Main entry point."""
    # Create argument parser
    parser = argparse.ArgumentParser(description="A tool to generate a csv table of vocabularies from a mapper.")
    parser.add_argument("template_id", type=str, help="ID of the template.")
    parser.add_argument(
        "-o", "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout."
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Create tabler
    tabler = VocabTabler(args.template_id)

    try:
        # Perform conversion
        tabler.generate_table(args.output_dest)
    finally:
        # Close output file
        args.output_dest.close()
