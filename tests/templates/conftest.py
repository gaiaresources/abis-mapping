"""Setup for all template tests."""

# Standard
import pathlib

# Third-party
import attrs

# Local
from abis_mapping import base

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
        expected_error_codes (set[str]): Set of frictionless error codes expected to
            to be returned for scenario.
        shacl (list[pathlib.Path]): Optional list of paths to shape graphs to perform validation
            against.
    """

    data: pathlib.Path
    expected: pathlib.Path | None
    scenario_name: Optional[str] = None
    should_validate: bool = True
    expected_error_codes: set[str] = set()
    shacl: list[pathlib.Path] = []


@attrs.define(kw_only=True)
class ChunkingParameters:
    """Provides data object containing required testing parameters per template for chunking.

    Attributes:
        data (pathlib.Path): Path of CSV input data.
        chunk_size (int): Number of rows to process from a data source before emitting a graph.
        yield_count (int): How many times the apply_mapping method will yield a graph.
    """

    data: pathlib.Path
    chunk_size: int
    yield_count: int


@attrs.define(kw_only=True)
class TemplateTestParameters:
    """Provides data object containing required testing parameters per template.

    Attributes:
        template_id (str): ID of the template
        mapping_cases (list[MappingParameters]): Parameters to be used in template mapping tests.
        empty_template (pathlib.Path): Path of empty template.
        metadata_sampling_type (str): The expected sampling type value expected for the template
            metadata.
        allows_extra_cols (bool): Whether the template allows for extra cols not specified in the
            schema.
    """

    template_id: str
    mapping_cases: list[MappingParameters]
    empty_template: pathlib.Path
    metadata_sampling_type: str
    allows_extra_cols: bool
    chunking_parameters: list[ChunkingParameters] = []


TEST_CASES_ALL: list[TemplateTestParameters] = [
    # Survey templates v3
    TemplateTestParameters(
        template_id="survey_metadata-v3.0.0.csv",
        empty_template=pathlib.Path("abis_mapping/templates/survey_metadata_v3/survey_metadata.csv"),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path("abis_mapping/templates/survey_metadata_v3/examples/minimal.csv"),
                expected=pathlib.Path("abis_mapping/templates/survey_metadata_v3/examples/minimal.ttl"),
            ),
            MappingParameters(
                scenario_name="invalid_chrono_order",
                should_validate=False,
                expected_error_codes={"row-constraint"},
                data=pathlib.Path(
                    "abis_mapping/templates/survey_metadata_v3/examples/minimal_error_chronological_order.csv"
                ),
                expected=None,
            ),
            MappingParameters(
                scenario_name="mutually-inclusive-field-missing",
                should_validate=False,
                expected_error_codes={"row-constraint"},
                data=pathlib.Path("abis_mapping/templates/survey_metadata_v3/examples/minimal_error_missing_datum.csv"),
                expected=None,
            ),
        ],
        metadata_sampling_type="systematic survey",
        allows_extra_cols=True,
    ),
    TemplateTestParameters(
        template_id="survey_occurrence_data-v3.0.0.csv",
        empty_template=pathlib.Path("abis_mapping/templates/survey_occurrence_data_v3/survey_occurrence_data.csv"),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    (
                        "abis_mapping/templates/survey_occurrence_data_v3/examples"
                        "/margaret_river_flora/margaret_river_flora.csv"
                    )
                ),
                expected=pathlib.Path(
                    (
                        "abis_mapping/templates/survey_occurrence_data_v3/examples"
                        "/margaret_river_flora/margaret_river_flora.ttl"
                    )
                ),
                shacl=[
                    pathlib.Path("abis_mapping/base/validators/shapes.ttl"),
                    pathlib.Path("abis_mapping/templates/survey_occurrence_data_v3/validators/validator.ttl"),
                ],
            ),
            MappingParameters(
                scenario_name="organism_qty",
                should_validate=True,
                data=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data_v3/examples/organism_qty.csv",
                ),
                expected=pathlib.Path(
                    "abis_mapping/templates/survey_occurrence_data_v3/examples/organism_qty.ttl",
                ),
            ),
        ],
        metadata_sampling_type="systematic survey",
        allows_extra_cols=True,
        chunking_parameters=[
            ChunkingParameters(
                data=pathlib.Path(
                    (
                        "abis_mapping/templates/survey_occurrence_data_v3/examples/"
                        "margaret_river_flora/margaret_river_flora.csv"
                    )
                ),
                chunk_size=7,
                yield_count=3,
            ),
        ],
    ),
    TemplateTestParameters(
        template_id="survey_site_data-v3.0.0.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_site_data_v3/survey_site_data.csv",
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path("abis_mapping/templates/survey_site_data_v3/examples/minimal.csv"),
                expected=pathlib.Path("abis_mapping/templates/survey_site_data_v3/examples/minimal.ttl"),
            ),
            MappingParameters(
                scenario_name="missing_relatedSiteID_and_datum",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_data_v3/examples/minimal-error-missing-fields.csv"
                ),
                expected=None,
                should_validate=False,
                expected_error_codes={"row-constraint"},
            ),
            MappingParameters(
                scenario_name="duplicate-site-ids",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_data_v3/examples/minimal-error-duplicate-site-ids.csv"
                ),
                expected=None,
                should_validate=False,
                expected_error_codes={"unique-together"},
            ),
        ],
        metadata_sampling_type="systematic survey",
        allows_extra_cols=True,
    ),
    TemplateTestParameters(
        template_id="survey_site_visit_data-v3.0.0.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_site_visit_data_v3/survey_site_visit_data.csv",
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path("abis_mapping/templates/survey_site_visit_data_v3/examples/minimal.csv"),
                expected=pathlib.Path("abis_mapping/templates/survey_site_visit_data_v3/examples/minimal.ttl"),
            ),
            MappingParameters(
                scenario_name="missing_start_date",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_visit_data_v3/examples/minimal-error-no-dates.csv"
                ),
                expected=None,
                should_validate=False,
                expected_error_codes={"constraint-error"},
            ),
            MappingParameters(
                scenario_name="dates_in_wrong_order",
                data=pathlib.Path(
                    "abis_mapping/templates/survey_site_visit_data_v3/examples/minimal-error-dates-wrong-order.csv"
                ),
                expected=None,
                should_validate=False,
                expected_error_codes={"row-constraint"},
            ),
        ],
        metadata_sampling_type="systematic survey",
        allows_extra_cols=True,
    ),
    # Incidental templates
    TemplateTestParameters(
        template_id="incidental_occurrence_data-v3.0.0.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_data_v3/incidental_occurrence_data.csv"
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path(
                    (
                        "abis_mapping/templates/incidental_occurrence_data_v3/examples/"
                        "margaret_river_flora/margaret_river_flora.csv"
                    )
                ),
                expected=pathlib.Path(
                    (
                        "abis_mapping/templates/incidental_occurrence_data_v3/examples/"
                        "margaret_river_flora/margaret_river_flora.ttl"
                    )
                ),
                shacl=[
                    pathlib.Path("abis_mapping/base/validators/shapes.ttl"),
                    pathlib.Path("abis_mapping/templates/incidental_occurrence_data_v3/validators/validator.ttl"),
                ],
            ),
        ],
        metadata_sampling_type="incidental",
        allows_extra_cols=True,
        chunking_parameters=[
            ChunkingParameters(
                data=pathlib.Path(
                    (
                        "abis_mapping/templates/incidental_occurrence_data_v3/examples/"
                        "margaret_river_flora/margaret_river_flora.csv"
                    )
                ),
                chunk_size=7,
                yield_count=3,
            ),
        ],
    ),
    # Incidental Delete templates
    TemplateTestParameters(
        template_id="incidental_occurrence_delete-v1.0.0.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_delete_v1/incidental_occurrence_delete.csv"
        ),
        mapping_cases=[
            MappingParameters(
                data=pathlib.Path("abis_mapping/templates/incidental_occurrence_delete_v1/examples/example.csv"),
                expected=pathlib.Path("abis_mapping/templates/incidental_occurrence_delete_v1/examples/example.ttl"),
                shacl=[
                    pathlib.Path("abis_mapping/base/validators/shapes.ttl"),
                ],
            ),
        ],
        metadata_sampling_type="incidental",
        allows_extra_cols=False,
        chunking_parameters=[
            ChunkingParameters(
                data=pathlib.Path("abis_mapping/templates/incidental_occurrence_delete_v1/examples/example.csv"),
                chunk_size=2,
                yield_count=2,
            ),
        ],
    ),
]

# Filter out only those templates that are registered
TEST_CASES = [tc for tc in TEST_CASES_ALL if tc.template_id in base.mapper.registered_ids()]


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


def chunking_test_args() -> Iterable[tuple[str, str, ChunkingParameters]]:
    """Constructs parameter sets necessary to perform chunking tests.

    Yields:
        tuple[str, str, ChunkingParameters]: First term is the test id, the second the template id,
            and lastly the parameters of the mapping test scenario.
    """
    for test_case in TEST_CASES:
        for i, chunking_case in enumerate(test_case.chunking_parameters):
            name = f"{test_case.template_id}"
            name += f"-{i}"
            d = (name, test_case.template_id, chunking_case)
            yield d
