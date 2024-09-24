"""Provides Unit Tests for the `abis_mapping.plugins.mutual_exclusion` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_mutually_exclusive_valid() -> None:
    """Tests the MutuallyExclusive Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # valid: neither field provided
            {"C0": "R1", "C1": "", "C2": None},
            # valid: only one field provided
            {"C0": "R4", "C1": "", "C2": 1},
            {"C0": "R5", "C1": "", "C2": 0},
            {"C0": "R6", "C1": "A", "C2": None},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.mutual_exclusion.MutuallyExclusive(
                    field_names=["C1", "C2"],
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_checks_mutually_exclusive_not_valid() -> None:
    """Tests the MutuallyExclusive Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # not valid: both fields provided
            {"C0": "R1", "C1": "A", "C2": 1},
            {"C0": "R2", "C1": "A", "C2": 0},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.mutual_exclusion.MutuallyExclusive(
                    field_names=["C1", "C2"],
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks[0].errors) == 2
    for error in report.tasks[0].errors:
        assert error.type == 'row-constraint'
        assert error.note == (
            "The columns ['C1', 'C2'] are mutually exclusive and must not be "
            "provided together (columns ['C1', 'C2'] were provided together)"
        )
