"""Provides visit protocol name vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# TODO confirm attributes on this vocab are right once we have RDF spec
class VisitProtocolName(utils.vocabs.FlexibleVocabulary):
    vocab_id = "VISIT_PROTOCOL_NAME"
    definition = rdflib.Literal("A type of protocolName")  # TODO confirm this is right
    base = utils.rdf.uri("bdr-cv/attribute/protocolName/")  # TODO confirm this is right
    scheme = rdflib.URIRef(
        "http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"
    )  # TODO confirm this is right
    broader = None
    default = None
    terms = ()
    publish = False


# Register
utils.vocabs.Vocabulary.register(VisitProtocolName)
