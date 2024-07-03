"""Provides sampling effort unit vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


class SamplingEffortUnit(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SAMPLING_EFFORT_UNIT"
    definition = rdflib.Literal("A type of samplingEffortUnit")
    base = utils.rdf.uri("bdr-cv/attribute/samplingEffortUnit/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/concept/samplingEffortUnit", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None
    terms = ()
    publish = False


# Register
utils.vocabs.Vocabulary.register(SamplingEffortUnit)
