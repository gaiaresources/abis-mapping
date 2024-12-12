"""Provides sensitivity category vocabulary"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# TODO complete this vocabulary
# Vocabulary
class SensitivityCategory(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SENSITIVITY_CATEGORY"
    definition = rdflib.Literal("A type of sensitivityCategory.")
    base = "bdr-cv/attribute/sensitivityCategory/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/sensitivityCategory", utils.namespaces.EXAMPLE)
    default = None  # No default, omitted if not provided
    terms = ()
    publish = True


# Register
utils.vocabs.register(SensitivityCategory)
