"""Provides string utilities for the package"""


# Standard
import re

# Third-party
import rdflib


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
    return REGEX_STRIP.sub("", value).upper()

def is_uri(value: str) -> bool:
    """Check to see if a string is a valid uri.

    Args:
        value (str): String to be tested.

    Returns:
        bool: True if valid uri else false
    """
    # Catch exception
    try:
        rdflib.URIRef(value)
        return True
    except:
        return False
