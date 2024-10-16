"""Provides Unit Tests for the `abis_mapping.plugins.mutual_inclusion` module"""

# Third-Party
import frictionless
import pytest

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
        checklist=frictionless.Checklist(
            checks=[
                plugins.mutual_inclusion.MutuallyInclusive(
                    field_names=["a", "b"],
                ),
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 4


@pytest.mark.parametrize(
    "fk_set,n_err",
    [
        ({"d": {"D", "DD", "DDD"}}, 0),
        ({"e": {"E"}, "d": {"D"}}, 0),
        ({"e": {"D"}, "d": {"E"}}, 7),
    ],
)
def test_check_mutual_inclusion_with_whitelists(fk_set: dict[str, set[str]], n_err: int) -> None:
    """Tests the mutual inclusion checker with whitelists provided."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            {"a": "A", "b": None, "c": None, "d": "D", "e": "E"},
            {"a": None, "b": "B", "c": None, "d": "D", "e": "E"},
            {"a": None, "b": None, "c": "C", "d": "D", "e": "E"},
            {"a": "A", "b": "B", "c": None, "d": "D", "e": "E"},
            {"a": "A", "b": None, "c": "C", "d": "D", "e": "E"},
            {"a": None, "b": "B", "c": "C", "d": "D", "e": "E"},
            {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E"},
            {"a": None, "b": None, "c": None, "d": "D", "e": "E"},
        ]
    )

    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.mutual_inclusion.MutuallyInclusive(
                    field_names=["a", "b", "c", "d"],
                    whitelists=fk_set,
                )
            ]
        )
    )

    # Check
    assert report.valid == (n_err == 0)
    assert len(report.flatten()) == n_err
