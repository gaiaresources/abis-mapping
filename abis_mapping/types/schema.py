"""Describes the models to define a schema."""

# Third-party
import pydantic

# Local
from abis_mapping import utils

# Typing
from typing import Any, Type, Annotated


class Constraints(pydantic.BaseModel):
    """The constraints of a schema field.

    Currently all defined below are a subset of those available from [frictionless](https://specs.frictionlessdata.io/table-schema/#constraints).
    """

    required: Annotated[
        bool,
        pydantic.Field(
            description="Indicates whether this field cannot be null. If required is false (the default), then null is allowed."
        ),
    ]
    unique: Annotated[
        bool | None,
        pydantic.Field(
            description="If true, then all values for that field MUST be unique within the data file in which it is found."
        ),
    ] = None
    minimum: Annotated[
        float | int | None,
        pydantic.Field(
            description="Specifies a minimum value for a field. This is different to minLength which checks the number of items in the value. A minimum value constraint checks whether a field value is greater than or equal to the specified value. The range checking depends on the type of the field. If a minimum value constraint is specified then the field descriptor MUST contain a type key."
        ),
    ] = None
    maximum: Annotated[
        float | int | None, pydantic.Field(description="As for `minimum`, but specifies a maximum value for a field.")
    ] = None
    enum: Annotated[
        list[str] | None,
        pydantic.Field(description="The value of the field must exactly match a value in the enum array."),
    ] = None


class Field(pydantic.BaseModel):
    """Field model of a schema.

    The properties of a field consisting of those properties used by frictionless for performing validations as well
    as extras to assist with the looking up of vocabularies when mapping as well as assisting with the creation
    of instruction documentation.
    [Frictionless reference](https://specs.frictionlessdata.io/table-schema).
    """

    name: Annotated[
        str,
        pydantic.Field(
            description="[Required by frictionless](https://specs.frictionlessdata.io/table-schema/#name). The field descriptor MUST contain a name property. This property SHOULD correspond to the name of field/column in the data file (if it has a name). As such it SHOULD be unique (though it is possible, but very bad practice, for the data file to have multiple columns with the same name). name SHOULD NOT be considered case sensitive in determining uniqueness. However, since it should correspond to the name of the field in the data file it may be important to preserve case.",
        ),
    ]
    title: Annotated[
        str,
        pydantic.Field(
            description="[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#title). A human readable label or title for the field.",
        ),
    ]
    description: Annotated[
        str,
        pydantic.Field(
            description='[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#description). A description for this field e.g. "The recipient of the funds".',
        ),
    ]
    example: Annotated[
        str | None,
        pydantic.Field(
            description="[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#example). An example value of the field",
        ),
    ] = None
    type: Annotated[
        str,
        pydantic.Field(
            description="[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#types-and-formats). `type` and `format` properties are used to give the type of the field. A fields `type` property is a string indicating the type of this field.",
        ),
    ]
    format: Annotated[
        str | None,
        pydantic.Field(
            description="[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#types-and-formats). `type` and `format` properties are used to give the type of the field. A field's `format` property is a string, indicating a format for the field type.",
        ),
    ]
    url: Annotated[pydantic.AnyUrl | None, pydantic.Field(description="The IRI of the field's concept.")] = None
    constraints: Constraints
    vocabularies: Annotated[
        list[str],
        pydantic.Field(
            description="Optional list of vocabulary IDs, defined internally within the project. Provided IDs need to have been registered to be valid. See [`abis_mapping.vocabs`](/abis_mapping/vocabs/).",
            default_factory=list,
        ),
    ]

    # Allow extra fields to be captured mainly to catch errors in json
    model_config = pydantic.ConfigDict(extra="allow")

    @pydantic.field_serializer("url")
    def serialize_url(self, url: pydantic.AnyUrl) -> str:
        """Custom serializer for the url field to return string on dump.

        Args:
            url (pydantic.AnyUrl): Url object to be serialized.

        Returns:
            str: String representation of url.
        """
        return str(url)

    @pydantic.field_validator("vocabularies", mode="after")
    @classmethod
    def check_vocabularies(cls, values: list[str]) -> list[str]:
        """Custom validation of the vocabularies field.

        Args:
            values (list[str]): The provided vocabularies initial value.

        Returns:
            list[str]: The validated vocabulary ids.

        Raises:
            KeyError: A provided vocabulary id does not exist.
        """
        # Check each provided name to see if it exists in the registry
        for name in values:
            if utils.vocabs.get_vocab(name) is None:
                raise ValueError(f"Vocabulary id {name} does not exist.")

        # Return list
        return values

    def get_vocab(self, name: str | None = None) -> Type[utils.vocabs.Vocabulary]:
        """Retrieves the vocab for the field.

        Args:
            name (str | None, optional): The name of the vocab to retrieve. Will
                return first vocab if not provided.

        Returns:
            Type[utils.vocabs.Vocabulary]: Returns vocabulary for the field.

        Raises:
            ValueError: If name is not within the vocabularies field.
        """
        # Check if name exists
        if name is not None and name not in self.vocabularies:
            raise ValueError(f"Vocabulary '{name}' is not defined for field {self.name}.")

        # Retrieve
        if name is not None:
            return utils.vocabs.get_vocab(name)

        return utils.vocabs.get_vocab(self.vocabularies[0])

    @property
    def publishable_vocabularies(self) -> list[str]:
        """Returns a list of only those vocabularies that are publishable.

        Returns:
            list[str]: The publishable vocabularies.
        """
        # Filter and return
        return [v for v in self.vocabularies if self.get_vocab(v).publish]


class Schema(pydantic.BaseModel):
    """Model for a template's schema descriptor.

    Typically defined using a `schema.json` file within a template's file structure.
    All properties are currently defined by the [frictionless table schema](https://specs.frictionlessdata.io/table-schema/)
    however, `fields` and `fields.constraints` are customised implementations for the project.
    """

    fields: Annotated[
        list[Field],
        pydantic.Field(
            description="[Frictionless reference](https://specs.frictionlessdata.io/table-schema/#descriptor). An array where each entry in the array is a field descriptor.",
        ),
    ]
    primaryKey: Annotated[
        str | None,
        pydantic.Field(
            description="[Used by frictionless](https://specs.frictionlessdata.io/table-schema/#primary-key), currently only supporting single values, contains the name of a field that effectively gets set to `required: true` and unique, and can provide reference for foreign keys when used in a Data Package.",
        ),
    ] = None
    foreignKeys: Annotated[
        list[dict[str, Any]] | None,
        pydantic.Field(
            description="[Used by frictionless](https://specs.frictionlessdata.io/table-schema/#foreign-keys), a foreign key is a reference where values in a field (or fields) on the table (‘resource’ in data package terminology) described by this Table Schema connect to values a field (or fields) on this or a separate table (resource). They are directly modelled on the concept of foreign keys in SQL.",
        ),
    ] = None

    # Allow extra fields to be captured mainly to catch errors in json
    model_config = pydantic.ConfigDict(extra="allow")
