"""Provides Unit Tests for the `abis_mapping.plugins.logical_or` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_check_logical_or() -> None:
    """Tests the logical or checker."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": None, "c": None, "d": "D"},
            {"a": None, "b": "B", "c": None, "d": "D"},
            {"a": None, "b": None, "c": "C", "d": "D"},
            {"a": "A", "b": "B", "c": None, "d": "D"},
            {"a": "A", "b": None, "c": "C", "d": "D"},
            {"a": None, "b": "B", "c": "C", "d": "D"},
            {"a": "A", "b": "B", "c": "C", "d": "D"},

            # Invalid
            {"a": None, "b": None, "c": None, "d": "D"},
        ]
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.logical_or.LogicalOr(
                    field_names=["a", "b", "c"],
                )
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1
