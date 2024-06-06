"""Provides relationship to related sites vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
SAME_AS = utils.vocabs.Term(
    labels=("SAME AS", ),
    iri=rdflib.SDO.sameAs,
    description="When two sites are the same."
)
PART_OF = utils.vocabs.Term(
    labels=("PART OF", ),
    iri=rdflib.SDO.isPartOf,
    description="When a site is a subset of another site."
)

# Vocabulary
RELATIONSHIP_TO_RELATED_SITE = utils.vocabs.RestrictedVocabulary(
    vocab_id="RELATIONSHIP_TO_RELATED_SITE",
    terms=(SAME_AS, PART_OF),
)

# Register
utils.vocabs.Vocabulary.register(RELATIONSHIP_TO_RELATED_SITE)
