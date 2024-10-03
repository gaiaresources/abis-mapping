"""Provides Unit Tests for the `abis_mapping.plugins.default_lookup` module"""

# Third-party
import frictionless

# Local
from abis_mapping import plugins


def test_default_lookup() -> None:
    """Tests that the default lookup check plugin."""
    # Default map
    default_map = {
        "A": "B",
        "AA": "B",
    }

    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": "B", "c": "C"},
            {"a": "A", "b": None, "c": "C"},
            {"a": "AA", "b": None, "c": "C"},
            {"a": "AAA", "b": "B", "c": "C"},
            {"a": None, "b": "B", "c": "C"},
            # Invalid
            {"a": "AAA", "b": None, "c": "C"},
            {"a": None, "b": None, "c": "C"},
        ]
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.default_lookup.DefaultLookup(
                    key_field="a",
                    value_field="b",
                    default_map=default_map,
                )
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 2
