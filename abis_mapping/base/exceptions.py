"""Provides Base Exceptions for the Package"""


# Standard
import dataclasses

# Typing
from typing import Any


class ABISMapperError(Exception):
    """Base ABIS Mapper Exception"""


class ABISMapperMappingError(ABISMapperError):
    """ABIS Mapper Mapping Exception for Mapping Errors"""


@dataclasses.dataclass
class ABISMapperValidationError(ABISMapperError):
    """ABIS Mapper Validation Exception for Validation Errors"""
    report: dict[str, Any]  # Validation Report
