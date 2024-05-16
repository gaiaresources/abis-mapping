"""Provides establishment means vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
INTRODUCED = utils.vocabs.Term(
    labels=("INTRODUCED", ),
    iri=utils.rdf.uri("establishmentMeans/introduced", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INTRODUCED_ASSISTED_COLONISATION = utils.vocabs.Term(
    labels=("INTRODUCED ASSISTED COLONISATION", ),
    iri=utils.rdf.uri("establishmentMeans/introducedAssistedColonisation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
)
NATIVE = utils.vocabs.Term(
    labels=("NATIVE", ),
    iri=utils.rdf.uri("establishmentMeans/native", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
NATIVE_REINTRODUCED = utils.vocabs.Term(
    labels=("NATIVE REINTRODUCED", ),
    iri=utils.rdf.uri("establishmentMeans/nativeReintroduced", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
UNCERTAIN = utils.vocabs.Term(
    labels=("UNCERTAIN", ),
    iri=utils.rdf.uri("establishmentMeans/uncertain", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
VAGRANT = utils.vocabs.Term(
    labels=("VAGRANT", ),
    iri=utils.rdf.uri("establishmentMeans/vagrant", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
ESTABLISHMENT_MEANS = utils.vocabs.FlexibleVocabulary(
    vocab_id="ESTABLISHMENT_MEANS",
    definition=rdflib.Literal("A type of establishmentMeans."),
    base=utils.rdf.uri("bdr-cv/parameter/establishmentMeans/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/establishmentMeans", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(INTRODUCED, INTRODUCED_ASSISTED_COLONISATION, NATIVE, NATIVE_REINTRODUCED, UNCERTAIN, VAGRANT),
)

# Register
utils.vocabs.Vocabulary.register(ESTABLISHMENT_MEANS)
