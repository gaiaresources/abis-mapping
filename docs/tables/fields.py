"""Tool for extracting fields from the mappers."""

# Standard
import argparse
import sys
from unittest import mock

# Third-party
import pydantic
import frictionless

# Local
from abis_mapping import models
from abis_mapping import plugins
from docs import tables

# Typing
from typing import IO, Annotated


class FieldTableRow(pydantic.BaseModel):
    """Standard Field table row."""

    field: Annotated[models.schema.Field, pydantic.Field(exclude=True)]
    checklist: Annotated[frictionless.Checklist | None, pydantic.Field(exclude=True)]

    @pydantic.computed_field(alias="Field Name")  # type: ignore[prop-decorator]
    @property
    def field_name(self) -> str:
        """Derive from supplied field."""
        return self.field.name

    @pydantic.computed_field(alias="Description")  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        """Derive from supplied field."""
        return self.field.description

    @pydantic.computed_field(alias="Mandatory / Optional")  # type: ignore[prop-decorator]
    @property
    def mandatory_optional(self) -> str:
        """Output text for mandatorinessness."""
        # Create blank list
        mi_fields: list[str] = []

        # Check for any mutual inclusivity checks
        if self.checklist is not None:
            mi_fields = mutual_inclusivity(self.field.name, self.checklist)

        # Conditionally return corresponding text
        if self.field.constraints.required:
            return "Mandatory"
        elif len(mi_fields) == 1:
            return f"Conditionally mandatory with {mi_fields.pop()}"
        elif len(mi_fields) > 1:
            last_field = mi_fields.pop()
            return f"Conditionally mandatory with {', '.join(mi_fields)} and {last_field}"
        return "Optional"

    @pydantic.computed_field(alias="Datatype Format")  # type: ignore[prop-decorator]
    @property
    def datatype_format(self) -> str:
        """Get datatype format type for field"""
        return self.field.type.title() if self.field.type not in ["wkt"] else self.field.type.upper()

    @pydantic.computed_field(alias="Examples")  # type: ignore[prop-decorator]
    @property
    def examples(self) -> str:
        """Get the field example."""
        return self.field.example or ""

    model_config = {"arbitrary_types_allowed": True}


class MarkdownFieldTableRow(FieldTableRow):
    """Provides markdown specific serialization properties."""

    @pydantic.computed_field(alias="Field Name")  # type: ignore[prop-decorator]
    @property
    def field_name(self) -> str:
        """Return field's name."""
        # Get field name
        text = self.field.name
        # If markdown add link to field names
        if self.field.url:
            text = f"[{text}]({self.field.url})"
        # Prepend anchor and return
        return f'<a name="{self.field.name}-field"></a>{text}'

    @pydantic.computed_field(alias="Mandatory / Optional")  # type: ignore[prop-decorator]
    @property
    def mandatory_optional(self) -> str:
        """Output text for mandatorinessness."""
        # Create blank list
        mi_fields: list[str] = []

        # Check for any mutual inclusivity checks
        if self.checklist is not None:
            mi_fields = mutual_inclusivity(self.field.name, self.checklist)

        # Conditionally return corresponding text
        if self.field.constraints.required:
            return '**<font color="Crimson">Mandatory</font>**'
        elif len(mi_fields) == 1:
            return f'**<font color="DarkGoldenRod">Conditionally mandatory with {mi_fields.pop()}</font>**'
        elif len(mi_fields) > 1:
            last_field = mi_fields.pop()
            return (
                '**<font color="DarkGoldenRod">'
                f'Conditionally mandatory with {", ".join(mi_fields)} and {last_field}'
                '</font>**'
            )
        return "Optional"

    @pydantic.computed_field(alias="Examples")  # type: ignore[prop-decorator]
    @property
    def examples(self) -> str:
        """Get the field example."""
        # Copy field example
        text = super().examples
        # Add vocab link if part of the field.
        if self.field.publishable_vocabularies:
            text += f"<br>([Vocabulary link](#{self.field.name}-vocabularies))"
        # If WKT field add link to WKT appendix
        if self.field.name in ["spatialCoverageWKT", "footprintWKT"]:
            text += "<br>([WKT notes](#appendix-ii-well-known-text-wkt))"
        return text


class FieldTabler(tables.base.BaseTabler):
    """Tabler class for creating fields tables."""

    alignment = ["l", "l", "c", "c", "l"]

    @property
    def header(self) -> list[str]:
        """Getter for the table header."""
        # Get titles from model
        raw_hdr = (hdr.alias or hdr.title for hdr in FieldTableRow.model_computed_fields.values())
        return [hdr for hdr in raw_hdr if hdr is not None]

    @property
    def fields(self) -> list[models.schema.Field]:
        """Getter for the fields.

        Returns:
            list[models.schema.Field]: List of all fields from schema.
        """
        # Get fields from schema and return
        dict_fields = self.mapper.schema()["fields"]
        return [models.schema.Field.model_validate(f) for f in dict_fields]

    def generate_table(
        self,
        dest: IO | None = None,
    ) -> str:
        """Compile fields table from the given template.

        Args:
            dest (IO): Destination file for result.

        Returns:
            str: Compiled fields table.

        Raises:
            ValueError: If the provided template id doesn't exist.
        """
        # Write header
        self.writer.writeheader()

        # Get checklist
        checklist = self.checklist()

        # Iterate through fields and add to csv
        for field in self.fields:
            # Create row
            if self.format == "markdown":
                field_table_row: FieldTableRow = MarkdownFieldTableRow(field=field, checklist=checklist)
            else:
                field_table_row = FieldTableRow(field=field, checklist=checklist)

            # Write row to csv
            row_d = field_table_row.model_dump(by_alias=True)
            self.writer.writerow(row_d)

        # Write to destination
        if dest is not None:
            print(self.output.getvalue(), file=dest)

        # Return
        return self.output.getvalue()

    def checklist(
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


class OccurrenceField(models.schema.Field):
    """Specific implementation of the field model.

    To be used only in the creation of survey and incidental occurrence field tables.
    """

    @property
    def publishable_vocabularies(self) -> list[str]:
        """Returns a list of only those vocabularies that are publishable.

        Returns:
            list[str]: The publishable vocabularies.
        """
        # Filter and return
        vocabs = []
        for v_id in self.vocabularies:
            v = self.get_vocab(v_id)
            # Modified from normal case threatStatus and conservationAuthority fields to make them
            # publishable so links are created for their corresponding vocab which is
            # currently its own table in the instructions.
            if v.publish or v.vocab_id in ["THREAT_STATUS", "CONSERVATION_AUTHORITY"]:
                vocabs.append(v_id)
        return vocabs


class OccurrenceFieldTabler(FieldTabler):
    """Specific implementation of the field tabler for survey and incidental occurrence templates."""

    @property
    def fields(self) -> list[models.schema.Field]:
        """Getter for the fields.

        Returns:
            list[OccurrenceField]: List of all fields from schema. NOTE: this specifically
                returns OccurrenceField object list
        """
        # Get fields from schema and return
        dict_fields = self.mapper.schema()["fields"]
        return [OccurrenceField.model_validate(f) for f in dict_fields]


def mutual_inclusivity(field_name: str, checklist: frictionless.Checklist) -> list[str]:
    """Retrieves all fields that share a mutual inclusive check with supplied field name.

    Args:
        field_name (str): Field name to check for mutual inclusivity.
        checklist (frictionless.Checklist): Checklist used within a template's
            validation method.

    Returns:
        set[str]: Field's mutually inclusive with named field.
    """
    # Filter out mutually inclusive checks from the checklist
    mutual_inclusive_checks: list[plugins.mutual_inclusion.MutuallyInclusive] = [
        check for check in checklist.checks if isinstance(check, plugins.mutual_inclusion.MutuallyInclusive)
    ]

    # Empty set to hold results
    fields: set[str] = set()

    # Iterate through checks
    for check in mutual_inclusive_checks:
        # Check field name in check
        if field_name in check.field_names:
            fields = fields.union(check.field_names)
            fields.remove(field_name)

    # Return
    return sorted(fields)


if __name__ == "__main__":
    """Main entry point."""
    # Create argument parser
    parser = argparse.ArgumentParser(description="A tool to generate a csv table of schema fields from a mapper.")
    parser.add_argument("template_id", type=str, help="ID of the template.")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout.",
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
