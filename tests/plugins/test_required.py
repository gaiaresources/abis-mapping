"""Provides Unit Tests for the `plugins.required` module"""

# Third-party
import frictionless
import pytest

# Local
from abis_mapping import plugins


def test_check_required_enhanced() -> None:
    """Tests the MutuallyInclusive Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": "B", "c": "C"},
            {"a": "A", "b": "B", "c": None},
            # Invalid
            {"a": None, "b": None, "c": "C"},
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
                plugins.required.RequiredEnhanced(
                    field_names=["a", "b"],
                ),
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 5


@pytest.mark.parametrize(
    "fk_set,n_err",
    [
        ({"d": {"D", "DD", "DDD"}}, 0),
        ({"e": {"E"}, "d": {"D"}}, 0),
        ({"e": {"D"}, "d": {"E"}}, 7),
    ],
)
def test_check_required_enhanced_with_whitelists(fk_set: dict[str, set[str]], n_err: int) -> None:
    """Tests the enhanced required checker with whitelists provided."""
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
                plugins.required.RequiredEnhanced(
                    field_names=["a", "b", "c"],
                    whitelists=fk_set,
                )
            ]
        )
    )

    # Check
    assert report.valid == (n_err == 0)
    assert len(report.flatten()) == n_err
    assert report.flatten(["type"]) == [["row-constraint"]] * n_err


def test_check_required_enhanced_with_invalid_whitelist() -> None:
    """Tests the enhanced required checker with an invalid whitelist."""
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
            checks=[plugins.required.RequiredEnhanced(field_names=["d", "e"], whitelists={"fake": {"FAKE"}})]
        )
    )

    assert not report.valid
    assert len(report.flatten()) == 1
    assert report.flatten(["type"]) == [["check-error"]]
