"""Provides all relevant validation tests."""

# Local
from tests.templates import conftest
import abis_mapping

# Third-party
import pytest


@pytest.mark.parametrize(
    argnames="template_id,test_params",
    argvalues=[(id_, params) for (_, id_, params) in conftest.mapping_test_args()],
    ids=[id_ for (id_, _, params) in conftest.mapping_test_args()],
)
def test_apply_validation(template_id: str, test_params: conftest.MappingParameters) -> None:
    """Tests the validation for the template"""
    # Get Mapper
    mapper = abis_mapping.get_mapper(template_id)
    assert mapper

    # Load Data
    with open(test_params.data, "rb") as data:
        # Validate
        report = mapper().apply_validation(data)

    # Assert validation result
    assert report.valid == test_params.should_validate
    # Validate errors if invalid expected (and supplied).
    if not report.valid:
        error_codes = [code for codes in report.flatten(["type"]) for code in codes]
        for code in test_params.expected_error_codes:
            assert code in error_codes
