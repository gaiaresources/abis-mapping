"""Provides Unit Tests for the `abis_mapping.plugins.timestamp` module"""


# Standard
import datetime

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_timestamp_plugin() -> None:
    """Tests the Timestamp Plugin"""
    # Instantiate the Plugin
    plugin = plugins.timestamp.TimestampPlugin()

    # Incorrect Type
    result = plugin.select_field_class("notAType")
    assert result is None

    # Correct Type
    result = plugin.select_field_class("timestamp")
    assert result is plugins.timestamp.TimestampField


def test_timestamp_registered() -> None:
    """Tests the timestamp field type is registered."""
    # Create schema with timestamp field
    schema = frictionless.Schema.from_descriptor({
        'fields': [{'name': 'someTimestamp', 'type': 'timestamp'}]
    })

    # Extract timestamp field
    field = schema.get_field('someTimestamp')

    # Will only reach this assertion if schema created (i.e. timestamp type registered)
    assert not field.builtin


def test_timestamp_type() -> None:
    """Tests the Timestamp Type"""
    # Instantiate the field
    field = plugins.timestamp.TimestampField(
        name="testField",
    )

    # Read Invalid Cells
    assert field.read_cell(123)[0] is None
    assert field.read_cell("hello world")[0] is None
    assert field.read_cell("2022-04-26T22:00:00")[0] is None  # No Timezone

    # Read Valid Cells
    assert field.read_cell("26/04/2022")[0]  # Date
    assert field.read_cell("2022-04-26")[0]  # Date
    assert field.read_cell("2022-04-26T22:00:00Z")[0]  # Date Time with Timezone
    assert field.read_cell("2022-04-26T22:00:00+08:00")[0]  # Date Time with Timezone

    # Write Cell
    assert field.write_cell(datetime.datetime.now())[0]
