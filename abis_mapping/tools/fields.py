"""Tool for extracting fields from the mappers."""

# Standard
import io
import csv

# Third-party
import pydantic

# Local
from abis_mapping import base
from abis_mapping import types

# Typing
from typing import Any


HEADERS = ["Field Name", "Description", "Mandatory / Optional", "Datatype Format", "Examples"]


class FieldTableRow(pydantic.BaseModel):
    """Field table row."""
    field_name: str = pydantic.Field(serialization_alias="Field Name")
    description: str = pydantic.Field(serialization_alias="Description")
    mandatory_optional: str = pydantic.Field(
        serialization_alias="Mandatory / Optional",
        pattern=r"(Mandatory|Optional)"
    )
    datatype_format: str = pydantic.Field(serialization_alias="Datatype Format")
    examples: str = pydantic.Field(serialization_alias="Examples")


def compile_fields(template_id: str) -> None:
    """Compile fields table from the given template.

    Args:
        template_id (str): ID of the template

    Raises:
        ValueError: If the provided template id doesn't exist.
    """
    # Check template exists, get mapper
    if (mapper := base.mapper.get_mapper(template_id)) is None:
        raise ValueError(f"mapper '{template_id}' not found.")

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
        csv_writer.writerow(generate_row(field).model_dump(by_alias=True))

    # Output to stdout
    print(output.getvalue())


def generate_row(field: types.schema.Field) -> FieldTableRow:
    """Takes a field object and generates a corresponding csv row object.

    Args:
        field (dict[str, Any]): Field from schema.

    Returns:
        dict[str, Any]: To be directly written to a csv writer row.
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

if __name__ == "__main__":
    compile_fields("incidental_occurrence_data-v2.0.0.csv")
