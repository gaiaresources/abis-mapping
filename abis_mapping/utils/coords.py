"""Provides coordinate utilities for the package"""


# Standard
import dataclasses
import decimal


# Define Simple Data Class for Coordinate Ranges
@dataclasses.dataclass
class CoordinateRange:
    """Simple Data Container for Coordinate Range"""
    min_lat: decimal.Decimal
    min_lon: decimal.Decimal
    max_lat: decimal.Decimal
    max_lon: decimal.Decimal


# List of Valid Coordinate Ranges
VALID_COORDINATE_RANGES: list[CoordinateRange] = [
    # Australian Mainland
    CoordinateRange(
        decimal.Decimal("-43.644444"),
        decimal.Decimal("113.155000"),
        decimal.Decimal("-10.689167"),
        decimal.Decimal("153.637222"),
    ),
    # Heard and McDonalds Island
    CoordinateRange(
        decimal.Decimal("-53.195018"),
        decimal.Decimal("72.577376"),
        decimal.Decimal("-52.902770"),
        decimal.Decimal("73.872715"),
    ),
    # Lord Howe Island
    CoordinateRange(
        decimal.Decimal("-31.787767"),
        decimal.Decimal("159.036807"),
        decimal.Decimal("-31.486129"),
        decimal.Decimal("159.280368"),
    ),
    # Macquarie Island
    CoordinateRange(
        decimal.Decimal("-55.123198"),
        decimal.Decimal("158.674929"),
        decimal.Decimal("-54.355874"),
        decimal.Decimal("158.998625"),
    ),
    # Norfolk Island
    CoordinateRange(
        decimal.Decimal("-28.994170"),
        decimal.Decimal("167.913770"),
        decimal.Decimal("-29.136568"),
        decimal.Decimal("167.998035"),
    ),
    # Ashmore and Cartier Islands
    CoordinateRange(
        decimal.Decimal("-12.547300"),
        decimal.Decimal("122.927010"),
        decimal.Decimal("-12.184700"),
        decimal.Decimal("123.581854"),
    ),
    # Christmas Island
    CoordinateRange(
        decimal.Decimal("-10.570559"),
        decimal.Decimal("105.533149"),
        decimal.Decimal("-10.412390"),
        decimal.Decimal("105.712810"),
    ),
    # Cocos Islands
    CoordinateRange(
        decimal.Decimal("-12.211000"),
        decimal.Decimal("96.815497"),
        decimal.Decimal("-11.822133"),
        decimal.Decimal("96.930763"),
    ),
    # Coral Sea Islands
    CoordinateRange(
        decimal.Decimal("-29.982747"),
        decimal.Decimal("147.839456"),
        decimal.Decimal("-15.721024"),
        decimal.Decimal("159.140729"),
    ),
    # Australian Antarctic Territory
    # TODO -> TBC (BDR-397)
]


def validate_coordinates(
    latitude: decimal.Decimal,
    longitude: decimal.Decimal,
) -> bool:
    """Validates a given latitude and longitude within Australia

    Args:
        latitude (decimal.Decimal): Latitude to check
        longitude (decimal.Decimal): Longitude to check

    Returns:
        bool: Whether the latitude and longitude are considered valid
    """
    # Loop through valid coordinate boundaries
    for r in VALID_COORDINATE_RANGES:
        # Check whether the specified coordinates fall within this boundary
        if (r.min_lat <= latitude <= r.max_lat) and (r.min_lon <= longitude <= r.max_lon):
            # The coordinates fall within this boundary, they must be valid
            return True

    # The specified coordinates did not fall within any of the boundaries
    # This means they must be invalid
    return False
