"""Provides Utils Types for the Package"""


# Standard
import datetime
import abc
import calendar

# Typing
from typing import Tuple, Any


class Timestamp(abc.ABC):

    @abc.abstractmethod
    def to_datetime(self, round_up: bool) -> datetime.datetime:
        raise NotImplementedError

    def __gt__(self, other: "Timestamp") -> bool:
        (dt1, dt2) = set_offsets_for_comparison(
            self.to_datetime(round_up=True),
            other.to_datetime(round_up=False)
        )
        return dt1 > dt2

    def __lt__(self, other: "Timestamp") -> bool:
        (dt1, dt2) = set_offsets_for_comparison(
            self.to_datetime(round_up=False),
            other.to_datetime(round_up=True)
        )
        return dt1 < dt2


class Datetime(datetime.datetime, Timestamp):
    def to_datetime(self, _: bool) -> datetime.datetime:
        return self


class Date(datetime.date, Timestamp):
    def to_datetime(self, round_up: bool) -> datetime.datetime:
        time = datetime.time.max if round_up else datetime.time.min
        return datetime.datetime.combine(self, time)


class YearMonth(Timestamp):

    def __init__(self, year: int, month: int) -> None:
        if not is_year(year):
            raise ValueError(f"Invalid year: {year}")
        if not is_month(month):
            raise ValueError(f"Invalid month: {month}")
        self._year = year
        self._month = month

    def to_datetime(self, round_up: bool) -> datetime.datetime:
        day = self.max_date() if round_up else 1
        return Date(self._year, self._month, day).to_datetime(round_up=round_up)

    def max_date(self) -> int:
        """Determines the max date for the month

        Returns:
            int: date of the last day of the month
        """
        _, last_day = calendar.monthrange(self._year, self._month)
        return last_day


class Year(int, Timestamp):
    def to_datetime(self, round_up: bool) -> datetime.datetime:
        ym = YearMonth(self, 12) if round_up else YearMonth(self, 1)
        return ym.to_datetime(round_up=round_up)


class TimestampFactory:
    def __init__(self, value: Any) -> None:
        """

        Args:
            value (Any): The underlying value, the type
                will either return an instance of one of
                    - Datetime
                    - Date
                    - Yearmonth
                    - Year
        """


# # Define Union Timestamp Type (Date, DateTime, Yearmonth or Year)
# Timestamp = Union[
#     datetime.date,
#     datetime.datetime,
#     YearMonth,
#     int,
# ]


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
