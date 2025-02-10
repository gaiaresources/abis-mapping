"""Tool for extracting fields from the mappers."""

# Standard
import argparse
import enum
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
from typing import IO, Annotated, Any


class MandatoryType(enum.Enum):
    OPTIONAL = enum.auto()
    CONDITIONALLY_MANDATORY = enum.auto()
    MANDATORY = enum.auto()


class FieldTableRow(pydantic.BaseModel):
    """Standard Field table row."""

    field: Annotated[models.schema.Field, pydantic.Field(exclude=True)]
    checklist: Annotated[frictionless.Checklist, pydantic.Field(exclude=True)]

    # Where the field appears in the schema and template columns beginning at 1
    field_no: Annotated[int, pydantic.Field(exclude=True)]

    @pydantic.computed_field(alias="Field #")  # type: ignore[prop-decorator]
    @property
    def field_number(self) -> str:
        """A dummy property to assist with serialization of the field_no field."""
        return str(self.field_no)

    @pydantic.computed_field(alias="Name")  # type: ignore[prop-decorator]
    @property
    def field_name(self) -> str:
        """Derive from supplied field."""
        return self.field.name

    @pydantic.computed_field(alias="Description")  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        """Derive from supplied field."""
        return self.field.description

    def _get_mandatory_optional(self) -> tuple[MandatoryType, str]:
        """Which "type" of mandatoryness, plus the text description."""
        # First check if field is Mandatory
        if self.field.constraints.required:
            return MandatoryType.MANDATORY, "Mandatory"

        # If this field+template is one of the "site identifier" fields, use a custom
        # conditionally mandatory message, rather than the usual logic.
        if is_site_identifier_field(self.field.name, self.checklist):
            skip_when_missing = site_identifier_skip_field(self.checklist)
            if skip_when_missing:
                skip_condition = f"{skip_when_missing} is provided and "
            else:
                skip_condition = ""
            if self.field.name == "siteID":
                return MandatoryType.CONDITIONALLY_MANDATORY, (
                    f"Mandatory if {skip_condition}existingBDRSiteIRI is not provided.\n"
                    "Mandatory if siteIDSource is provided.\n"
                )
            elif self.field.name == "siteIDSource":
                return MandatoryType.CONDITIONALLY_MANDATORY, (
                    f"Mandatory if {skip_condition}existingBDRSiteIRI is not provided.\n"
                    "Mandatory if siteID is provided.\n"
                )
            elif self.field.name == "existingBDRSiteIRI":
                return MandatoryType.CONDITIONALLY_MANDATORY, (
                    f"Mandatory if {skip_condition}siteID and siteIDSource are not provided.\n"
                )

        # Otherwise, Check for any mutual inclusivity checks
        mi_fields = mutual_inclusivity(self.field.name, self.checklist)
        # Conditionally return corresponding text
        if len(mi_fields) == 1:
            return MandatoryType.CONDITIONALLY_MANDATORY, f"Mandatory if {mi_fields[0]} is provided."
        elif len(mi_fields) > 1:
            last_field = mi_fields.pop()
            return (
                MandatoryType.CONDITIONALLY_MANDATORY,
                f"Mandatory if {', '.join(mi_fields)} or {last_field} are provided.",
            )

        # Otherwise, field is optional.
        return MandatoryType.OPTIONAL, "Optional"

    @pydantic.computed_field(alias="Mandatory / Optional")  # type: ignore[prop-decorator]
    @property
    def mandatory_optional(self) -> str:
        """Output text for mandatoryness."""
        _, text = self._get_mandatory_optional()
        text = text.strip().replace("\n", " ")
        return text

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

    @pydantic.computed_field(alias="Name")  # type: ignore[prop-decorator]
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
        """Output text for mandatoryness, in Markdown format."""
        mandatory, text = self._get_mandatory_optional()

        # Can't use an actual \n in the middle of a Markdown table
        text = text.strip().replace("\n", "<br>")

        # Return text wrapped in color if needed.
        if mandatory == MandatoryType.MANDATORY:
            return f'**<font color="Crimson">{text}</font>**'
        elif mandatory == MandatoryType.CONDITIONALLY_MANDATORY:
            return f'**<font color="DarkGoldenRod">{text}</font>**'
        else:
            return text

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

    alignment = ["c", "l", "l", "c", "c", "l"]

    @property
    def header(self) -> list[str]:
        """Getter for the table header."""
        # Get titles from model
        ftrow = MarkdownFieldTableRow if self.format == "markdown" else FieldTableRow
        raw_hdr = (hdr.alias or hdr.title for hdr in ftrow.model_computed_fields.values())
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
        dest: IO[str] | None = None,
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
        for i, field in enumerate(self.fields, start=1):
            # Create row
            if self.format == "markdown":
                field_table_row: FieldTableRow = MarkdownFieldTableRow(field=field, checklist=checklist, field_no=i)
            else:
                field_table_row = FieldTableRow(field=field, checklist=checklist, field_no=i)

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
        **kwargs: Any,
    ) -> frictionless.Checklist:
        """Determines frictionless checklist being performed as part of a template's validation.

        Args:
            **kwargs: Keyword arguments that may be provided to the validation method.

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
                checklist = mocked_validate.call_args.kwargs.get("checklist")
                if not isinstance(checklist, frictionless.Checklist):
                    raise ValueError("checklist is not a frictionless checklist")
                return checklist

            # Else
            raise Exception("Resource.validate() not called by apply_validation()")


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
        list[str]: Field's mutually inclusive with named fields, sorted.
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


def is_site_identifier_field(
    field_name: str,
    checklist: frictionless.Checklist,
) -> bool:
    """Check is the field is a "site identifier" field,
    and the template uses SiteIdentifierCheck plugin."""
    return field_name in ("siteID", "siteIDSource", "existingBDRSiteIRI") and any(
        isinstance(check, plugins.site_id_or_iri_validation.SiteIdentifierCheck) for check in checklist.checks
    )


def site_identifier_skip_field(checklist: frictionless.Checklist) -> str | None:
    """Get the field the SiteIdentifierCheck is skipped for."""
    for check in checklist.checks:
        if isinstance(check, plugins.site_id_or_iri_validation.SiteIdentifierCheck):
            return check.skip_when_missing
    raise Exception("Could not find SiteIdentifierCheck in checklist")


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
