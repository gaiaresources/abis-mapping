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
        decimal.Decimal("-31.787767354279936"),
        decimal.Decimal("159.03680760268878"),
        decimal.Decimal("-31.486129946639664"),
        decimal.Decimal("159.28036851389584"),
    ),
    # Macquarie Island
    CoordinateRange(
        decimal.Decimal("-55.123198591741584"),
        decimal.Decimal("158.67492926247553"),
        decimal.Decimal("-54.35587401197603"),
        decimal.Decimal("158.998625266443"),
    ),
    # Norfolk Island
    CoordinateRange(
        decimal.Decimal("-28.994170999591915"),
        decimal.Decimal("167.9137700000855"),
        decimal.Decimal("-29.136568000312934"),
        decimal.Decimal("167.9980350000153"),
    ),
    # Ashmore and Cartier Islands
    CoordinateRange(
        decimal.Decimal("-12.547300808985085"),
        decimal.Decimal("122.92701027970077"),
        decimal.Decimal("-12.184700176471893"),
        decimal.Decimal("123.58185450628048"),
    ),
    # Christmas Island
    CoordinateRange(
        decimal.Decimal("-10.570559999744148"),
        decimal.Decimal("105.53314999957286"),
        decimal.Decimal("-10.412390000098355"),
        decimal.Decimal("105.7128100000815"),
    ),
    # Cocos Islands
    CoordinateRange(
        decimal.Decimal("-12.21100099090296"),
        decimal.Decimal("96.8154973639123"),
        decimal.Decimal("-11.822133252347669"),
        decimal.Decimal("96.93076388874255"),
    ),
    # Coral Sea Islands
    CoordinateRange(
        decimal.Decimal("-29.982747999620415"),
        decimal.Decimal("147.83945691360577"),
        decimal.Decimal("-15.721024000057525"),
        decimal.Decimal("159.1407290000434"),
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
