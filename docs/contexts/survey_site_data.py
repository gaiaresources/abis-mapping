"""Declares and registers the survey site data instruction rendering context."""

# Local
from docs import contexts
from docs import tables


# Constants
mapper_id = "survey_site_data-v1.0.0.csv"


# Declare context
_ctx = {
    "tables": {
        "vocabularies": tables.vocabs.VocabTabler(mapper_id).generate_table(as_markdown=True),
        "fields": tables.fields.FieldTabler(mapper_id).generate_table(as_markdown=True),
    },
}


# Register
contexts.base.register(mapper_id, _ctx)
