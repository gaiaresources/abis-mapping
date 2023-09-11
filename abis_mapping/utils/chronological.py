"""Provides chronological utilities for the package"""

# Standard
import datetime


def is_chronologically_ordered(dts: list[datetime.datetime]) -> bool:
    """Tests the chronological ordering of a given list of datetimes

    Args:
        dts list[datetime.datetime]: Datetimes to be checked

    Returns:
        True if all datetimes in the given list are monotonically increasing else False
        It returns True for empty or single value list.
    """
    # Test for 0 - 1 length list
    if len(dts) < 2:
        return True  # If there are 0 or 1 datetimes, they are considered chronological

    # Iterate through the values and determine if each greater than the previous
    for i in range(len(dts) - 1):
        if dts[i] > dts[i + 1]:
            return False

    return True
