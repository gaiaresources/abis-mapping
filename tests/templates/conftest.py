"""Setup for all template tests."""

# Standard
import dataclasses
import pathlib

# Typing
from typing import Optional


@dataclasses.dataclass
class MappingParameters:
    """Provides data object containing required parameters for a mapping test.

    Attributes:
        data (pathlib.Path): Path of CSV input data to use.
        expected (pathlib.Path): Path of the expected turtle output.
        scenario_name (Optional[str]): Optional string to be used to easily identify
            test scenario in output.
    """
    data: pathlib.Path
    expected: pathlib.Path
    scenario_name: Optional[str] = None


@dataclasses.dataclass
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
                data=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.csv",
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.ttl",
                )
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
