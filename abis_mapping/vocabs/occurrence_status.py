"""Provides occurrence status vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
PRESENT = utils.vocabs.Term(
    labels=("PRESENT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a2fb93cd-ad72-4c15-b23b-14882c2418c2"),  # real URI
    description="The occurrence was present at the location and time of the observation.",
)
ABSENT = utils.vocabs.Term(
    labels=("ABSENT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2ca99992-75ff-4b48-b426-ca86a0b5d40f"),  # real URI
    description="The occurrence was not present at the location and time of the observation.",
)


# Vocabulary
class OccurrenceStatus(utils.vocabs.FlexibleVocabulary):
    vocab_id = "OCCURRENCE_STATUS"
    definition = rdflib.Literal("A type of occurrenceStatus.")
    base = "bdr-cv/parameter/occurrenceStatus/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/835d7166-2a4d-4335-9d39-8082ff201811")
    default = None  # No default, ommitted if not provided
    terms = (PRESENT, ABSENT)


# Register
utils.vocabs.register(OccurrenceStatus)
