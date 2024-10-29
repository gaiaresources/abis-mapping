# Schema

Model for a template's schema descriptor.

Typically defined using a `schema.json` file within a template's file structure.
All properties are currently defined by the [frictionless table schema](https://specs.frictionlessdata.io/table-schema/)
however, `fields` and `fields.constraints` are customised implementations for the project.

### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| fields | `array` | ✅ | [Field](#field) | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#descriptor). An array where each entry in the array is a field descriptor. |
| primaryKey | `string` or `null` |  | string | [Used by frictionless](https://specs.frictionlessdata.io/table-schema/#primary-key), currently only supporting single values, contains the name of a field that effectively gets set to `required: true` and unique, and can provide reference for foreign keys when used in a Data Package. |
| foreignKeys | `array` or `null` |  | object | [Used by frictionless](https://specs.frictionlessdata.io/table-schema/#foreign-keys), a foreign key is a reference where values in a field (or fields) on the table (‘resource’ in data package terminology) described by this Table Schema connect to values a field (or fields) on this or a separate table (resource). They are directly modelled on the concept of foreign keys in SQL. |


---

# Definitions

## Constraints

The constraints of a schema field.

Currently all defined below are a subset of those available from [frictionless](https://specs.frictionlessdata.io/table-schema/#constraints).

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| required | `boolean` | ✅ | boolean | Indicates whether this field cannot be null. If required is false (the default), then null is allowed. |
| unique | `boolean` or `null` |  | boolean | If true, then all values for that field MUST be unique within the data file in which it is found. |
| minimum | `integer` or `number` or `null` |  | integer and/or number | Specifies a minimum value for a field. This is different to minLength which checks the number of items in the value. A minimum value constraint checks whether a field value is greater than or equal to the specified value. The range checking depends on the type of the field. If a minimum value constraint is specified then the field descriptor MUST contain a type key. |
| maximum | `integer` or `number` or `null` |  | integer and/or number | As for `minimum`, but specifies a maximum value for a field. |
| enum | `array` or `null` |  | string | The value of the field must exactly match a value in the enum array. |

## Field

Field model of a schema.

The properties of a field consisting of those properties used by frictionless for performing validations as well
as extras to assist with the looking up of vocabularies when mapping as well as assisting with the creation
of instruction documentation.
[Frictionless reference](https://specs.frictionlessdata.io/table-schema).

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| name | `string` | ✅ | string | [Required by frictionless](https://specs.frictionlessdata.io/table-schema/#name). The field descriptor MUST contain a name property. This property SHOULD correspond to the name of field/column in the data file (if it has a name). As such it SHOULD be unique (though it is possible, but very bad practice, for the data file to have multiple columns with the same name). name SHOULD NOT be considered case sensitive in determining uniqueness. However, since it should correspond to the name of the field in the data file it may be important to preserve case. |
| title | `string` | ✅ | string | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#title). A human readable label or title for the field. |
| description | `string` | ✅ | string | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#description). A description for this field e.g. "The recipient of the funds". |
| type | `string` | ✅ | string | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#types-and-formats). `type` and `format` properties are used to give the type of the field. A fields `type` property is a string indicating the type of this field. |
| format | `string` or `null` | ✅ | string | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#types-and-formats). `type` and `format` properties are used to give the type of the field. A field's `format` property is a string, indicating a format for the field type. |
| constraints | `object` | ✅ | [Constraints](#constraints) |  |
| example | `string` or `null` |  | string | [Frictionless reference](https://specs.frictionlessdata.io/table-schema/#example). An example value of the field |
| url | `string` or `null` |  | Format: [`uri`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) | The IRI of the field's concept. |
| vocabularies | `array` |  | string | Optional list of vocabulary IDs, defined internally within the project. Provided IDs need to have been registered to be valid. See [`abis_mapping.vocabs`](/abis_mapping/vocabs/). |
