import frictionless

from abis_mapping import plugins


def test_customized_string_plugin() -> None:
    """Tests the customized string plugin"""
    # Instantiate plugin
    plugin = plugins.string_customized.CustomizedStringPlugin()

    # Incorrect type
    result = plugin.select_field_class("notAType")
    assert result is None

    # Type this plugin overrides field class for
    result = plugin.select_field_class("string")
    assert result is plugins.string_customized.CustomizedStringField


def test_customized_string_registered() -> None:
    """Tests the customized string class is used for string fields."""
    # Create schema with string field
    schema = frictionless.Schema.from_descriptor({"fields": [{"name": "foo", "type": "string"}]})

    # Extract string field
    field = schema.get_field("foo")

    # field is our custom class
    assert isinstance(field, plugins.string_customized.CustomizedStringField)


def test_customized_string_field() -> None:
    """Tests the customized string field."""
    # Instantiate the field
    field = plugins.string_customized.CustomizedStringField(name="TestField")

    # Normal string field behavior
    assert field.read_cell("") == (None, None)
    assert field.read_cell("foo") == ("foo", None)
    assert field.read_cell("  foo") == ("  foo", None)
    assert field.read_cell("foo  ") == ("foo  ", None)

    # All whitespace value is customized to None
    assert field.read_cell(" ") == (None, None)
    assert field.read_cell("  ") == (None, None)
    assert field.read_cell("\n ") == (None, None)
    assert field.read_cell(" \r\n") == (None, None)
    assert field.read_cell(" \t ") == (None, None)


def test_customized_string_field_with_required_constraint() -> None:
    """Tests the customized string field with a required constraint."""
    # Instantiate the field
    required_field = plugins.string_customized.CustomizedStringField(
        name="TestField",
        constraints={"required": True},
    )

    # normal string field behavior
    assert required_field.read_cell("foo") == ("foo", None)
    assert required_field.read_cell("") == (None, {"required": 'constraint "required" is "True"'})

    # Normalization is applied before checking constraint, making these invalid.
    assert required_field.read_cell("  ") == (None, {"required": 'constraint "required" is "True"'})
    assert required_field.read_cell("\t") == (None, {"required": 'constraint "required" is "True"'})


def test_using_customized_string_field_with_resource() -> None:
    """Test reading a valid csv where the cells are string fields."""
    # Create schema with some string fields
    schema = frictionless.Schema.from_descriptor(
        {
            "fields": [
                {"name": "ID", "type": "string", "constraints": {"unique": True}},
                {"name": "foo", "type": "string"},
                {"name": "bar", "type": "string"},
            ],
        },
    )
    data = b"\r\n".join(
        [
            b"ID,foo,bar",
            b"AA,fff,\t ",
            b"BB,   ,bar",
        ],
    )
    resource = frictionless.Resource(
        data=data,
        schema=schema,
        format="csv",
        encoding="utf-8",
    )

    report = resource.validate()
    assert report.valid
    with resource.open() as r:
        assert list(r.row_stream) == [
            {"ID": "AA", "foo": "fff", "bar": None},
            {"ID": "BB", "foo": None, "bar": "bar"},
        ]


def test_customized_string_field_as_unique_field() -> None:
    """Tests that checking if a unique field has all distinct values is done after normalization is applied."""
    # Create schema with unique string field
    schema = frictionless.Schema.from_descriptor(
        {
            "fields": [
                {"name": "ID", "type": "string", "constraints": {"unique": True}},
                {"name": "foo", "type": "string"},
            ],
        },
    )
    # The unique "ID" field has duplicate raw values,
    # but these are converted to null by our custom class,
    # and so are not included in the unique check.
    data = b"\r\n".join(
        [
            b"ID,foo",
            b"AA,22",
            b"  ,33",
            b"  ,44",
            b"\t,55",
            b"\t,66",
        ],
    )
    resource = frictionless.Resource(
        data=data,
        schema=schema,
        format="csv",
        encoding="utf-8",
    )

    report = resource.validate()

    assert report.valid
    with resource.open() as r:
        assert list(r.row_stream) == [
            {"ID": "AA", "foo": "22"},
            {"ID": None, "foo": "33"},
            {"ID": None, "foo": "44"},
            {"ID": None, "foo": "55"},
            {"ID": None, "foo": "66"},
        ]
