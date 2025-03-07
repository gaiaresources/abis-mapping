"""Provides survey type vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
WET_PITFALL_TRAPPING = utils.vocabs.Term(
    labels=("WET PITFALL TRAPPING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/054145e7-137d-50c5-a750-d85a47e81fad"),
    description=(
        "The type/method of invertebrate fauna sampling implemented. Wet pitfall trapping "
        "consists of a grid of 20 traps (specimen containers), dug into the ground so they "
        "are flush with the soil surface, and partially filled with a liquid preservative "
        "to rapidly kill the invertebrates that fall in. The trap grid is established anywhere "
        "within the plot, consisting of 4 north-south rows of 5 traps, spaced 10 m apart."
    ),
)


class SurveyType(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SURVEY_TYPE"
    definition = rdflib.Literal("A type of surveyType")
    base = "bdr-cv/attribute/surveyType/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/concept/surveyType", utils.namespaces.DATASET_BDR)
    default = None
    terms = (WET_PITFALL_TRAPPING,)


# Register
utils.vocabs.register(SurveyType)
