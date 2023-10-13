"""Provides Unit Tests for the `abis_mapping.plugins.coordinates` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_valid_coordinates() -> None:
    """Tests the ValidCoordinates Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # Missing
            {"name": "A", "lat": None,       "lon": None},
            {"name": "B", "lat": -31.953512, "lon": None},
            {"name": "C", "lat": None,       "lon": 115.857048},

            # Valid
            {"name": "D", "lat": -31.953512, "lon": 115.857048},

            # Invalid
            {"name": "E", "lat": 100.0,      "lon": 100.0},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.coordinates.ValidCoordinates(
                    latitude_name="lat",
                    longitude_name="lon",
                ),
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1
