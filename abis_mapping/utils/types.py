"""Provides Utils Types for the Package"""


# Standard
import datetime

# Typing
from typing import Union, NamedTuple


# Definition of yearmonth
class YearMonth(NamedTuple):
    year: int
    month: int


# Define Union Timestamp Type (Date, DateTime, Yearmonth or Year)
Timestamp = Union[
    datetime.date,
    datetime.datetime,
    YearMonth,
    int,
]
