"""Provides Unit Tests for the `abis_mapping.plugins.lookup_match` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_vlookup_match() -> None:
    """Tests the VLookupMatch Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # Valid
            {"a": "A", "b": "B", "c": "C"},
            {"a": "A", "b": "B", "c": None},
            {"a": "A1", "b": "B1", "c": None},
            {"a": None, "b": "B", "c": "C"},
            {"a": None, "b": "B", "c": None},
            {"a": None, "b": None, "c": "C"},
            # Invalid
            {"a": "A", "b": None, "c": None},
            {"a": "A", "b": None, "c": "C"},
            {"a": "A1", "b": "B2", "c": "C"},
            {"a": "A", "b": "B1", "c": "C"},
            {"a": "A2", "b": "B", "c": "C"},
        ],
    )

    lookup_map: dict[object, str] = {"A": "B", "A1": "B1"}

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.lookup_match.VLookupMatch(
                    key_field="a",
                    value_field="b",
                    lu_map=lookup_map,
                ),
            ]
        )
    )

    # Check
    assert not report.valid
    row_numbers = report.flatten(["rowNumber"])
    assert len(row_numbers) == 5
    # Confirm that the rows in error are where we expect
    assert all([r[0] > 7 for r in row_numbers])
