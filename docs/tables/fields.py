"""Tool for extracting fields from the mappers."""

# Standard
import io
import csv
import argparse
import sys
from unittest import mock

# Third-party
import pydantic
import frictionless

# Local
from abis_mapping import types
from abis_mapping import plugins
from docs import tables

# Typing
from typing import IO


class FieldTableRow(pydantic.BaseModel):
    """Field table row."""
    field_name: str = pydantic.Field(serialization_alias="Field Name")
    description: str = pydantic.Field(serialization_alias="Description")
    mandatory_optional: str = pydantic.Field(
        serialization_alias="Mandatory / Optional",
    )
    datatype_format: str = pydantic.Field(serialization_alias="Datatype Format")
    examples: str = pydantic.Field(serialization_alias="Examples")


class FieldTabler(tables.base.BaseTabler):
    def generate_table(
        self,
        dest: IO | None = None,
        as_markdown: bool = False,
    ) -> str:
        """Compile fields table from the given template.

        Args:
            dest (IO): Destination file for result.
            as_markdown (bool, optional): Whether to output the table as markdown.

        Returns:
            str: Compiled fields table.

        Raises:
            ValueError: If the provided template id doesn't exist.
        """
        # Localize fields
        dict_fields = self.mapper.schema()["fields"]
        fields: list[types.schema.Field] = [types.schema.Field.model_validate(f) for f in dict_fields]

        # Create a memory io and dictionary to csv writer
        output = io.StringIO()
        raw_hdr = (hdr.serialization_alias or hdr.title for hdr in FieldTableRow.model_fields.values())
        header = [hdr for hdr in raw_hdr if hdr is not None]

        if as_markdown:
            # MarkdownDictWriter is a subclass of DictWriter hence the type hint.
            writer: csv.DictWriter = tables.base.MarkdownDictWriter(
                f=output,
                fieldnames=header,
                alignment=["l", "l", "c", "c", "l"],
            )
        else:
            writer = csv.DictWriter(output, fieldnames=header)

        # Write header
        writer.writeheader()

        # Iterate through fields and add to csv
        for field in fields:
            # Perform basic mapping initially
            field_table_row = self.generate_row(field)

            # Modify mandatory_optional attribute
            field_table_row.mandatory_optional = self.mandatory_optional_text(
                required=field.constraints.required,
                field_name=field.name,
            )

            # If markdown add link to vocabularies
            if as_markdown and field.publishable_vocabularies:
                field_table_row.examples += f"<br>([Vocabulary link](#{field.name}-vocabularies))"

            # If markdown add link to field names
            if as_markdown and field.url:
                field_table_row.field_name = f"[{field_table_row.field_name}]({field.url})"

            # Write row to csv
            writer.writerow(field_table_row.model_dump(by_alias=True))

        # Write to destination
        if dest is not None:
            print(output.getvalue(), file=dest)

        # Return
        return output.getvalue()

    def mandatory_optional_text(
        self,
        required: bool,
        field_name: str
    ) -> str:
        """Determines text value to use for a mandatory / optional field.

        Args:
            required (bool): Whether the field is required.
            field_name (str): Field name.

        Returns:
            str: Text to use for mandatory / optional field.
        """
        # Get checklist
        checklist = self.determine_checklist()

        # Create blank set
        fields = set()

        # Check for any mutual inclusivity checks
        if checklist is not None:
            fields = self.mutual_inclusivity(field_name, checklist)

        # Conditionally send corresponding text
        if required:
            return "Mandatory"
        elif len(fields) == 1:
            return f"Conditionally mandatory with {fields.pop()}"
        elif len(fields) > 1:
            last_field = fields.pop()
            return f"Conditionally mandatory with {', '.join(fields)} and {last_field}"

        return "Optional"

    @staticmethod
    def generate_row(
        field: types.schema.Field
    ) -> FieldTableRow:
        """Takes a field object and generates a corresponding csv row object.

        Args:
            field (dict[str, Any]): Field from schema.

        Returns:
            FieldTableRow: To be written to a csv writer row.
        """
        # Perform mapping
        row = FieldTableRow(
            field_name=field.name,
            description=field.description,
            mandatory_optional="Mandatory" if field.constraints.required else "Optional",
            datatype_format=field.type.title() if field.type not in ["wkt"] else field.type.upper(),
            examples=field.example or "",
        )

        # Return
        return row

    def determine_checklist(
        self,
        **kwargs: dict,
    ) -> frictionless.Checklist | None:
        """Determines frictionless checklist being performed as part of a template's validation.

        Args:
            **kwargs (dict): Keyword arguments that may be provided to the
                validation method.

        Returns:
            frictionless.Checklist: Instance used in template validation.
        """
        # Create patch and mock
        with mock.patch("frictionless.Resource") as mocked_resource:
            # Call validation method
            self.mapper().apply_validation(b"some,sample,data\n", **kwargs)

            # Get validate method mock
            mocked_validate: mock.Mock = mocked_resource.return_value.validate

            # Retrieve checklist and return
            if mocked_validate.called:
                checklist: frictionless.Checklist = mocked_validate.call_args.kwargs.get("checklist")
                return checklist

            # Else
            return None

    @staticmethod
    def mutual_inclusivity(
        field_name: str,
        checklist: frictionless.Checklist
    ) -> set[str]:
        """Retrieves all fields that share a mutual inclusive check with supplied field name.

        Args:
            field_name (str): Field name to check for mutual inclusivity.
            checklist (frictionless.Checklist): Checklist used within a template's
                validation method.

        Returns:
            set[str]: Field's mutually inclusive with named field.
        """
        # Filter out mutually inclusive checks from the checklist
        mutual_inclusive_checks: list[plugins.mutual_inclusion.MutuallyInclusive] = \
            [check for check in checklist.checks if isinstance(check, plugins.mutual_inclusion.MutuallyInclusive)]

        # Empty set to hold results
        fields: set[str] = set()

        # Iterate through checks
        for check in mutual_inclusive_checks:
            # Check field name in check
            if field_name in check.field_names:
                fields = fields.union(check.field_names)
                fields.remove(field_name)

        # Return
        return fields


if __name__ == "__main__":
    """Main entry point."""
    # Create argument parser
    parser = argparse.ArgumentParser(description="A tool to generate a csv table of schema fields from a mapper.")
    parser.add_argument("template_id", type=str, help="ID of the template.")
    parser.add_argument(
        "-o", "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout."
    )

    # Parse supplied command line arguments
    args = parser.parse_args()

    # Create tabler
    tabler = FieldTabler(args.template_id)

    try:
        # Perform conversion
        tabler.generate_table(args.output_dest)
    finally:
        # Close output file
        args.output_dest.close()
