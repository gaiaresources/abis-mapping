"""Provides sex vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
FEMALE = utils.vocabs.Term(
    labels=("FEMALE", ),
    iri=utils.rdf.uri("sex/female", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
HERMAPHRODITE = utils.vocabs.Term(
    labels=("HERMAPHRODITE", ),
    iri=utils.rdf.uri("sex/hermaphrodite", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
MALE = utils.vocabs.Term(
    labels=("MALE", ),
    iri=utils.rdf.uri("sex/male", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
UNDETERMINED = utils.vocabs.Term(
    labels=("UNDETERMINED", ),
    iri=utils.rdf.uri("sex/undetermined", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
SEX = utils.vocabs.FlexibleVocabulary(
    vocab_id="SEX",
    definition=rdflib.Literal("A type of sex."),
    base=utils.rdf.uri("bdr-cv/parameter/sex/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/sex", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(FEMALE, HERMAPHRODITE, MALE, UNDETERMINED),
)

# Register
utils.vocabs.Vocabulary.register(SEX)
