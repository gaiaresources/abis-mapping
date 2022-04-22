"""Provides Base Types for the Package"""


# Standard
import datetime

# Typing
from os import PathLike
from typing import IO, Union


# Define Readable Filepath and IO Type
ReadableType = Union[
    str,
    bytes,
    Union[str, PathLike[str]],
    IO[bytes],
    IO[str],
]

# Define Union Timestamp Type (Date or DateTime)
DateOrDatetime = Union[
    datetime.date,
    datetime.datetime,
]
