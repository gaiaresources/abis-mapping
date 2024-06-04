"""Provides threat status check protocol vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
UNSPECIFIED = utils.vocabs.Term(
    labels=("UNSPECIFIED", ),
    iri=utils.rdf.uri("threatStatusCheckProtocol/default", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Unspecified",
)

# Vocabulary
CHECK_PROTOCOL = utils.vocabs.FlexibleVocabulary(
    vocab_id="CHECK_PROTOCOL",
    definition=rdflib.Literal("A type of threatStatusCheckProtocol."),
    base=utils.rdf.uri("bdr-cv/methods/threatStatusCheckProtocol/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c"),
    broader=utils.rdf.uri("bdr-cv/methods/threatStatusCheckProtocol", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
    default=UNSPECIFIED,
    terms=(UNSPECIFIED, ),
    publish=False,
)

# Register
utils.vocabs.Vocabulary.register(CHECK_PROTOCOL)
