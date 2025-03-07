"""Provides Unit Tests for the `abis_mapping.plugins.default_lookup` module"""

# Third-party
import frictionless

# Local
from abis_mapping import plugins


def test_default_lookup() -> None:
    """Tests that the default lookup check plugin."""
    # Default map
    default_map: dict[object, str] = {
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
                    no_key_error_template="",
                    no_default_error_template="",
                )
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 2


def test_default_lookup_with_callable_key_valid() -> None:
    """Tests that the default lookup check plugin with a callable key."""
    # Default map
    default_map: dict[object, str] = {
        "A1": "10",
        "B2": "20",
    }

    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"value": None, "letter": "A", "number": "1"},
            {"value": None, "letter": "B", "number": "2"},
        ]
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.default_lookup.DefaultLookup(
                    value_field="value",
                    key_field=lambda row: row["letter"] + str(row["number"]),
                    default_map=default_map,
                    no_key_error_template="",
                    no_default_error_template="",
                )
            ]
        )
    )

    # Check
    assert report.valid


def test_default_lookup_with_callable_key_invalid() -> None:
    """Tests that the default lookup check plugin with a callable key, and invalid data."""
    # Default map
    default_map: dict[object, str] = {
        "AA": "10",
    }

    # Construct fake resource
    resource = frictionless.Resource(
        source=[
            # Invalid
            {"id": "1", "value": None, "letter": None},
            {"id": "2", "value": None, "letter": "B"},
        ]
    )

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.default_lookup.DefaultLookup(
                    value_field="value",
                    key_field=lambda row: (letter + letter) if (letter := row["letter"]) else None,
                    default_map=default_map,
                    no_key_error_template="No key found",
                    no_default_error_template="No default found for {key_value}",
                )
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 2
    assert report.tasks[0].errors[0].message == "The row at position 2 has an error: No key found"
    assert report.tasks[0].errors[1].message == "The row at position 3 has an error: No default found for BB"
