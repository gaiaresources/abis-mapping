"""Provides Base Exceptions for the Package"""


# Standard
import dataclasses

# Third-Party
import frictionless


class ABISMapperError(Exception):
    """Base ABIS Mapper Exception"""


class ABISMapperMappingError(ABISMapperError):
    """ABIS Mapper Mapping Exception for Mapping Errors"""


@dataclasses.dataclass
class ABISMapperValidationError(ABISMapperError):
    """ABIS Mapper Validation Exception for Validation Errors"""
    report: frictionless.Report  # Validation Report
