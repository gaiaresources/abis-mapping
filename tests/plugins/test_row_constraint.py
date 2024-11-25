"""Provides tests for the custom row_constraint checks."""

# Third-party
import frictionless
import frictionless.checks

# Local
from abis_mapping import plugins


def test_validate_row_constraint_side_input() -> None:
    """Tests the RowConstraintSideInput check."""
    source = [
        ["row", "salary", "bonus"],
        [2, 1100, 200],
        [3, 2600, 500],
        [4, 1300, 500],
        [5, 5100, 1000],
        [6],
    ]
    resource = frictionless.Resource(source=source)
    checklist = frictionless.Checklist(
        checks=[
            plugins.row_constraint.RowConstraintSideInput(
                formula="salary == bonus * 5 + superannuation",
                side_inputs={"superannuation": 100},
            )
        ]
    )
    report = resource.validate(checklist)
    assert report.flatten(["rowNumber", "fieldNumber", "type"]) == [
        [4, None, "row-constraint"],
        [6, 2, "missing-cell"],
        [6, 3, "missing-cell"],
        [6, None, "row-constraint"],
    ]


def test_validate_row_constraint_list_in_formula_issue_817() -> None:
    source = [["val"], ["one"], ["two"]]
    resource = frictionless.Resource(source=source)
    checklist = frictionless.Checklist(
        checks=[
            frictionless.checks.duplicate_row(),
            plugins.row_constraint.RowConstraintSideInput(
                formula="val in ['one', 'two']",
                side_inputs={"val2": ["one"]},
            ),
        ],
    )
    report = resource.validate(checklist)
    assert report.valid


def test_validate_row_constraint_side_input_name_clash() -> None:
    source = [["val"], [5], [6]]
    resource = frictionless.Resource(source=source)
    checklist = frictionless.Checklist(
        checks=[
            frictionless.checks.duplicate_row(),
            plugins.row_constraint.RowConstraintSideInput(
                formula="val == 5 or val == 6",
                side_inputs={"val": 6},
            ),
        ],
    )
    report = resource.validate(checklist)
    assert report.flatten(["type"]) == [["side-input"]]
