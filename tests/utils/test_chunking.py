"""Provides Unit Tests for the `abis_mapping.utils.chunking` module"""


# Third-Party
import pytest

# Local
from abis_mapping import utils

# Typing
from typing import Optional


@pytest.mark.parametrize(
    [
        "rows",
        "row_number",
        "chunk_size",
        "result",
    ],
    [
        # Regular Usage
        (100, 1, 7, False),
        (100, 7, 7, True),
        (100, 14, 7, True),
        (100, 99, 7, False),
        (100, 100, 7, True),
        # Edge Cases (Chunk Size: 1, None, 0, -1, 999)
        (100, 1, 1, True),
        (100, 2, 1, True),
        (100, 3, 1, True),
        (100, 1, None, False),
        (100, 100, None, True),
        (100, 1, 0, False),
        (100, 100, 0, True),
        (100, 1, -1, False),
        (100, 100, -1, True),
        (100, 1, 999, False),
        (100, 100, 999, True),
    ]
)
def test_chunking_should_chunk(
    rows: int,
    row_number: int,
    chunk_size: Optional[int],
    result: bool,
) -> None:
    """Tests the `should_chunk()` Utility Function.

    Args:
        rows (int): Total number of rows in the "resource" to test
        row_number (int): Row number to test
        chunk_size (Optional[int]): Chunk size to test
        result (bool): Expected result of whether to perform a chunk
    """
    # Test `should_chunk()`
    assert utils.chunking.should_chunk(
        row_number=row_number,
        n_rows=rows,
        chunk_size=chunk_size,
    ) is result
