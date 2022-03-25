"""Provides Base Types for the Package"""


# Typing
from os import PathLike
from typing import IO, Union


# Define Filepath and IO Types
FilePath = Union[str, PathLike[str]]
ReadCsvBuffer = IO
CSVType = Union[
    FilePath,
    ReadCsvBuffer[bytes],
    ReadCsvBuffer[str],
]
