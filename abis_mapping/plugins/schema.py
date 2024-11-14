"""Provides a custom implementation of the frictionless schema class."""

# Standard
import copy

# Third-party
import attrs
import frictionless
import frictionless.types
import frictionless.errors

# Typing
from typing import Iterable, Generator


class ExtraFieldsSchemaError(frictionless.errors.SchemaError):
    """Used for any raising of schema related exceptions from within the project."""

    type = "extra-fields_schema-error"
    title = "Extra Fields Schema Error"
    description = "Provided schema is not valid."
    template = "Schema is not valid: {note}"


@attrs.define(kw_only=True, repr=False)
class ExtraFieldsSchema(frictionless.Schema):
    """A customised schema implementation allowing for improved extra fields."""

    original_descriptor: frictionless.types.IDescriptor

    # This schemas descriptor should be modified to include the original schema descriptor
    _original_metadata_profile = lambda: copy.deepcopy(frictionless.Schema.metadata_profile)  # noqa
    metadata_profile = _original_metadata_profile()
    metadata_profile["properties"] = {
        "originalDescriptor": {"type": "object", "properties": _original_metadata_profile()},
        **_original_metadata_profile()["properties"],
    }
    metadata_profile["required"].append("originalDescriptor")
    metadata_Error = ExtraFieldsSchemaError

    @classmethod
    def metadata_validate(cls, descriptor: frictionless.types.IDescriptor) -> Generator[frictionless.Error, None, None]:  # type: ignore[override]
        """Performs validation of the schema descriptor.

        Args:
            descriptor: Dictionary describing the schema.

        Yields:
            Errors encountered.
        """
        # Get original descriptor
        original_descriptor = descriptor["originalDescriptor"]
        if original_descriptor == descriptor:
            # No change in descriptors so revert to standard schema validation
            metadata_errors: Iterable[frictionless.Error] = list(super().metadata_validate(descriptor))
        else:
            # Check for any errors raised by parents, filtering out SchemaErrors.
            metadata_errors = [
                err
                for err in super().metadata_validate(descriptor)
                if not isinstance(err, frictionless.errors.SchemaError)
            ]
        if metadata_errors:
            # Yield metadata errors and return
            yield from metadata_errors
            return

        # Collect fieldnames
        fieldnames = lambda d: [f["name"] for f in d["fields"] if f.get("name") is not None]  # noqa
        actual_fieldnames = fieldnames(descriptor)
        original_fieldnames = fieldnames(original_descriptor)

        # Perform check to ensure that the names of the actual fields matches the original schema
        error_lines: list[str] = []
        zip_fields = [(a, e) for a, e in zip(actual_fieldnames, original_fieldnames, strict=False)]
        error_template = "Field pos {}: expected '{}', got '{}'"
        error_lines = [error_template.format(i, e, a) for i, (a, e) in enumerate(zip_fields, start=1) if a != e]
        if error_lines:
            note = (
                f"The supplied data's first {len(original_fieldnames)} fields should match the "
                f"schema of the template. Found these issue(s): {'; '.join(error_lines)}."
            )
            yield ExtraFieldsSchemaError(note=note)

        # Primary Key - Ensure that the only used keys are from the original descriptor fields
        pk = original_descriptor.get("primaryKey", [])
        for name in pk:
            if name not in original_fieldnames:
                note = 'primary key "%s" not found in original schema fields "%s"'
                note = note % (pk, original_fieldnames)
                yield ExtraFieldsSchemaError(note=note)

        # Foreign Keys - Ensure that the only used keys are from the original descriptor fields
        fks = original_descriptor.get("foreignKeys", [])
        for fk in fks:
            for name in fk["fields"]:
                if name not in original_fieldnames:
                    note = 'foreign key "%s" does not match the original schema fields "%s"'
                    note = note % (fk, original_fieldnames)
                    yield ExtraFieldsSchemaError(note=note)
            if len(fk["fields"]) != len(fk["reference"]["fields"]):
                note = 'foreign key fields "%s" does not match the reference fields "%s"'
                note = note % (fk["fields"], fk["reference"]["fields"])
                yield ExtraFieldsSchemaError(note=note)


