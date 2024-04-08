"""Provides sampling effort unit vocabulary for the package."""

# Local
from abis_mapping import utils

# Third-party
import rdflib


SAMPLING_EFFORT_UNIT = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of samplingEffortUnit"),
    base=utils.rdf.uri("bdr-cv/attribute/samplingEffortUnit/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=utils.rdf.uri("bdr-cv/concept/samplingEffortUnit", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,
    terms=(),
)

