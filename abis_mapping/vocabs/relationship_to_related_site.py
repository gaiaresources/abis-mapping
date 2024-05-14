"""Provides relationship to related sites vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
SAME_AS = utils.vocabs.Term(
    labels=("SAMEAS", "SAME AS"),
    iri=rdflib.SDO.sameAs,
)
PART_OF = utils.vocabs.Term(
    labels=("PARTOF", "PART OF"),
    iri=rdflib.SDO.isPartOf
)

# Vocabulary
RELATIONSHIP_TO_RELATED_SITE = utils.vocabs.RestrictedVocabulary(
    vocab_id="RELATIONSHIP_TO_RELATED_SITE",
    terms=(SAME_AS, PART_OF),
)

# Register
utils.vocabs.Vocabulary.register(RELATIONSHIP_TO_RELATED_SITE)
