"""Provides Unit Tests for the `abis_mapping.utils.coords` module"""


# Local
from abis_mapping import utils


def test_coords_validate_coordinates() -> None:
    """Tests the validate_coordinates() Function"""
    # Check Coordinates
    assert utils.coords.validate_coordinates(-31.953512, 115.857048)  # type: ignore
    assert not utils.coords.validate_coordinates(31.953512, -115.857048)  # type: ignore
