"""Provides sensitivity authority vocabulary"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# TODO Probably will make this a restricted vocabulary at some point.
# Vocabulary
class SensitivityAuthority(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SENSITIVITY_AUTHORITY"
    definition = rdflib.Literal("A type of sensitivityAuthority.")
    base = utils.rdf.uri("bdr-cv/attribute/sensitivityAuthority/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/sensitivityAuthority", utils.namespaces.EXAMPLE)
    default = None  # No default, omitted if not provided
    terms = ()
    publish = False


# Register
utils.vocabs.Vocabulary.register(SensitivityAuthority)