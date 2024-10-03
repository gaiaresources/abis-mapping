"""Provides Unit Tests for the `abis_mapping.plugins.logical_or` module"""

# Third-Party
import frictionless
import pytest

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


@pytest.mark.parametrize(
    "fk_set,n_err",
    [
        ({"d": {"D", "DD", "DDD"}}, 0),
        ({"e": {"E"}, "d": {"D"}}, 0),
        ({"e": {"D"}, "d": {"E"}}, 1),
    ],
)
def test_check_logical_or_with_foreign_keys(fk_set: dict[str, set[str]], n_err: int) -> None:
    """Tests the logical or checker with foreign keys provided."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": None, "c": None, "d": "D", "e": "E"},
            {"a": None, "b": "B", "c": None, "d": "D", "e": "E"},
            {"a": None, "b": None, "c": "C", "d": "D", "e": "E"},
            {"a": "A", "b": "B", "c": None, "d": "D", "e": "E"},
            {"a": "A", "b": None, "c": "C", "d": "D", "e": "E"},
            {"a": None, "b": "B", "c": "C", "d": "D", "e": "E"},
            {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E"},
            # Invalid
            {"a": None, "b": None, "c": None, "d": "D", "e": "E"},
        ]
    )

    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.logical_or.LogicalOr(
                    field_names=["a", "b", "c"],
                    foreign_keys=fk_set,
                )
            ]
        )
    )

    # Check
    assert report.valid == (n_err == 0)
    assert len(report.flatten()) == n_err
