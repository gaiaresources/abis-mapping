"""Declares and registers the incidental occurrence data instruction rendering context."""

# Local
from abis_mapping import base
from abis_mapping import vocabs
from docs import contexts
from docs import tables


# Constants
mapper_id = "incidental_occurrence_data-v2.0.0.csv"

# Retrieve mapper
mapper = base.mapper.get_mapper(mapper_id)

# Create context
_ctx = {
    "tables": {
        "fields": tables.fields.OccurrenceFieldTabler(template_id=mapper_id, format="markdown").generate_table(),
        "vocabularies": tables.vocabs.VocabTabler(template_id=mapper_id, format="markdown").generate_table(),
        "threat_status": tables.threat_status.ThreatStatusTabler(
            template_id=mapper_id, format="markdown"
        ).generate_table(),
    },
    "values": {
        "geodetic_datum_count": len(vocabs.geodetic_datum.GeodeticDatum.terms),
    },
    "metadata": mapper.metadata() if mapper is not None else None,
}

# Register
contexts.base.register(mapper_id, _ctx)
