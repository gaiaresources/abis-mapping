import pathlib

import abis_mapping.templates.survey_metadata_v3.mapping


def test_extract_survey_id_set() -> None:
    """Test the extract_survey_id_set method on the Survey metadata mapper"""
    mapper = abis_mapping.templates.survey_metadata_v3.mapping.SurveyMetadataMapper()

    with pathlib.Path("abis_mapping/templates/survey_metadata_v3/examples/minimal.csv").open("rb") as data:
        result = mapper.extract_survey_id_set(data)

    assert result == {"COL1": True, "COL2": True}
