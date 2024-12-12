"""Provides occurrence status vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
PRESENT = utils.vocabs.Term(
    labels=("PRESENT",),
    iri=utils.rdf.uri("occurrenceStatus/present", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="The occurrence was present at the location and time of the observation.",
)
ABSENT = utils.vocabs.Term(
    labels=("ABSENT",),
    iri=utils.rdf.uri("occurrenceStatus/absent", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="The occurrence was not present at the location and time of the observation.",
)


# Vocabulary
class OccurrenceStatus(utils.vocabs.FlexibleVocabulary):
    vocab_id = "OCCURRENCE_STATUS"
    definition = rdflib.Literal("A type of occurrenceStatus.")
    base = "bdr-cv/parameter/occurrenceStatus/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = utils.rdf.uri("bdr-cv/parameter/occurrenceStatus", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None  # No default, ommitted if not provided
    terms = (PRESENT, ABSENT)


# Register
utils.vocabs.register(OccurrenceStatus)
