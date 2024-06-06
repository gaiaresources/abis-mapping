"""Tool for extracting vocabularies from the mappers."""

# Standard
import argparse
import csv
import io
import sys

# Third-party
import pydantic

# Local
from tools import table
from abis_mapping import types
from abis_mapping import utils

# Typing
from typing import Iterable, IO


class VocabTableRow(pydantic.BaseModel):
    """Model for a vocab table row."""
    field_name: str = pydantic.Field(serialization_alias="Template field name")
    preferred_label: str = pydantic.Field(serialization_alias="Preferred label")
    definition: str = pydantic.Field(serialization_alias="Definition")
    alternate_label: str = pydantic.Field(serialization_alias="Alternate label")


class VocabTabler(table.Tabler):
    def generate_table(
        self,
        dest: IO | None = None
    ) -> str:
        """Generates vocabulary table.

        Args:
            dest (IO, optional): Destination file. Defaults to None.

        Returns:
            str: Table as csv.
        """
        # Get all fields that have associated vocabularies.
        dict_fields = self.mapper.schema()["fields"]

        fields: list[types.schema.Field] = [
            types.schema.Field.model_validate(f) for f in dict_fields if f.get("vocabularies") is not None
        ]
        fields = sorted(fields, key=lambda f: f.name)

        # Create a memory io and dictionary to csv writer
        output = io.StringIO()
        header = [hdr.serialization_alias or hdr.title for hdr in VocabTableRow.model_fields.values()]
        csv_writer = csv.DictWriter(output, fieldnames=header)

        # Write header
        csv_writer.writeheader()

        # Iterate through fields
        for field in fields:
            # Retrieve publishable vocabs for field
            vocabs = (utils.vocabs.get_vocab(v) for v in field.vocabularies)
            publishable_vocabs = (v for v in vocabs if v.publish)

            # Iterate through publishable vocabs
            for vocab in publishable_vocabs:
                # Create a row per vocab term
                for vocab_table_row in self.generate_vocab_rows(field, vocab):
                    # Write row to csv
                    csv_writer.writerow(vocab_table_row.model_dump(by_alias=True))

        # Write to destination
        if dest is not None:
            print(output.getvalue(), file=dest)

        # Return
        return output.getvalue()

    def generate_vocab_rows(
        self,
        field: types.schema.Field,
        vocab: utils.vocabs.Vocabulary,
    ) -> Iterable[VocabTableRow]:
        """Generates a set of rows based on vocabulary.

        Args:
            field (types.schema.Field): Field the vocabulary is related to.
            vocab (utils.vocabs.Vocabulary): Vocabulary to generate.

        Yields:
            VocabTableRow: Vocabulary table rows.
        """
        # Itermate through terms and yield each row.
        for term in sorted(vocab.terms, key=lambda x: x.preferred_label):
            yield self.generate_row(
                field=field,
                term=term,
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
            preferred_label=term.preferred_label,
            definition=term.description,
            alternate_label=", ".join(term.alternative_labels),
        )

        # Return
        return row


if __name__ == "__main__":
    """Main entry point."""
    # Create argument parser
    parser = argparse.ArgumentParser(description="A tool to genera a csv table of vocabularies from a mapper.")
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

