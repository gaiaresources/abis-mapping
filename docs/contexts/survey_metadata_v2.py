"""Declares and registers the survey metadata v2 instruction rendering context."""

# Local
from abis_mapping import base
from abis_mapping import vocabs
import abis_mapping.templates.survey_metadata_v2.mapping
from docs import contexts
from docs import tables


# Constants
mapper = abis_mapping.templates.survey_metadata_v2.mapping.SurveyMetadataMapper
mapper_id = mapper().template_id

if mapper_id in base.mapper.get_mappers():
    # Create context
    _ctx = {
        "tables": {
            "fields": tables.fields.FieldTabler(template_id=mapper_id, format="markdown").generate_table(),
            "vocabularies": tables.vocabs.VocabTabler(template_id=mapper_id, format="markdown").generate_table(),
        },
        "values": {
            "geodetic_datum_count": len(vocabs.geodetic_datum.GeodeticDatum.terms),
        },
        "metadata": mapper.metadata(),
    }

    # Register
    contexts.base.register(mapper_id, _ctx)