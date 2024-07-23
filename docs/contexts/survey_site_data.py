"""Declares and registers the survey site data instruction rendering context."""

# Local
from abis_mapping import base
from docs import contexts
from docs import tables


# Constants
mapper_id = "survey_site_data-v1.0.0.csv"

# Retrieve mapper
mapper = base.mapper.get_mapper(mapper_id)


# Declare context
_ctx = {
    "tables": {
        "vocabularies": tables.vocabs.VocabTabler(mapper_id).generate_table(as_markdown=True),
        "fields": tables.fields.FieldTabler(mapper_id).generate_table(as_markdown=True),
    },
    "metadata": mapper.metadata() if mapper is not None else None,
}


# Register
contexts.base.register(mapper_id, _ctx)
