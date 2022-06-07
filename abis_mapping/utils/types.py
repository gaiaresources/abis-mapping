"""Provides Utils Types for the Package"""


# Standard
import datetime

# Typing
from typing import Union


# Define Union Timestamp Type (Date or DateTime)
DateOrDatetime = Union[
    datetime.date,
    datetime.datetime,
]
