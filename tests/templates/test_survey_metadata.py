"""Provides Unit Tests for the `survey_metadata.csv` Template"""


# Standard
import pathlib

# Local
import abis_mapping

TEMPLATE_ID = "survey_metadata.csv"


def test_temporal_coverage_date_ordering() -> None:
    """Tests that the temporal coverage start date must be before end date."""
    # Load data
    data = pathlib.Path(
        "abis_mapping/templates/survey_metadata/examples/minimal_error_chronological_order.csv"
    ).read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert not report.valid
    error_codes = [code for codes in report.flatten(['type']) for code in codes]
    assert "row-constraint" in error_codes
