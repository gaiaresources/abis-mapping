"""Provides Unit Tests for the `abis_mapping.plugins.mutual_inclusion` module"""


# Third-Party
import frictionless
import pytest

# Local
from abis_mapping import plugins


@pytest.mark.parametrize(
    "use_or_behavior,n_invalid",
    [
        (False, 5),
        (True, 1)
    ]
)
def test_check_mutually_exclusive(use_or_behavior: bool, n_invalid: int) -> None:
    """Tests the mutual exclusion checker."""
    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Valid both
            {"a": "A", "b": None, "c": None, "d": "D"},
            {"a": None, "b": "B", "c": None, "d": "D"},
            {"a": None, "b": None, "c": "C", "d": "D"},

            # Invalid - not OR behavior
            {"a": "A", "b": "B", "c": None, "d": "D"},
            {"a": "A", "b": None, "c": "C", "d": "D"},
            {"a": None, "b": "B", "c": "C", "d": "D"},
            {"a": "A", "b": "B", "c": "C", "d": "D"},

            # Invalid both
            {"a": None, "b": None, "c": None, "d": "D"},
        ]
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.mutual_exclusion.MutuallyExclusive(
                    field_names=["a", "b", "c"],
                    use_or_behavior=use_or_behavior,
                )
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == n_invalid
