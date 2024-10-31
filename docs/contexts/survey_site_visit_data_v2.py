"""Declares and registers the survey site visit data v2 instruction rendering context."""

# Local
from abis_mapping import base
import abis_mapping.templates.survey_site_visit_data_v2.mapping
from docs import contexts
from docs import tables


# Constants
mapper = abis_mapping.templates.survey_site_visit_data_v2.mapping.SurveySiteVisitMapper
mapper_id = mapper().template_id

if mapper_id in base.mapper.get_mappers():
    # Declare context
    _ctx = {
        "tables": {
            "vocabularies": tables.vocabs.VocabTabler(template_id=mapper_id, format="markdown").generate_table(),
            "fields": tables.fields.FieldTabler(template_id=mapper_id, format="markdown").generate_table(),
        },
        "values": {},
        "metadata": mapper.metadata(),
    }

    # Register
    contexts.base.register(mapper_id, _ctx)
