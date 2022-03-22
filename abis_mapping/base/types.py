"""Provides Base Types for the Package"""


# Typing
from os import PathLike
from typing import IO, Union


# Define Pandas Types
# pandas._typing cannot be resolved properly, so re-defining them here
FilePath = Union[str, PathLike[str]]
ReadCsvBuffer = IO

# Constants
# See: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# See: https://github.com/pandas-dev/pandas/blob/v1.4.1/pandas/io/parsers/readers.py#L597
CSVType = Union[
    FilePath,
    ReadCsvBuffer[bytes],
    ReadCsvBuffer[str],
]
