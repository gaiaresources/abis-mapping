"""Provides preparations vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ALCOHOL = utils.vocabs.Term(
    labels=("ALCOHOL",),
    iri=utils.rdf.uri("preparations/alcohol", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Alcohol",
)
DEEPFROZEN = utils.vocabs.Term(
    labels=("DEEP FROZEN",),
    iri=utils.rdf.uri("preparations/deepFrozen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Deep frozen",
)
DRIED = utils.vocabs.Term(
    labels=("DRIED",),
    iri=utils.rdf.uri("preparations/dried", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Dried",
)
DRIEDANDPRESSED = utils.vocabs.Term(
    labels=("DRIED AND PRESSED",),
    iri=utils.rdf.uri("preparations/driedAndPressed", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Dried and pressed",
)
FORMALIN = utils.vocabs.Term(
    labels=("FORMALIN",),
    iri=utils.rdf.uri("preparations/formalin", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Formalin",
)
FREEZEDRIED = utils.vocabs.Term(
    labels=("FREEZE DRIED",),
    iri=utils.rdf.uri("preparations/freezeDried", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Freeze-dried",
)
GLYCERIN = utils.vocabs.Term(
    labels=("GLYCERIN",),
    iri=utils.rdf.uri("preparations/glycerin", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Glycerin",
)
GUMARABIC = utils.vocabs.Term(
    labels=("GUM ARABIC",),
    iri=utils.rdf.uri("preparations/gumArabic", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Gum arabic",
)
MICROSCOPICPREPARATION = utils.vocabs.Term(
    labels=("MICROSCOPIC PREPARATION",),
    iri=utils.rdf.uri("preparations/microscopicPreparation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Microscopic preparation",
)
MOUNTED = utils.vocabs.Term(
    labels=("MOUNTED",),
    iri=utils.rdf.uri("preparations/mounted", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Mounted",
)
NOTREATMENT = utils.vocabs.Term(
    labels=("NO TREATMENT",),
    iri=utils.rdf.uri("preparations/noTreatment", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="No treatment",
)
OTHER = utils.vocabs.Term(
    labels=("OTHER",),
    iri=utils.rdf.uri("preparations/other", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Other",
)
PINNED = utils.vocabs.Term(
    labels=("PINNED",),
    iri=utils.rdf.uri("preparations/pinned", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Pinned",
)
REFRIGERATED = utils.vocabs.Term(
    labels=("REFRIGERATED",),
    iri=utils.rdf.uri("preparations/refrigerated", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Refrigerated",
)


# Vocabulary
class Preparations(utils.vocabs.FlexibleVocabulary):
    vocab_id = "PREPARATIONS"
    definition = rdflib.Literal("A type of preparations.")
    base = "bdr-cv/attribute/preparations/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/preparations", utils.namespaces.DATASET_BDR)
    default = None  # No default, ommitted if not provided
    terms = (
        ALCOHOL,
        DEEPFROZEN,
        DRIED,
        DRIEDANDPRESSED,
        FORMALIN,
        FREEZEDRIED,
        GLYCERIN,
        GUMARABIC,
        MICROSCOPICPREPARATION,
        MOUNTED,
        NOTREATMENT,
        OTHER,
        PINNED,
        REFRIGERATED,
    )


# Register
utils.vocabs.register(Preparations)
