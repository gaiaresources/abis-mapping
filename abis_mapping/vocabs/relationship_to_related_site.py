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
RELATIONSHIP = utils.vocabs.RestrictedVocabulary(
    terms=(SAME_AS, PART_OF),
)
