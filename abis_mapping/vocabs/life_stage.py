"""Provides life stage vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ADULT = utils.vocabs.Term(
    labels=("ADULT", ),
    iri=utils.rdf.uri("lifeStage/adult", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
EMBRYO = utils.vocabs.Term(
    labels=("EMBRYO", ),
    iri=utils.rdf.uri("lifeStage/embryo", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
GAMETE = utils.vocabs.Term(
    labels=("GAMETE", ),
    iri=utils.rdf.uri("lifeStage/gamete", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
GAMETOPHYTE = utils.vocabs.Term(
    labels=("GAMETOPHYTE", ),
    iri=utils.rdf.uri("lifeStage/gametophyte", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
JUVENILE = utils.vocabs.Term(
    labels=("JUVENILE", ),
    iri=utils.rdf.uri("lifeStage/juvenile", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
LARVA = utils.vocabs.Term(
    labels=("LARVA", ),
    iri=utils.rdf.uri("lifeStage/larva", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
PUPA = utils.vocabs.Term(
    labels=("PUPA", ),
    iri=utils.rdf.uri("lifeStage/pupa", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPORE = utils.vocabs.Term(
    labels=("SPORE", ),
    iri=utils.rdf.uri("lifeStage/spore", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPOROPHYTE = utils.vocabs.Term(
    labels=("SPOROPHYTE", ),
    iri=utils.rdf.uri("lifeStage/sporophyte", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
ZYGOTE = utils.vocabs.Term(
    labels=("ZYGOTE", ),
    iri=utils.rdf.uri("lifeStage/zygote", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
LIFE_STAGE = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of lifeStage."),
    base=utils.rdf.uri("bdr-cv/parameter/lifeStage/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/lifeStage", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(
        ADULT,
        EMBRYO,
        GAMETE,
        GAMETOPHYTE,
        JUVENILE,
        LARVA,
        PUPA,
        SPORE,
        SPOROPHYTE,
        ZYGOTE,
    ),
)
