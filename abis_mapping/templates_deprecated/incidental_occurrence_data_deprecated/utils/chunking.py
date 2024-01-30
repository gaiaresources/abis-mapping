"""Provides chunking utilities for the package"""


# Typing
from typing import Optional


def should_chunk(
    row_number: int,
    n_rows: int,
    chunk_size: Optional[int] = None,
) -> bool:
    """Determines whether a mapper should chunk at this row.

    Args:
        row_number (int): The number of the row that has just been mapped (starts at 1).
        n_rows (int): The total number of rows in the raw data.
        chunk_size (Optional[int]): The optional size to chunk at.

    Returns:
        bool: Whether chunking should occur.

    Raises:
        ValueError: If row_number is not a positive integer
    """
    # Check valid input
    if row_number <= 0:
        raise ValueError(f"row_number should be positive non-zero integer; got {row_number}")

    # Normalize Chunk Size
    if (chunk_size is None) or (chunk_size < 1) or (chunk_size > n_rows):
        # If `chunk_size` is not provided, an integer less than one is provided
        # or an integer greater than the total number of rows is provided, then
        # the behaviour is to "not chunk", or more accurately just provide a
        # single chunk. As such, set the chunk size to the total number of rows
        # so that the chunking will only occur on the final row.
        chunk_size = n_rows

    # Check and Return
    return (
            row_number % chunk_size == 0  # Check if chunk-boundary reached
            or row_number == n_rows  # Must always chunk at the last row
    )
