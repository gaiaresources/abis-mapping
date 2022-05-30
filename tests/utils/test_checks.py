"""Provides Unit Tests for the `abis_mapping.utils.checks` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import utils


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
        checks=[
            utils.checks.ValidCoordinates(
                latitude_name="lat",
                longitude_name="lon",
            ),
        ]
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1


def test_checks_not_empty() -> None:
    """Tests the NotEmpty Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=__file__,
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checks=[
            utils.checks.NotEmpty(),
        ]
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1


def test_checks_not_tabular() -> None:
    """Tests the NotTabular Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=__file__,
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checks=[
            utils.checks.NotTabular(),
        ]
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1
