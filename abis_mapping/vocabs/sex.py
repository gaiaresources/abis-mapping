"""Provides sex vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
FEMALE = utils.vocabs.Term(
    labels=(
        "FEMALE",
        "F",
        "♀",
    ),
    iri=utils.rdf.uri("sex/female", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "Female (♀) is the sex of an organism, or a part of an organism, which " "produces mobile ova (egg cells)."
    ),
)
HERMAPHRODITE = utils.vocabs.Term(
    labels=(
        "HERMAPHRODITE",
        "ZWITTER",
    ),
    iri=utils.rdf.uri("sex/hermaphrodite", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "One organism having both male and female sexual characteristics and "
        "organs; at birth an unambiguous assignment of male or female cannot be "
        "made"
    ),
)
MALE = utils.vocabs.Term(
    labels=(
        "MALE",
        "M",
        "♂",
    ),
    iri=utils.rdf.uri("sex/male", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "Male (♂) refers to the sex of an organism, or part of an organism, which "
        "produces small mobile gametes, called spermatozoa."
    ),
)
UNDETERMINED = utils.vocabs.Term(
    labels=(
        "UNDETERMINED",
        "UNDET.",
        "UNKNOWN",
    ),
    iri=utils.rdf.uri("sex/undetermined", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="If the sex of an organism can't be determined for some reason.",
)


# Vocabulary
class Sex(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SEX"
    definition = rdflib.Literal("A type of sex.")
    base = "bdr-cv/parameter/sex/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = utils.rdf.uri("bdr-cv/parameter/sex", utils.namespaces.DATASET_BDR)
    default = None  # No default, ommitted if not provided
    terms = (FEMALE, HERMAPHRODITE, MALE, UNDETERMINED)


# Register
utils.vocabs.register(Sex)
