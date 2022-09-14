"""Provides string utilities for the package"""


# Standard
import re


# Constants
REGEX_STRIP = re.compile(
    pattern=r"[\W_]+",
    flags=re.IGNORECASE | re.UNICODE,
)


def sanitise(value: str) -> str:
    """Capitalises and strips all non-alphanumeric characters from a string.

    Args:
        value (str): String to be stripped and capitalised

    Returns:
        str: The stripped and capitalised string
    """
    # Strip, Capitalise and Return
    return REGEX_STRIP.sub("", value.upper())
