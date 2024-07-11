"""Declares and registers the incidental occurrence data instruction rendering context."""

# Local
from abis_mapping import vocabs
from docs import contexts
from docs import tables


# Constants
mapper_id = "incidental_occurrence_data-v2.0.0.csv"

# Create context
_ctx = {
    "tables": {
        "fields": tables.fields.FieldTabler(mapper_id).generate_table(as_markdown=True),
        "vocabularies": tables.vocabs.VocabTabler(mapper_id).generate_table(as_markdown=True),
        "threat_status": tables.threat_status.ThreatStatusTabler(mapper_id).generate_table(as_markdown=True),
    },
    "values": {
        "geodetic_datum_count": len(vocabs.geodetic_datum.GeodeticDatum.terms),
    },
}

# Register
contexts.base.register(mapper_id, _ctx)
