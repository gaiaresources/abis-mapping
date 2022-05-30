"""Provides chunking utilities for the package"""


# Third-Party
import frictionless

# Typing
from typing import Optional


def should_chunk(
    row: frictionless.Row,
    rows: int,
    chunk_size: Optional[int] = None,
) -> bool:
    """Determines whether a mapper should chunk at this row.

    Args:
        row (frictionless.Row): The row that has just been mapped.
        rows (int): The total number of rows in the raw data.
        chunk_size (Optional[int]): The optional size to chunk at.

    Returns:
        bool: Whether chunking should occur.
    """
    # Normalize Chunk Size
    if (chunk_size is None) or (chunk_size < 1) or (chunk_size > rows):
        # If `chunk_size` is not provided, an integer less than one is provided
        # or an integer greater than the total number of rows is provided, then
        # the behaviour is to "not chunk", or more accurately just provide a
        # single chunk. As such, set the chunk size to the total number of rows
        # so that the chunking will only occur on the final row.
        chunk_size = rows

    # Check and Return
    return (  # type: ignore[no-any-return]
        row.row_number % chunk_size == 0  # Check if chunk-boundary reached
        or row.row_number == rows  # Must always chunk at the last row
    )
