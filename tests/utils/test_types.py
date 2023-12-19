"""Tests for types module."""

from abis_mapping.utils import types

def test_date_to_datetime() -> None:
    d = types.Date(2020, 1, 1)
    dt = d.to_datetime(round_up=True)

    assert dt.date() == d
