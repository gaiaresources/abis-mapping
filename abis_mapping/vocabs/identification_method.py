"""Provides identification method vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# TERMS
UNDEFINED = utils.vocabs.Term(
    labels=("UNDEFINED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2eef4e87-beb3-449a-9251-f59f5c07d653"),
    description="Undefined",
)


# Vocabulary
class IdentificationMethod(utils.vocabs.FlexibleVocabulary):
    vocab_id = "IDENTIFICATION_METHOD"
    definition = rdflib.Literal("A type of identificationMethod.")
    base = utils.rdf.uri("bdr-cv/methods/identificationMethod/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c")
    broader = utils.rdf.uri("bdr-cv/methods/identificationMethod", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = UNDEFINED
    terms = ()  # No baseline vocabulary values
    publish = True


# Register
utils.vocabs.Vocabulary.register(IdentificationMethod)
