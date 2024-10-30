"""Provides Unit Tests for the `abis_mapping.plugins.mutual_inclusion` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_chained_inclusion() -> None:
    """Tests the ChainedInclusion Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": "B", "c": "C"},
            {"a": "A", "b": "B", "c": None},
            {"a": None, "b": "B", "c": "C"},
            {"a": None, "b": "B", "c": None},
            {"a": None, "b": None, "c": "C"},
            # Invalid
            {"a": "A", "b": None, "c": None},
            {"a": "A", "b": None, "c": "C"},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.chained_inclusion.ChainedInclusion(
                    field_names=["a", "b"],
                ),
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 2
