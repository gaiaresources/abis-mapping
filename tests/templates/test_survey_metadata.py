# Third-party
import frictionless

# Standard
import pathlib

# Local
import abis_mapping
import tests.conftest

TEMPLATE_ID = "survey_metadata.csv"
DATA = pathlib.Path(
    "abis_mapping/templates/survey_metadata/examples/minimal.csv"
)
EXPECTED = pathlib.Path(
    "abis_mapping/templates/survey_metadata/examples/minimal.ttl"
)


def test_validation() -> None:
    """Tests the validation for the template."""
    # Load Data
    data = DATA.read_bytes()

    # Get Mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert report.valid


def test_validation_empty_template() -> None:
    """Tests validation fails for empty template."""
    # Load data
    data = pathlib.Path(
        "abis_mapping/templates/survey_metadata/examples/empty.csv"
    ).read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert not report.valid
    error_codes = [code for codes in report.flatten(['type']) for code in codes]
    assert "table-dimensions" in error_codes


def test_mapping() -> None:
    """Tests mapping for the template."""
    # Load data
    data = DATA.read_bytes()
    expected = EXPECTED.read_text()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Map
    graphs = list(mapper().apply_mapping(data))

    # Assert
    assert len(graphs) == 1

    # Compare graphs
    assert tests.conftest.compare_graphs(
        graph1=graphs[0],
        graph2=expected,
    )


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