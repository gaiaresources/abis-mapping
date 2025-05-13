"""Provides threat status check protocol vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
UNSPECIFIED = utils.vocabs.Term(
    labels=("UNSPECIFIED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fd083167-3cbf-4f7e-a611-4550a5926a8b"),  # real URI
    description="Unspecified",
)


# Vocabulary
class CheckProtocol(utils.vocabs.FlexibleVocabulary):
    vocab_id = "CHECK_PROTOCOL"
    definition = rdflib.Literal("A type of threatStatusCheckProtocol.")
    base = "bdr-cv/methods/threatStatusCheckProtocol/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c")
    broader = utils.rdf.uri("bdr-cv/methods/threatStatusCheckProtocol", utils.namespaces.DATASET_BDR)
    default = UNSPECIFIED
    terms = (UNSPECIFIED,)
    publish = True


# Register
utils.vocabs.register(CheckProtocol)
