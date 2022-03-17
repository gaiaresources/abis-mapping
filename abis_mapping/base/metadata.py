"""Provides Metadata Classes for the Package"""


# Standard
import dataclasses
import datetime


@dataclasses.dataclass
class DatasetMetadata:
    """Metadata for the Dataset"""
    name: str
    description: str
    issued: datetime.date
