"""Provides sequencing method vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
UNDEFINED = utils.vocabs.Term(
    labels=("UNDEFINED",),
    iri=utils.rdf.uri("sequencingMethod/undefined", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Undefined",
)


# Vocabulary
class SequencingMethod(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SEQUENCING_METHOD"
    definition = rdflib.Literal("A type of sequencingMethod.")
    base = "bdr-cv/methods/sequencingMethod/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c")
    broader = utils.rdf.uri("bdr-cv/methods/sequencingMethod", utils.namespaces.DATASET_BDR)
    default = UNDEFINED
    terms = ()  # No baseline vocabulary values
    publish = True


# Register
utils.vocabs.register(SequencingMethod)
