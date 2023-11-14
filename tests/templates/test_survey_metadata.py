"""Provides Unit Tests for the `survey_metadata.csv` Template"""


# Third-party
import frictionless
import pytest

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
        "abis_mapping/templates/survey_metadata/survey_metadata.csv"
    ).read_bytes()

    # Get mapper
    mapper = abis_mapping.get_mapper(TEMPLATE_ID)
    assert mapper

    # Validate
    report = mapper().apply_validation(data)
    assert not report.valid
    error_codes = [code for codes in report.flatten(['type']) for code in codes]
    assert "table-dimensions" in error_codes


@pytest.mark.parametrize(
    "data_path,expected_path",
    [
        ("abis_mapping/templates/survey_metadata/examples/minimal.csv",
         "abis_mapping/templates/survey_metadata/examples/minimal.ttl"),
        ("abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv",
         "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.ttl"),
    ]
)
def test_mapping(data_path: str, expected_path: str) -> None:
    """Tests mapping for the template."""
    # Load data
    data = pathlib.Path(data_path).read_bytes()
    expected = pathlib.Path(expected_path).read_text()

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

    # Check that there are no `None`s in the Graph
    # This check is important. As some fields are optional they can be `None`
    # at runtime. Unfortunately, `None` is valid in many contexts in Python,
    # including string formatting. This means that type-checking is unable to
    # determine whether a statement is valid in our specific context. As such,
    # we check here to see if any `None`s have snuck their way into the RDF.
    assert "None" not in graphs[0].serialize(format="ttl")


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
