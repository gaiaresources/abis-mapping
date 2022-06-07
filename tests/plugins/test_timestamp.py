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
    field = frictionless.Field(type="any")
    result = plugin.create_type(field)
    assert result is None

    # Correct Type
    field = frictionless.Field(type="timestamp")
    result = plugin.create_type(field)
    assert isinstance(result, plugins.timestamp.TimestampType)


def test_timestamp_type() -> None:
    """Tests the Timestamp Type"""
    # Instantiate the Type
    type = plugins.timestamp.TimestampType(field=frictionless.Field())

    # Read Invalid Cells
    assert type.read_cell(123) is None
    assert type.read_cell("hello world") is None
    assert type.read_cell("2022-04-26T22:00:00") is None  # No Timezone

    # Read Valid Cells
    assert type.read_cell("26/04/2022")  # Date
    assert type.read_cell("2022-04-26")  # Date
    assert type.read_cell("2022-04-26T22:00:00Z")  # Date Time with Timezone
    assert type.read_cell("2022-04-26T22:00:00+08:00")  # Date Time with Timezone

    # Write Cell
    assert type.write_cell(datetime.datetime.now())
