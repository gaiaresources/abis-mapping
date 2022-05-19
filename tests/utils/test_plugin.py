"""Provides Unit Tests for the `abis_mapping.utils.plugin` module"""


# Standard
import datetime

# Third-Party
import frictionless
import pytest

# Local
from abis_mapping import utils


def test_plugin_timestamp_plugin() -> None:
    """Tests the Timestamp Plugin"""
    # Instantiate the Plugin
    plugin = utils.plugin.TimestampPlugin()

    # Incorrect Type
    field = frictionless.Field(type="any")
    result = plugin.create_type(field)
    assert result is None

    # Correct Type
    field = frictionless.Field(type="timestamp")
    result = plugin.create_type(field)
    assert isinstance(result, utils.plugin.TimestampType)


def test_plugin_timestamp_type() -> None:
    """Tests the Timestamp Type"""
    # Instantiate the Type
    type = utils.plugin.TimestampType(field=frictionless.Field())

    # Read Invalid Cells
    assert type.read_cell(123) is None
    assert type.read_cell("hello world") is None
    assert type.read_cell("2022-04-26T22:00:00") is None  # No Timezone

    # Read Valid Cells
    assert type.read_cell("2022-04-26")  # Date
    assert type.read_cell("26/04/2022")  # Date
    assert type.read_cell("2022-04-26T22:00:00Z")  # Date Time with Timezone
    assert type.read_cell("2022-04-26T22:00:00+08:00")  # Date Time with Timezone

    # Write Cell
    assert type.write_cell(datetime.datetime.now())


def test_plugin_parse_timestamp() -> None:
    """Tests the Timestamp Parser"""
    # Parse Invalid Timestamps
    with pytest.raises(ValueError):
        utils.plugin.parse_timestamp(123)  # type: ignore
    with pytest.raises(ValueError):
        utils.plugin.parse_timestamp("hello world")
    with pytest.raises(ValueError):
        utils.plugin.parse_timestamp("2022-04-26T22:00:00")
    with pytest.raises(ValueError):
        utils.plugin.parse_timestamp("2022")
    with pytest.raises(ValueError):
        utils.plugin.parse_timestamp("2022-04")

    # Parse Valid Timestamps
    assert utils.plugin.parse_timestamp("2022-04-26").isoformat() == "2022-04-26"
    assert utils.plugin.parse_timestamp("26/04/2022").isoformat() == "2022-04-26"
    assert utils.plugin.parse_timestamp("2022-04-26T22Z").isoformat() == "2022-04-26T22:00:00+00:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00Z").isoformat() == "2022-04-26T22:00:00+00:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00Z").isoformat() == "2022-04-26T22:00:00+00:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00.000Z").isoformat() == "2022-04-26T22:00:00+00:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00.000000Z").isoformat() == "2022-04-26T22:00:00+00:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22+08:00").isoformat() == "2022-04-26T22:00:00+08:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00+08:00").isoformat() == "2022-04-26T22:00:00+08:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00+08:00").isoformat() == "2022-04-26T22:00:00+08:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00.000+08:00").isoformat() == "2022-04-26T22:00:00+08:00"
    assert utils.plugin.parse_timestamp("2022-04-26T22:00:00.000000+08:00").isoformat() == "2022-04-26T22:00:00+08:00"
