"""Provides Unit Tests for the `survey_site_data.csv` Template"""


# Third-party
import frictionless

# Standard
import pathlib

# Local
import abis_mapping


TEMPLATE_ID = "survey_site_data.csv"
DATA = pathlib.Path(
    "abis_mapping/templates/survey_site_data/examples/minimal.csv"
)


def test_validation() -> None:
    """Tests the validation for the template."""
    # Load data
    data = DATA.read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert report.valid


def test_validation_empty_template() -> None:
    """Tests validation fails for empty template."""
    # Load data
    data = pathlib.Path(
        "abis_mapping/templates/survey_site_data/survey_site_data.csv"
    ).read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert not report.valid
    error_codes = [code for codes in report.flatten(['type']) for code in codes]
    assert "table-dimensions" in error_codes


def test_metadata_sampling_type() -> None:
    """Tests the metadata sampling type set correctly."""
    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Get metadata
    metadata = mapper().metadata()

    # Confirm field set correctly
    assert metadata.get("sampling_type") == "systematic survey"


def test_schema_is_valid() -> None:
    """Tests that the schema.json is a valid frictionless schema."""
    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Get schema dictionary
    descriptor = mapper().schema()

    # Generate report
    report = frictionless.Schema.validate_descriptor(descriptor)

    # Assert valid
    assert report.valid
