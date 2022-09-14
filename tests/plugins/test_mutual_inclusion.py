"""Provides Unit Tests for the `abis_mapping.plugins.mutual_inclusion` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_mutually_inclusive() -> None:
    """Tests the MutuallyInclusive Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": "B", "c": "C"},
            {"a": "A", "b": "B", "c": None},
            {"a": None, "b": None, "c": "C"},

            # Invalid
            {"a": None, "b": "B", "c": "C"},
            {"a": None, "b": "B", "c": None},
            {"a": "A", "b": None, "c": "C"},
            {"a": "A", "b": None, "c": None},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checks=[
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["a", "b"],
            ),
        ]
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 4
