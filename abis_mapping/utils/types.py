"""Provides Utils Types for the Package"""


# Standard
import datetime
import frictionless.fields

# Typing
from typing import Union


# Define Union Timestamp Type (Date, DateTime, Yearmonth or Year)
Timestamp = Union[
    datetime.date,
    datetime.datetime,
    frictionless.fields.yearmonth.yearmonth,
    int,
]
