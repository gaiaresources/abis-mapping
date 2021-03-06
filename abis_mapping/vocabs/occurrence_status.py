"""Provides occurrence status vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
PRESENT = utils.vocabs.Term(
    labels=("PRESENT", ),
    iri=utils.rdf.uri("occurrenceStatus/present", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
ABSENT = utils.vocabs.Term(
    labels=("ABSENT", ),
    iri=utils.rdf.uri("occurrenceStatus/absent", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
OCCURRENCE_STATUS = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of occurrenceStatus."),
    base=utils.rdf.uri("bdr-cv/parameter/occurrenceStatus/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/occurrenceStatus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(PRESENT, ABSENT)
)
