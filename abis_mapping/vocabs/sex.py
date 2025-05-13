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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/647cc9ca-3d55-4336-840d-d0a0b6d36231"),  # real URI
    description=(
        "Female (♀) is the sex of an organism, or a part of an organism, which produces mobile ova (egg cells)."
    ),
)
HERMAPHRODITE = utils.vocabs.Term(
    labels=(
        "HERMAPHRODITE",
        "ZWITTER",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fe3b31bf-43af-4735-9d7d-8830fa27e559"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b3b56ae7-bd42-46e3-9391-cac2352a306f"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/8d116443-a711-4c47-816c-71a099e113e9"),  # real URI
    description="If the sex of an organism can't be determined for some reason.",
)


# Vocabulary
class Sex(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SEX"
    definition = rdflib.Literal("A type of sex.")
    base = "bdr-cv/parameter/sex/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/05cbf534-c233-4aa8-a08c-00b28976ed36")
    default = None  # No default, ommitted if not provided
    terms = (FEMALE, HERMAPHRODITE, MALE, UNDETERMINED)


# Register
utils.vocabs.register(Sex)
