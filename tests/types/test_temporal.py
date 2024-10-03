"""Provides Unit Tests for the `abis_mapping.utils.timestamps` module"""

# Third-Party
import pytest
import rdflib

# Standard
import datetime
import contextlib

# Local
from abis_mapping.types import temporal

# Typing
from typing import Any, Tuple


@pytest.mark.parametrize(
    ["raw", "expected"],
    [
        ("26/04/2022", "2022-04-26"),
        ("2022-04-26", "2022-04-26"),
        ("2022-04-26T22Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00.000Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22:00:00.000000Z", "2022-04-26T22:00:00+00:00"),
        ("2022-04-26T22+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00.000+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04-26T22:00:00.000000+08:00", "2022-04-26T22:00:00+08:00"),
        ("2022-04", "2022-04"),
        ("04/2022", "2022-04"),
        ("4/2022", "2022-04"),
        ("2022", "2022"),
    ],
)
def test_timestamp_parse_valid(raw: str, expected: str) -> None:
    """Tests the Timestamp Parser with Valid Input

    Args:
        raw (str): Raw string to parse.
        expected (str): Expected result of parsing the raw string.
    """
    # Parse Valid Timestamp
    assert str(temporal.parse_timestamp(raw)) == expected


@pytest.mark.parametrize(
    [
        "raw",
    ],
    [
        ("hello world",),
        ("26/04/2022 22:00:00Z",),
        ("22",),
        ("2022-4",),
    ],
)
def test_timestamp_parse_invalid(raw: Any) -> None:
    """Tests the Timestamp Parser with Invalid Input

    Args:
        raw (str): Raw string to parse.
    """
    # Parse Invalid Timestamps
    with pytest.raises(ValueError):
        temporal.parse_timestamp(raw)


@pytest.mark.parametrize(
    "tstmps,is_ordered",
    [
        # Scenario 1
        (
            [
                temporal.Datetime(2022, 9, 11, 15, 15, 15),
                temporal.Datetime(2023, 9, 11, 15, 15, 15),
                temporal.Date(2023, 10, 11),
                temporal.Date(2023, 10, 11),
                temporal.Datetime(2023, 10, 12, 0, 0, 1),
                temporal.YearMonth(2023, 11),
                temporal.YearMonth(2023, 12),
                temporal.Year(2024),
                temporal.Year(2024),
                temporal.YearMonth(2024, 1),
            ],
            True,
        ),
        # Scenario 2
        (
            [
                temporal.Date(2022, 9, 11),
                temporal.Datetime(2023, 10, 11, 15, 15, 15),
                temporal.Datetime(2023, 9, 11, 15, 15, 15),
            ],
            False,
        ),
        # Scenario 3
        (
            [
                temporal.Datetime(2023, 9, 11, 15, 15, 15),
                temporal.Datetime(2023, 9, 11, 15, 15, 14),
            ],
            False,
        ),
    ],
)
def test_timestamp_le_comparison(tstmps: list[temporal.Timestamp], is_ordered: bool) -> None:
    """Tests implementation of the __le__ method for timestamp types."""

    # Check chronologically increasing
    assert all(x <= y for x, y in zip(tstmps[:-1], tstmps[1:], strict=True)) == is_ordered


@pytest.mark.parametrize(
    "year,month,expected,raise_error",
    [
        (2022, 4, 30, contextlib.nullcontext()),
        (2022, 12, 31, contextlib.nullcontext()),
        (2022, 2, 28, contextlib.nullcontext()),
        (2022, 13, 0, pytest.raises(ValueError)),
        (-5, 12, 0, pytest.raises(ValueError)),
    ],
)
def test_max_date(
    year: int,
    month: int,
    expected: int,
    raise_error: contextlib.AbstractContextManager,
) -> None:
    """Tests the functionality of the max_data function.

    Args:
        year (int): Year input
        month (int): Month input
        expected (int): Expected return
        raise_error (contextlib.AbstractContextManager | pytest.RaisesContext | pytest.ExceptionInfo):
            Exception to be raised or not.
    """
    with raise_error:
        assert temporal.YearMonth(year, month).max_date == expected


class TestSharedParams:
    """These tests grouped up as they have shared parameters formed through class attributes."""

    # Constants to create shared test params
    dt1 = temporal.Datetime(1111, 1, 1, 1, 1, 1)
    dt2 = temporal.Datetime(2222, 2, 2, 2, 2, 2)
    date1 = temporal.Date(2022, 4, 4)
    max_time = datetime.time.max
    min_time = datetime.time.min
    ym1 = temporal.YearMonth(2022, 4)
    y1 = temporal.Year(2022)

    @pytest.mark.parametrize(
        "inputs,expected",
        [
            # Both naive
            ((dt1, dt2), (dt1, dt2)),
            # Both timezoned same
            (
                (
                    dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                    dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                ),
                (
                    dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                    dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                ),
            ),
            # Both timezoned different
            (
                (
                    dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                    dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=2))),
                ),
                (
                    dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                    dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=2))),
                ),
            ),
            # First timezoned second naive
            ((dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))), dt2), (dt1, dt2)),
            # Second timezoned first naive
            ((dt1, dt2.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1)))), (dt1, dt2)),
        ],
    )
    def test_set_offsets_for_comparison(
        self,
        inputs: Tuple[datetime.datetime, datetime.datetime],
        expected: Tuple[datetime.datetime, datetime.datetime],
    ) -> None:
        """Tests the set_offsets_for_comparison function.

        Args:
            inputs (datetime.datetime, datetime.datetime): Inputs args for the function
            expected (datetime.datetime, datetime.datetime): Expected returned
        """
        assert temporal.set_offsets_for_comparison(*inputs) == expected

    @pytest.mark.parametrize(
        "timestamp,round_up,expected",
        [
            # datetime with timezone
            (
                dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
                False,
                dt1.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
            ),
            # datetime naive
            (dt1, False, dt1),
            # date
            (date1, False, datetime.datetime.combine(date1, min_time)),
            # date roundup
            (date1, True, datetime.datetime.combine(date1, max_time)),
            # yearmonth
            (ym1, False, datetime.datetime.combine(datetime.date(ym1._year, ym1._month, 1), min_time)),
            # yearmonth roundup
            (ym1, True, datetime.datetime.combine(datetime.date(ym1._year, ym1._month, 30), max_time)),
            # year
            (y1, False, datetime.datetime.combine(datetime.date(2022, 1, 1), min_time)),
            # year roundup
            (y1, True, datetime.datetime.combine(datetime.date(2022, 12, 31), max_time)),
        ],
    )
    def test_transform_timestamp_to_datetime(
        self, timestamp: temporal.Timestamp, round_up: bool, expected: datetime.datetime
    ) -> None:
        """Tests the transform_timestamp_to_datetime function.

        Args:
            timestamp (temporal.Timestamp): Input to be converted
            round_up (bool): Whether to round up the timestamp up when converting.
            expected (datetime.datetime): Expected output
        """
        assert timestamp.to_datetime(round_up=round_up) == expected


@pytest.mark.parametrize(
    "time,expected",
    [
        # Test Datetime with Timezone
        (temporal.Datetime.now().astimezone(datetime.timezone.utc), rdflib.TIME.inXSDDateTimeStamp),
        # Test Datetime without Timezone
        (temporal.Datetime.now(), rdflib.TIME.inXSDDateTime),
        # Test Date
        (temporal.Date.today(), rdflib.TIME.inXSDDate),
        # Test Yearmonth
        (temporal.YearMonth(year=2022, month=12), rdflib.TIME.inXSDgYearMonth),
        # Test Year
        (temporal.Year(2022), rdflib.TIME.inXSDgYear),
    ],
)
def test_rdf_in_xsd(time: temporal.Timestamp, expected: rdflib.URIRef) -> None:
    """Tests the rdf_in_xsd parameter method.

    Args:
        time (temporal.Timestamp): input timestamp.
        expected (rdflib.URIRef): expected output.
    """
    # Call function and assert
    predicate = time.rdf_in_xsd
    assert predicate == expected


@pytest.mark.parametrize(
    "time,expected_datatype",
    [
        # Test Datetime with Timezone
        (temporal.Datetime.now().astimezone(datetime.timezone.utc), rdflib.XSD.dateTimeStamp),
        # Test Datetime without Timezone
        (temporal.Datetime.now(), rdflib.XSD.dateTime),
        # Test Date
        (temporal.Date.today(), rdflib.XSD.date),
        # Test Year month
        (temporal.YearMonth(year=2022, month=4), rdflib.XSD.gYearMonth),
        # Test year only
        (temporal.Year(2022), rdflib.XSD.gYear),
    ],
)
def test_to_rdf_literal(time: temporal.Timestamp, expected_datatype: rdflib.Literal) -> None:
    """Tests the to_rdf_literal() method."""
    # Invoke method
    literal = time.to_rdf_literal()

    # Build expected literal and compare
    assert literal == rdflib.Literal(str(time), datatype=expected_datatype)


def test_year_constructor_raises_value_error() -> None:
    """Tests the year constructor raises value error."""
    with pytest.raises(ValueError):
        temporal.Year(10101)


def test_datetime_strptime_returns_timestamp() -> None:
    """Tests that the Datetime.strptime() method returns a Datetime (not datetime)."""
    dt = temporal.Datetime.strptime("26/04/2022", "%d/%m/%Y")
    assert isinstance(dt, temporal.Datetime)
    # Verify date() returns Date
    assert isinstance(dt.date(), temporal.Date)
