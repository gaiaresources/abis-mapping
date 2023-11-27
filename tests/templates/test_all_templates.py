"""Provided unit tests across all templates."""

# Local
import abis_mapping
import abis_mapping.base
import tests.conftest

# Standard
import dataclasses
import pathlib

# Third-party
import pytest
import frictionless

# Typing
from typing import Type, Optional


@dataclasses.dataclass
class TemplateTestParameters:
    """Provides data object containing required testing parameters per template.

    Attributes:
        template_id (str): ID of the template
        data (pathlib.Path): Path relating t
    """
    template_id: str
    empty_template: pathlib.Path
    data: pathlib.Path
    expected: pathlib.Path
    extra_cols_data: pathlib.Path
    extra_cols_expected: pathlib.Path
    metadata_sampling_type: str
    organism_qty_data: Optional[pathlib.Path] = None
    organism_qty_expected: Optional[pathlib.Path] = None


test_cases: list[TemplateTestParameters] = [
    TemplateTestParameters(
        template_id="survey_occurrence_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data/survey_occurrence_data.csv"
        ),
        data=pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv"
        ),
        expected=pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data/examples/margaret_river_flora/margaret_river_flora.ttl"
        ),
        extra_cols_data=pathlib.Path(
            ("abis_mapping/templates/survey_occurrence_data/examples"
             "/margaret_river_flora/margaret_river_flora_extra_cols.csv"),
        ),
        extra_cols_expected=pathlib.Path(
            ("abis_mapping/templates/survey_occurrence_data/examples"
             "/margaret_river_flora/margaret_river_flora_extra_cols.ttl"),
        ),
        metadata_sampling_type="systematic survey",
        organism_qty_data=pathlib.Path(
            "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.csv",
        ),
        organism_qty_expected=pathlib.Path(
             "abis_mapping/templates/survey_occurrence_data/examples/organism_qty.ttl",
        )
    ),
    TemplateTestParameters(
        template_id="survey_site_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_site_data/survey_site_data.csv",
        ),
        data=pathlib.Path(
            "abis_mapping/templates/survey_site_data/examples/minimal.csv"
        ),
        expected=pathlib.Path(
            "abis_mapping/templates/survey_site_data/examples/minimal.ttl"
        ),
        extra_cols_data=pathlib.Path(
            "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols.csv"
        ),
        extra_cols_expected=pathlib.Path(
            "abis_mapping/templates/survey_site_data/examples/minimal_extra_cols.ttl"
        ),
        metadata_sampling_type="systematic survey"
    ),
    TemplateTestParameters(
        template_id="survey_metadata.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/survey_metadata/survey_metadata.csv"
        ),
        data=pathlib.Path(
            "abis_mapping/templates/survey_metadata/examples/minimal.csv"
        ),
        expected=pathlib.Path(
            "abis_mapping/templates/survey_metadata/examples/minimal.ttl"
        ),
        extra_cols_data=pathlib.Path(
            "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.csv"
        ),
        extra_cols_expected=pathlib.Path(
            "abis_mapping/templates/survey_metadata/examples/minimal_extra_cols.ttl"
        ),
        metadata_sampling_type="systematic survey"
    ),
    TemplateTestParameters(
        template_id="incidental_occurrence_data.csv",
        empty_template=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_data/incidental_occurrence_data.csv"
        ),
        data=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv"
        ),
        expected=pathlib.Path(
            "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.ttl"
        ),
        extra_cols_data=pathlib.Path(
            ("abis_mapping/templates/incidental_occurrence_data/examples"
             "/margaret_river_flora/margaret_river_flora_extra_cols.csv")
        ),
        extra_cols_expected=pathlib.Path(
            ("abis_mapping/templates/incidental_occurrence_data/examples"
             "/margaret_river_flora/margaret_river_flora_extra_cols.ttl")
        ),
        metadata_sampling_type="incidental"
    ),
]


@pytest.mark.parametrize(
    argnames="test_params",
    argvalues=[tc for tc in test_cases],
    ids=[tc.template_id for tc in test_cases]
)
class TestTemplateBasicSuite:
    @pytest.fixture(scope="class")
    def mappers(self) -> dict[str, Type[abis_mapping.base.mapper.ABISMapper]]:
        """Test fixture that retrieves all mappers"""
        return abis_mapping.get_mappers()

    def test_template_registered(
        self,
        mappers: dict[str, abis_mapping.base.mapper.ABISMapper],
        test_params: TemplateTestParameters
    ) -> None:
        """Tests that the supplied template id is registered."""
        assert test_params.template_id in mappers

    def test_validation(self, test_params: TemplateTestParameters) -> None:
        """Tests the validation for the template"""
        # Load Data
        data = test_params.data.read_bytes()

        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Validate
        report = mapper().apply_validation(data)
        assert report.valid

    def test_metadata_sampling_type(self, test_params: TemplateTestParameters) -> None:
        """Tests the metadata sampling type set correctly"""
        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get metadata
        metadata = mapper().metadata()

        # Confirm field set correctly
        assert metadata.get("sampling_type") == test_params.metadata_sampling_type

    def test_schema_is_valid(self, test_params: TemplateTestParameters) -> None:
        """Tests that the schema.json is a valid frictionless schema."""
        # Get Mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Get schema dictionary
        descriptor = mapper().schema()

        # Generate report
        report = frictionless.Schema.validate_descriptor(descriptor)

        # Assert valid
        assert report.valid

    def test_validation_empty_template(self, test_params: TemplateTestParameters) -> None:
        """Tests validation fails for empty template."""
        # Load data
        data = test_params.empty_template.read_bytes()

        # Get mapper
        mapper = abis_mapping.get_mapper(test_params.template_id)
        assert mapper

        # Validate
        report = mapper().apply_validation(data)
        assert not report.valid
        error_codes = [code for codes in report.flatten(['type']) for code in codes]
        assert "table-dimensions" in error_codes



def mapping_test_args() -> dict[str, tuple[str, pathlib.Path, pathlib.Path]]:
    """Constructs parameter sets necessary to perform mapping tests."""
    d1 = {tc.template_id: (tc.template_id, tc.data, tc.expected) for tc in test_cases}
    d2 = {
        f"{tc.template_id}-extra_cols": (tc.template_id, tc.extra_cols_data, tc.extra_cols_expected)
        for tc in test_cases
    }
    d3 = {
        f"{tc.template_id}-organism_qty": (tc.template_id, tc.organism_qty_data, tc.organism_qty_expected)
        for tc in test_cases if tc.organism_qty_data is not None
    }
    return {**d1, **d2, **d3}


@pytest.mark.parametrize(
    argnames="template_id,data_path,expected_path",
    argvalues=mapping_test_args().values(),
    ids=mapping_test_args().keys(),
)
def test_mapping(template_id: str, data_path: pathlib.Path, expected_path: pathlib.Path) -> None:
    """Tests the mapping for the template"""
    # Load Data and Expected Output
    data = data_path.read_bytes()
    expected = expected_path.read_text()

    # Get Mapper
    mapper = abis_mapping.get_mapper(template_id)
    assert mapper

    # Map
    graphs = list(mapper().apply_mapping(data))

    # Assert
    assert len(graphs) == 1

    # Compare Graphs
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
