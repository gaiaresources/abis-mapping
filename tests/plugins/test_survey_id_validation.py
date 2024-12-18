"""Provides Unit Tests for the `abis_mapping.plugins.survey_id_validation` module"""

# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_survey_id_validation_valid() -> None:
    """Tests the SurveyIDValidation Checker with valid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {"rowID": "1", "surveyID": "S1"},
            {"rowID": "2", "surveyID": "S2"},
            {"rowID": "3", "surveyID": None},
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.survey_id_validation.SurveyIDValidation(
                    valid_survey_ids={"S1", "S2", "S3"},
                ),
            ],
        ),
    )

    # Check
    assert report.valid


def test_survey_id_validation_invalid() -> None:
    """Tests the SurveyIDValidation Checker with invalid data"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=[
            {"rowID": "1", "surveyID": "S1"},
            {"rowID": "2", "surveyID": "NOT_A_SURVEY"},  # invalid
            {"rowID": "3", "surveyID": "S2"},
            {"rowID": "4", "surveyID": None},
            {"rowID": "5", "surveyID": "ALSO_NOT_A_SURVEY"},  # invalid
        ],
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.survey_id_validation.SurveyIDValidation(
                    valid_survey_ids={"S1", "S2", "S3"},
                ),
            ],
        ),
    )

    # Check
    assert not report.valid
    assert len(report.tasks) == 1
    assert len(report.tasks[0].errors) == 2
    assert report.tasks[0].errors[0].message == (
        'The cell "NOT_A_SURVEY" in row at position "3" and field '
        '"surveyID" at position "2" does not conform to a constraint: '
        "surveyID must match a surveyID in the survey_metadata template"
    )
    assert report.tasks[0].errors[1].message == (
        'The cell "ALSO_NOT_A_SURVEY" in row at position "6" and field '
        '"surveyID" at position "2" does not conform to a constraint: '
        "surveyID must match a surveyID in the survey_metadata template"
    )
