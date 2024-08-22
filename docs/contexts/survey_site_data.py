"""Declares and registers the survey site data instruction rendering context."""

# Local
from abis_mapping import base
from docs import contexts
from docs import tables
from abis_mapping import vocabs


# Constants
mapper_id = "survey_site_data-v1.0.0.csv"

# Retrieve mapper
mapper = base.mapper.get_mapper(mapper_id)


# Declare context
_ctx = {
    "tables": {
        "vocabularies": tables.vocabs.VocabTabler(
            template_id=mapper_id,
            format="markdown",
        ).generate_table(),
        "fields": tables.fields.FieldTabler(
            template_id=mapper_id,
            format="markdown",
        ).generate_table(),
    },
    "values": {
        "geodetic_datum_count": len(vocabs.geodetic_datum.GeodeticDatum.terms),
    },
    "metadata": mapper.metadata() if mapper is not None else None,
}


# Register
contexts.base.register(mapper_id, _ctx)
