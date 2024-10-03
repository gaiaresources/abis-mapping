"""Provides reproductive condition vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Vocabulary
class ReproductiveCondition(utils.vocabs.FlexibleVocabulary):
    vocab_id = "REPRODUCTIVE_CONDITION"
    definition = rdflib.Literal("A type of reproductiveCondition.")
    base = utils.rdf.uri("bdr-cv/parameter/reproductiveCondition/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = utils.rdf.uri("bdr-cv/parameter/reproductiveCondition", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None  # No default, ommitted if not provided
    terms = ()  # No baseline vocabulary values
    publish = False


# Register
utils.vocabs.Vocabulary.register(ReproductiveCondition)
