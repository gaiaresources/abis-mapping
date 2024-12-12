"""Declares and registers the incidental occurrence data instruction rendering context."""

# Local
from abis_mapping import base
from abis_mapping import vocabs
from docs import contexts
from docs import tables

# Typing
from typing import Any

# Constants
mapper_id = "incidental_occurrence_data-v3.0.0.csv"


# Create context
def _ctx() -> dict[str, Any]:
    """Returns the context for rendering the instructions of the mapper."""
    # Retrieve mapper
    mapper = base.mapper.get_mapper(mapper_id)

    # Return
    return {
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


# Register once the mapper is also registered
if mapper_id in base.mapper.registered_ids():
    contexts.base.register(mapper_id, _ctx())
