"""Provides Unit Tests for the `abis_mapping.plugins.timestamp` module"""


# Third-Party
import frictionless
import frictionless.fields

# Local
from abis_mapping import plugins
from abis_mapping import types


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
    schema: frictionless.Schema = frictionless.Schema.from_descriptor({
        'fields': [{'name': 'someTimestamp', 'type': 'timestamp'}]
    })

    # Extract timestamp field
    field = schema.get_field('someTimestamp')

    # Will only reach this assertion if schema created (i.e. timestamp type registered)
    assert not field.builtin


def test_timestamp_type() -> None:
    """Tests the Timestamp Type Date and Datetime types specifically."""
    # Instantiate the field
    field = plugins.timestamp.TimestampField(
        name="testField",
    )

    # Read Invalid Cells
    assert field.read_cell(123)[0] is None
    assert field.read_cell("hello world")[0] is None
    assert field.read_cell("2022-4-26")[0] is None
    assert field.read_cell("26/04/22")[0] is None
    assert field.read_cell("26/04/10101")[0] is None

    # Read Valid Cells
    assert field.read_cell("26/04/2022")[0]  # Date
    assert field.read_cell("26/04/0022")[0]  # Date
    assert field.read_cell("2022-04-26")[0]  # Date
    assert field.read_cell("2022-04-26T22:00:00")[0]  # No Timezone
    assert field.read_cell("2022-04-26T22:00:00Z")[0]  # Date Time with Timezone
    assert field.read_cell("2022-04-26T22:00:00+08:00")[0]  # Date Time with Timezone
    assert field.read_cell("2022-04-26T22:00+08:00")[0]  # Date Time with Timezone
    assert field.read_cell("2022-04-26T22:00+08")[0]  # Date Time with Timezone
    assert field.read_cell("2022-04-26 22:00+08")[0]  # Date Time with Timezone
    assert field.read_cell(types.temporal.Datetime.now())[0]

    # Write Cell
    assert field.write_cell(types.temporal.Datetime.now())[0]


def test_timestamp_type_year_month() -> None:
    """Tests the Timestamp type with year and month specifically."""
    # Instantiate the field
    field = plugins.timestamp.TimestampField(
        name="testField",
    )

    # Read invalid cells
    assert field.read_cell("04/22")[0] is None
    assert field.read_cell("2022-4")[0] is None
    assert field.read_cell("22-04")[0] is None
    assert field.read_cell("10101-04")[0] is None
    assert field.read_cell("2022-13")[0] is None
    assert field.read_cell("04/10101")[0] is None
    assert field.read_cell("13/2022")[0] is None

    # Read valid cells
    assert field.read_cell("2022-04")[0] == types.temporal.YearMonth(year=2022, month=4)  # Year month
    assert field.read_cell("04/2022")[0] == types.temporal.YearMonth(year=2022, month=4)  # Year month
    assert field.read_cell("4/2022")[0] == types.temporal.YearMonth(year=2022, month=4)  # Year month
    assert field.read_cell("04/0022")[0] == types.temporal.YearMonth(year=22, month=4)  # Year month
    assert field.read_cell(types.temporal.YearMonth(2022, 4))[0] ==\
           types.temporal.YearMonth(year=2022, month=4)  # Year month

    # Write cell
    assert field.write_cell(types.temporal.YearMonth(year=2022, month=4))[0] == "2022-04"


def test_ym_equality() -> None:
    """Tests the __eq__ implementation for YearMonth"""
    assert types.temporal.YearMonth(2022, 4) == types.temporal.YearMonth(2022, 4)


def test_year_equality() -> None:
    """Tests the __eq__ implementation for Year"""
    assert types.temporal.Year(2022) == types.temporal.Year(2022)


def test_timestamp_type_year() -> None:
    """Tests the Timestamp type year specifically."""
    # Instantiate the field
    field = plugins.timestamp.TimestampField(
        name="testField",
    )

    # Read invalid cells
    assert field.read_cell("22")[0] is None
    assert field.read_cell("10101")[0] is None
    assert field.read_cell(10101)[0] is None

    # Read valid cells
    assert field.read_cell("2022")[0] == types.temporal.Year(2022)
    assert field.read_cell(types.temporal.Year(2022))[0] == types.temporal.Year(2022)
    assert field.read_cell("0022")[0] == types.temporal.Year(22)

    # Write cell
    assert field.write_cell(types.temporal.Year(2022))[0] == "2022"
    assert field.write_cell(types.temporal.Datetime.now())[0]
