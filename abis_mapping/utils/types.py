"""Provides Utils Types for the Package"""


# Standard
import datetime
import abc
import calendar
import re
import contextlib
import dateutil.parser

# Third-party
import rdflib

# Typing
from typing import Tuple, Any


class Timestamp(abc.ABC):
    """Common interface for Timestamp types."""
    @abc.abstractmethod
    def to_datetime(self, round_up: bool) -> datetime.datetime:
        """Converts a Timestamp to a datetime.

        Args:
            round_up (bool): Will round up to latest moment in
                time for the object else earliest.

        Returns:
            datetime.datetime: The corresponding rounded datetime
        """

    @property
    @abc.abstractmethod
    def rdf_in_xsd(self) -> rdflib.URIRef:
        """Getter for the inXSDxxxx IRI corresponding to the type.

        Returns:
            rdflib.URIRef: The appropriate inXSDxxxx IRI.
        """

    @property
    @abc.abstractmethod
    def rdf_datatype(self) -> rdflib.URIRef:
        """Getter for the rdf datatype IRI corresponding to the type.

        Returns:
            rdflib.URIRef: The appropriate rdf datatype IRI.
        """

    def to_rdf_literal(self) -> rdflib.Literal:
        """Converts to rdf literal object.

        Returns:
            rdflib.Literal: The converted literal.
        """
        return rdflib.Literal(self, datatype=self.rdf_datatype)

    def __le__(self, other: "Timestamp") -> bool:
        """Performs less than or equal comparison

        Args:
            other (Timestamp): Other timestamp to compare to.

        Returns:
            bool: True if this timestamp is less than or equal other.
        """
        # Convert each operand to datetime and set offsets for comparison
        (dt1, dt2) = set_offsets_for_comparison(
            self.to_datetime(round_up=False),
            other.to_datetime(round_up=True)
        )

        # Return datetime comparison
        return dt1 <= dt2


class Date(Timestamp, datetime.date):
    @property
    def rdf_in_xsd(self) -> rdflib.URIRef:
        """Getter for the inXSDxxxx URI.

        Returns:
            rdflib.URIRef: the appropriate inXSD URI
        """
        return rdflib.TIME.inXSDDate

    @property
    def rdf_datatype(self) -> rdflib.URIRef:
        """Getter for literal datatype.

        Returns:
            rdflib.URIRef: URI to be used for the datatype.
        """
        return rdflib.XSD.date

    def to_datetime(self, round_up: bool) -> datetime.datetime:
        """Convert and return as datetime.

        Args:
            round_up (bool): Whether to round up the time.

        Returns:
            datetime.datetime: with first moment of the given date
                if round_up is False else the last moment
        """
        time = datetime.time.max if round_up else datetime.time.min
        return datetime.datetime.combine(self, time)

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: Date in ISO format
        """
        return self.isoformat()

    def __new__(cls, *args: Any, **kwargs: Any) -> "Date":
        """Create new instance of Date

        Args:
            *args: Positional arguments provided
            **kwargs:Keyword arguments provided

        Returns:
            Date: A new instance of Date
        """
        return super(Date, cls).__new__(cls, *args, **kwargs)


class Datetime(Timestamp, datetime.datetime):
    @property
    def rdf_in_xsd(self) -> rdflib.URIRef:
        """Getter for the inXSDxxxx uri.

        Returns:
            rdflib.URIRef: the corresponding inXSD uri for the given datetime.
        """
        return rdflib.TIME.inXSDDateTime if self.tzinfo is None else rdflib.TIME.inXSDDateTimeStamp

    @property
    def rdf_datatype(self) -> rdflib.URIRef:
        """Getter for rdf datatype URI.

        Returns:
            rdflib.URIRef: XSD datatype URI that the datetime corresponds.
        """
        return rdflib.XSD.dateTime if self.tzinfo is None else rdflib.XSD.dateTimeStamp

    def to_datetime(self, round_up: bool) -> datetime.datetime:
        """Return datetime object.

        Args:
            round_up (bool): Not used

        Returns:
            datetime.datetime: A datetime.datetime instance
        """
        return datetime.datetime.fromtimestamp(self.timestamp(), tz=self.tzinfo)

    def date(self) -> Date:
        """Returns a Date instance from the instance.

        Returns:
            Date: consists of year, month, day of current object.
        """
        return Date(self.year, self.month, self.day)

    def __str__(self) -> str:
        """String representation

        Returns:
            str: ISO format of datetime
        """
        return self.isoformat()

    def __new__(cls, *args: Any, **kwargs: Any) -> "Datetime":
        """Create new instance of Datetime

        Args:
            *args: Positional arguments provided
            **kwargs: Keyword arguments provided

        Returns:
            Date: A new instance of Datetime
        """
        return super(Datetime, cls).__new__(cls, *args, **kwargs)


class YearMonth(Timestamp):

    def __init__(self, year: int, month: int) -> None:
        """Constructor for YearMonth

        Args:
            year (int): Value representing the year.
            month (int): Value representing the month.
        """
        if not is_year(year):
            raise ValueError(f"Invalid year: {year}")
        if not is_month(month):
            raise ValueError(f"Invalid month: {month}")
        self._year = year
        self._month = month

    def to_datetime(self, round_up: bool) -> datetime.datetime:
        """Convert to datetime.datetime object.

        Args:
            round_up: whether to round up to the last moment of the corresponding
                month or the earliest.

        Returns:
            datetime.datetime: Rounded datetime object.
        """
        day = self.max_date if round_up else 1
        return Date(self._year, self._month, day).to_datetime(round_up=round_up)

    @property
    def rdf_in_xsd(self) -> rdflib.URIRef:
        """Getter for the inXSDxxxx uri.

        Returns:
            rdflib.URIRef: the corresponding inXSD uri for the given YearMonth.
        """
        return rdflib.TIME.inXSDgYearMonth

    @property
    def rdf_datatype(self) -> rdflib.URIRef:
        """Getter for the rdf datatype.

        Returns:
            rdflib.URIRef: the appropriate rdf datatype.
        """
        return rdflib.XSD.gYearMonth

    @property
    def max_date(self) -> int:
        """Determines the max date for the month

        Returns:
            int: date of the last day of the month
        """
        _, last_day = calendar.monthrange(self._year, self._month)
        return last_day

    def __str__(self) -> str:
        """String representation

        Returns:
            str: String representation of the YearMonth
        """
        return f"{self._year}-{self._month:02}"

    def __eq__(self, other: object) -> bool:
        """Performs equality test.

        Args:
            other (YearMonth): The other operand

        Returns:
            bool: True if both year and month are equal, False otherwise
        """
        if not isinstance(other, YearMonth):
            raise NotImplementedError(f"Unable to compare YearMonth and {type(object)}")
        return self._year == other._year and self._month == other._month


class Year(Timestamp):

    def __init__(self, year: int) -> None:
        """Year constructor.

        Args:
            year (int): Value to represent the year.
        """
        if not is_year(year):
            raise ValueError(f"Invalid year: {year}")
        self._year = year

    @property
    def rdf_in_xsd(self) -> rdflib.URIRef:
        """Getter property for RDF predicate.

        Returns:
            rdflib.URIRef: RDF XSD for a gYear
        """
        return rdflib.TIME.inXSDgYear

    @property
    def rdf_datatype(self) -> rdflib.URIRef:
        """Getter property for RDF datatype of XSD's gYear.

        Returns:
            rdflib.URIRef: RDF datatype for XSD's gYear.
        """
        return rdflib.XSD.gYear

    def __str__(self) -> str:
        """Returns a string representation of the year.

        Returns:
            str: String representation of the year
        """
        return f"{self._year}"

    def __eq__(self, other: object) -> bool:
        """Performs equality test.

        Args:
            other (object): Other operand.

        Returns:
            bool: True if both _year values are equal, False otherwise.
        """
        if not isinstance(other, Year):
            raise NotImplementedError(f"Unable to compare Year and {type(other)}")
        return self._year == other._year

    def to_datetime(self, round_up: bool) -> datetime.datetime:
        """Converts Year and returns a datetime object

        Args:
            round_up (bool): Round up the produced datetime value

        Returns:
            datetime.datetime: Either the first moment of a given year
                or last depending on `round_up`
        """
        ym = YearMonth(self._year, 12) if round_up else YearMonth(self._year, 1)
        return ym.to_datetime(round_up=round_up)


def parse_timestamp(raw: str) -> Timestamp:
    """Parses a string value into a Timestamp object.

      Args:
          raw (str): The string representation of the timestamp.

      Returns:
          Timestamp: An instance of Timestamp or its subclasses (Year, YearMonth, Date, Datetime).

      Raises:
          ValueError: If the input value cannot be parsed as a valid timestamp.
    """
    # Regular expressions for matching different timestamp formats
    year_only = re.compile(r"^\d{4}$")
    year_month_dash = re.compile(r"^(\d{4})-(\d{2})$")
    year_month_slash = re.compile(r"^(\d{1,2})/(\d{4})$")

    # Check if the value matches the 'year_only' format (e.g., "2022")
    if year_only.match(raw):
        year = int(raw)
        return Year(year)

    # Check if the value matches the 'year_month_dash' format (e.g., "2022-12")
    elif match := year_month_dash.match(raw):
        month = int(match.group(2))
        year = int(match.group(1))
        # Defer handling of exceptions until the final statement
        try:
            return YearMonth(year, month)
        except ValueError:
            pass

    # Check if the value matches the 'year_month_slash' format (e.g., "12/2022")
    elif match := year_month_slash.match(raw):
        month = int(match.group(1))
        year = int(match.group(2))
        # Defer handling of exceptions until the final statement
        try:
            return YearMonth(year, month)
        except ValueError:
            pass

    # (1) Try Parse as ISO86001 Date
    with contextlib.suppress(Exception):
        return Date.fromisoformat(raw)

    # (2) Try Parse as `dd/mm/YYYY` Date
    with contextlib.suppress(Exception):
        d = Datetime.strptime(raw, "%d/%m/%Y").date()
        # This assertion is included to prove to mypy that the
        # type returned from the previous statement is of a
        # Timestamp type i.e. Date.
        assert isinstance(d, Date)
        return d

    # (3) Try Parse as ISO Datetime with Timezone
    with contextlib.suppress(Exception):
        assert len(raw) > 10  # Shortcut to disable some formats we don't want
        timestamp = dateutil.parser.isoparse(raw)
        assert timestamp.tzinfo is not None
        return Datetime.fromtimestamp(timestamp.timestamp(), tz=timestamp.tzinfo)

    # Could not parse the string to a Timestamp type
    # Raise a ValueError
    raise ValueError(f"Could not parse '{raw}' as a timestamp")


def is_year(year: int) -> bool:
    """Determines if a valid year was supplied as arg.

    Args:
        year (int): Year contestant.

    Returns:
        bool: True if year is between 0 and 9999 else False
    """
    # Return check to see out of bounds
    return datetime.MINYEAR <= year <= datetime.MAXYEAR


def is_month(month: int) -> bool:
    """Determines if a valid month was supplied as arg.

    Args:
        month (int): Month contestant.

    Returns:
        bool: True if month is 1-12 else False.
    """
    # Return check
    return 1 <= month <= 12


def set_offsets_for_comparison(
    timestamp1: datetime.datetime,
    timestamp2: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns timestamps with potentially modified offsets to enable comparison.

    The assumption made by this function is that if one datetime is naive and the other
    is aware then they both belong to the same timezone. This results in the function
    returning naive datetimes for this situation.

    Args:
          timestamp1 (datetime.datetime): First timestamp involved in the comparison
          timestamp2 (datetime.datetime): Second timestamp involved in the comparison

    Returns:
        (datetime.datetime, datetime.datetime): Timestamps with appropriate timezone offsets,
            the first element corresponding to timestamp1 and the second to timestamp2.
    """
    # If both have tzinfo return unchanged
    if timestamp1.tzinfo is not None and timestamp2.tzinfo is not None:
        return timestamp1, timestamp2

    # Convert offset-aware datetime to naive and return
    return timestamp1.replace(tzinfo=None), timestamp2.replace(tzinfo=None)
