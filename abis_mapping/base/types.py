"""Provides Base Types for the Package"""

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
