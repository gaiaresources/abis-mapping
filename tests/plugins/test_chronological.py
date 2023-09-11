"""Provides unit tests for the `abis_mapping.plugins.chronological` module"""


# Third-party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_valid_chronological_order() -> None:
    """Test the ChronologicalOrder checker"""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Missing
            {"name": "A", "start": "2022-09-11T15:15:15Z", "end": None},
            {"name": "B", "start": None, "end": "2022-09-11T15:15:15Z"},
            {"name": "C", "start": None, "end": None},

            # Valid
            {"name": "D", "start": "2022-09-11T15:15:15Z", "end": "2023-09-11T15:15:15Z"},

            # Invalid
            {"name": "E", "start": "2023-09-11T15:15:15Z", "end": "2022-09-11T15:15:15Z"},
        ],
    )

    # Validate
    report = resource.validate(
        checks=[
            plugins.chronological.ChronologicalOrder(
                field_names=["start", "end"]
            ),
        ]
    )

    # Assert
    assert not report.valid
    assert len(report.flatten()) == 1
