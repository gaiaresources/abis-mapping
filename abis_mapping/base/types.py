"""Provides Base Types for the Package"""


# Third-Party
import pandas._typing as pdt

# Typing
from typing import Union


# Constants
# See: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
CSVType = Union[
    pdt.FilePath,
    pdt.ReadCsvBuffer[bytes],
    pdt.ReadCsvBuffer[str],
]
