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
    base = "bdr-cv/attribute/sensitivityAuthority/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/sensitivityAuthority", utils.namespaces.DATASET_BDR)
    default = None  # No default, omitted if not provided
    terms = ()
    publish = True


# Register
utils.vocabs.register(SensitivityAuthority)
