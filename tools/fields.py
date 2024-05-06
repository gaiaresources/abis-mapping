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
from abis_mapping import base
from abis_mapping import types
from abis_mapping import plugins

# Typing
from typing import IO, Iterable


HEADERS = ["Field Name", "Description", "Mandatory / Optional", "Datatype Format", "Examples"]


class FieldTableRow(pydantic.BaseModel):
    """Field table row."""
    field_name: str = pydantic.Field(serialization_alias="Field Name")
    description: str = pydantic.Field(serialization_alias="Description")
    mandatory_optional: str = pydantic.Field(
        serialization_alias="Mandatory / Optional",
    )
    datatype_format: str = pydantic.Field(serialization_alias="Datatype Format")
    examples: str = pydantic.Field(serialization_alias="Examples")


def retrieve_mapper(template_id: str) -> type[base.mapper.ABISMapper]:
    """Retrieves specified mapper if it exists

    Args:
        template_id (str): ID of the template.

    Returns:
        base.mapper.ABISMapper: The specified mapper.

    Raises:
        ValueError: If template ID not a registered mapper.
    """
    # Check template exists, get mapper
    if (mapper := base.mapper.get_mapper(template_id)) is None:
        raise ValueError(f"mapper '{template_id}' not found.")

    # Return
    return mapper


def compile_fields(template_id: str, dest: IO) -> None:
    """Compile fields table from the given template.

    Args:
        template_id (str): ID of the template.
        dest (IO): Destination file for result.

    Raises:
        ValueError: If the provided template id doesn't exist.
    """
    # Get mapper
    mapper = retrieve_mapper(template_id)

    # Localize fields
    dict_fields = mapper.schema()["fields"]
    fields: list[types.schema.Field] = [types.schema.Field.model_validate(f) for f in dict_fields]

    # Create a memory io and dictionary to csv writer
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=HEADERS)

    # Write header
    csv_writer.writeheader()

    # Iterate through fields and add to csv
    for field in fields:
        # Perform basic mapping initially
        field_table_row = generate_row(field)

        # Modify mandatory_optional attribute
        field_table_row.mandatory_optional = mandatory_optional_text(
            required=field.constraints.required,
            template_id=template_id,
            field_name=field.name,
        )

        # Write row to csv
        csv_writer.writerow(generate_row(field).model_dump(by_alias=True))

    # Write to destination
    print(output.getvalue(), file=dest)


def mandatory_optional_text(required: bool, template_id: str, field_name: str) -> str:
    """Determines text value to use for a mandatory / optional field.

    Args:
        required (bool): Whether the field is required.
        template_id (str): ID of the template field belongs.
        field_name (str): Field name.

    Returns:
        str: Text to use for mandatory / optional field.
    """
    # Get checklist
    checklist = determine_checklist(template_id)

    # Create blank set
    fields = set()

    # Check for any mutual inclusivity checks
    if checklist is not None:
        fields = mutual_inclusivity(field_name, checklist)

    # Conditionally send corresponding text
    if required:
        return "Mandatory"
    elif len(fields) == 1:
        return f"Conditionally mandatory with {fields.pop()}"
    elif len(fields) > 1:
        last_field = fields.pop()
        return f"Conditionally mandatory with {', '.join(fields)} and {last_field}"

    return "Optional"


def generate_row(field: types.schema.Field) -> FieldTableRow:
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
        datatype_format=field.type.title(),
        examples=field.example,
    )

    # Return
    return row


def determine_checklist(template_id: str, **kwargs: dict) -> frictionless.Checklist | None:
    """Determines frictionless checklist being performed as part of a template's validation.

    Args:
        template_id (str): ID of template.
        **kwargs (dict): Keyword arguments that may be provided to the
            validation method.

    Returns:
        frictionless.Checklist: Instance used in template validation.
    """
    # Create patch and mock
    with mock.patch("frictionless.Resource") as mocked_resource:
        # Get mapper
        mapper = retrieve_mapper(template_id)

        # Call validation method
        mapper().apply_validation(b"some,sample,data\n", **kwargs)

        # Get validate method mock
        mocked_validate: mock.Mock = mocked_resource.return_value.validate

        # Retrieve checklist
        if mocked_validate.called:
            return mocked_validate.call_args.kwargs.get("checklist")

        # Else
        return None


def mutual_inclusivity(field_name: str, checklist: frictionless.Checklist) -> set[str]:
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
    parser = argparse.ArgumentParser(description="A tool to generate a csv table from a mapper.")
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

    # Perform conversion
    compile_fields(args.template_id, args.output_dest)

    # Close output file
    args.output_dest.close()
