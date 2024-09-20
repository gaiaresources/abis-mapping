"""Tests for specific for the `survey_occurrence_data` template."""

# Third-party
import pytest_mock

# Local
from abis_mapping import base
import abis_mapping.templates.survey_occurrence_data_v2.mapping


def test_extract_site_visit_id_keys(mocker: pytest_mock.MockerFixture) -> None:
    """Test the extract_site_visit_id_keys method.

    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture.
    """
    # Get the specific mapper
    mapper = abis_mapping.templates.survey_occurrence_data_v2.mapping.SurveyOccurrenceMapper()

    # Modify schema to only include the necessary fields
    descriptor = {"fields": [
        {"name": "siteVisitID", "type": "string"}
    ]}
    mocker.patch.object(base.mapper.ABISMapper, "schema").return_value = descriptor

    # Create raw data csv string
    csv_data = b"\r\n".join([
        b"siteVisitID",
        b"S1",
        b"S2",
        b"",
        b"S3",
        b"S2",
        b"S1",
    ])

    expected = {
        "S1": True,
        "S2": True,
        "S3": True,
    }

    # Invoke method
    actual = mapper.extract_site_visit_id_keys(csv_data)

    # Validate
    assert actual == expected
