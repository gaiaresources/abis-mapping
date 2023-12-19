"""Setup for all template tests."""

# Standard
import pathlib

# Third-party
import attrs

# Typing
from typing import Optional, Iterable


@attrs.define(kw_only=True)
class MappingParameters:
    """Provides data object containing required parameters for a mapping test.

    Attributes:
        data (pathlib.Path): Path of CSV input data to use.
        expected (pathlib.Path): Path of the expected turtle output.
        scenario_name (Optional[str]): Optional string to be used to easily identify
            test scenario in output. Default: None
        should_validate (bool): Indicates whether the data file provided should
            pass validation. Default: True
    """
    data: pathlib.Path
    expected: pathlib.Path | None
    scenario_name: Optional[str] = None
    should_validate: bool = True
    expected_error_codes: set[str] = set()


@attrs.define(kw_only=True)
class TemplateTestParameters:
    """Provides data object containing required testing parameters per template.

    Attributes:
        template_id (str): ID of the template
        mapping_cases (list[MappingParameters]): Parameters to be used in template mapping tests.
        empty_template (pathlib.Path): Path of empty template.
        metadata_sampling_type (str): The expected sampling type value expected for the template
            metadata.
    """
    template_id: str
    mapping_cases: list[MappingParameters]
    empty_template: pathlib.Path
    metadata_sampling_type: str


TEST_CASES: list[TemplateTestParameters] = [
    TemplateTestParameters(
        template_id="survey_occurrence_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data/survey_occurrence_data.csv"
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    ("abis_mapping/templates/survey_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora.csv")
                ),
                expected=pathlib.Path(
                    ("abis_mapping/templates/survey_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora.ttl")
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols",
                data=pathlib.Path(
                    ("abis_mapping/templates/survey_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora_extra_cols.csv"),
                ),
                expected=pathlib.Path(
                    ("abis_mapping/templates/survey_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora_extra_cols.ttl"),
                ),
            ),
            MappingParameters(
                scenario_name="organism_qty",
                should_validate=False,
                data=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.csv",
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.ttl",
                )
            ),
            MappingParameters(
                scenario_name="extra_cols_mid",
                should_validate=False,
                expected_error_codes={"incorrect-label"},
                data=pathlib.Path(
                    ("abis_mapping/templates/survey_occurrence_data/examples/"
                     "margaret_river_flora/margaret_river_flora_extra_cols_mid.csv"),
                ),
                expected=None,
            )
        ],
        metadata_sampling_type="systematic survey",
    ),
    TemplateTestParameters(
        template_id="survey_site_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_site_data/survey_site_data.csv",
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_data/examples/minimal.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_site_data/examples/minimal.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols_mid",
                should_validate=False,
                expected_error_codes={'incorrect-label'},
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols_mid.csv",
                ),
                expected=None,
            )
        ],
        metadata_sampling_type="systematic survey"
    ),
    TemplateTestParameters(
        template_id="survey_metadata.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_metadata/survey_metadata.csv"
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="yearmonth",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/yearmonth.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/yearmonth.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="year",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/year.csv"
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/year.ttl"
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols_mid",
                expected_error_codes={"incorrect-label"},
                should_validate=False,
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols_mid.csv",
                ),
                expected=None,
            ),
            MappingParameters(
                scenario_name="invalid_chrono_order",
                should_validate=False,
                expected_error_codes={'row-constraint'},
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata/examples/minimal_error_chronological_order.csv"
                ),
                expected=None,
            )
        ],
        metadata_sampling_type="systematic survey"
    ),
    TemplateTestParameters(
        template_id="incidental_occurrence_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_data/incidental_occurrence_data.csv"
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    ("abis_mapping/templates/incidental_occurrence_data/examples/"
                     "margaret_river_flora/margaret_river_flora.csv")
                ),
                expected=pathlib.Path(
                    ("abis_mapping/templates/incidental_occurrence_data/examples/"
                     "margaret_river_flora/margaret_river_flora.ttl")
                ),
            ),
            MappingParameters(
                scenario_name="extra_cols",
                data=pathlib.Path(
                    ("abis_mapping/templates/incidental_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora_extra_cols.csv")
                ),
                expected=pathlib.Path(
                    ("abis_mapping/templates/incidental_occurrence_data/examples"
                     "/margaret_river_flora/margaret_river_flora_extra_cols.ttl")
                ),
            )
        ],
        metadata_sampling_type="incidental"
    ),
]


def mapping_test_args() -> Iterable[tuple[str, str, MappingParameters]]:
    """Constructs parameter sets necessary to perform mapping tests.

    Yields:
        tuple[str, str, MappingParameters]: First term is the test id, the second the template id,
            and lastly the parameters of the mapping test scenario.
    """
    for test_case in TEST_CASES:
        for mapping_case in test_case.mapping_cases:
            name = f"{test_case.template_id}"
            name += f"-{mapping_case.scenario_name}" if mapping_case.scenario_name is not None else ""
            d = (name, test_case.template_id, mapping_case)
            yield d
