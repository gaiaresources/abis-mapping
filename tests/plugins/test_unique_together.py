"""Provides Unit Tests for the `abis_mapping.plugins.unique_together` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_unique_together_valid_nulls_skipped() -> None:
    """Tests the UniqueTogether Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # unique rows
            {"rowID": "1", "ID": "A1", "source": "Z1"},
            {"rowID": "2", "ID": "A1", "source": "Z2"},
            {"rowID": "3", "ID": "A2", "source": "Z1"},
            {"rowID": "4", "ID": "A2", "source": "Z2"},
            # rows with None are skipped, can be duplicates
            {"rowID": "5", "ID": "A1", "source": None},
            {"rowID": "6", "ID": "A1", "source": None},
            {"rowID": "7", "ID": None, "source": "Z2"},
            {"rowID": "8", "ID": None, "source": "Z2"},
            {"rowID": "9", "ID": None, "source": None},
            {"rowID": "0", "ID": None, "source": None},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.unique_together.UniqueTogether(
                    fields=["ID", "source"],
                    null_handling="skip",
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_unique_together_valid_nulls_included() -> None:
    """Tests the UniqueTogether Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            # unique rows
            {"rowID": "1", "ID": "A1", "source": "Z1"},
            {"rowID": "2", "ID": "A1", "source": "Z2"},
            {"rowID": "3", "ID": "A2", "source": "Z1"},
            {"rowID": "4", "ID": "A2", "source": "Z2"},
            # rows with None are checked, can't be duplicates
            {"rowID": "5", "ID": "A1", "source": None},
            {"rowID": "6", "ID": None, "source": "Z2"},
            {"rowID": "7", "ID": None, "source": None},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.unique_together.UniqueTogether(
                    fields=["ID", "source"],
                    null_handling="include",
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_unique_together_invalid() -> None:
    """Tests the UniqueTogether Checker with invalid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {"rowID": "1", "ID": "A1", "source": "Z1"},
            {"rowID": "2", "ID": "A1", "source": "Z1"},  # invalid, copies row 1
            {"rowID": "3", "ID": "A1", "source": "Z2"},
            {"rowID": "4", "ID": "A1", "source": "Z2"},  # invalid, copies row 3
            {"rowID": "5", "ID": "A1", "source": "Z3"},
            {"rowID": "6", "ID": "A1", "source": "Z1"},  # invalid, copies row 1
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.unique_together.UniqueTogether(
                    fields=["ID", "source"],
                    null_handling="skip",
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 3
    assert report.tasks[0].errors[0].message == (
        'Row at position "3" violates the unique together constraint: '
        "The unique together fields [ID, source] contain the values [A1, Z1] "
        'that have already been used in the row at position "2"'
    )
    assert report.tasks[0].errors[1].message == (
        'Row at position "5" violates the unique together constraint: '
        "The unique together fields [ID, source] contain the values [A1, Z2] "
        'that have already been used in the row at position "4"'
    )
    assert report.tasks[0].errors[2].message == (
        'Row at position "7" violates the unique together constraint: '
        "The unique together fields [ID, source] contain the values [A1, Z1] "
        'that have already been used in the row at position "2"'
    )


def test_unique_together_invalid_nulls_included() -> None:
    """Tests the UniqueTogether Checker with invalid data including nulls"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {"rowID": "1", "ID": "A1", "source": None},
            {"rowID": "2", "ID": "A1", "source": None},  # invalid, copies row 1
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.unique_together.UniqueTogether(
                    fields=["ID", "source"],
                    null_handling="include",
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 1
    assert report.tasks[0].errors[0].message == (
        'Row at position "3" violates the unique together constraint: '
        "The unique together fields [ID, source] contain the values [A1, None] "
        'that have already been used in the row at position "2"'
    )


def test_unique_together_invalid_custom_template() -> None:
    """Tests the UniqueTogether Checker with invalid data and a custom error"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {"rowID": "1", "ID": "A1", "source": "Z1"},
            {"rowID": "2", "ID": "A1", "source": "Z1"},  # invalid, copies row 1
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.unique_together.UniqueTogether(
                    fields=["ID", "source"],
                    null_handling="skip",
                    error_message_template="FIELDS: {fields} VALUES: {values} ROW: {first_seen_row_number}",
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 1
    assert report.tasks[0].errors[0].message == (
        'Row at position "3" violates the unique together constraint: FIELDS: ID, source VALUES: A1, Z1 ROW: 2'
    )
