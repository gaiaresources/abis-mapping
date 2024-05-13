"""Provides sampling protocol vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
HUMAN_OBSERVATION = utils.vocabs.Term(
    labels=("HUMAN OBSERVATION", ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157"),
)
UNSPECIFIED = utils.vocabs.Term(
    labels=("UNSPECIFIED", ),
    iri=utils.rdf.uri("sampling-protocol/default", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
SAMPLING_PROTOCOL = utils.vocabs.FlexibleVocabulary(
    vocab_id="SAMPLING_PROTOCOL",
    definition=rdflib.Literal("A type of samplingProtocol."),
    base=utils.rdf.uri("bdr-cv/methods/samplingProtocol/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c"),
    broader=utils.rdf.uri("bdr-cv/methods/samplingProtocol", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=UNSPECIFIED,
    terms=(HUMAN_OBSERVATION, UNSPECIFIED),
)
