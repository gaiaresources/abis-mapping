"""Provides survey type vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
WET_PITFALL_TRAPPING = utils.vocabs.Term(
    labels=("WET PITFALL TRAPPING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/054145e7-137d-50c5-a750-d85a47e81fad")
)

SURVEY_TYPE = utils.vocabs.FlexibleVocabulary(
    vocab_id="SURVEY_TYPE",
    definition=rdflib.Literal("A type of surveyType"),
    base=utils.rdf.uri("bdr-cv/attribute/surveyType/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=utils.rdf.uri("bdr-cv/concept/surveyType", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,
    terms=(WET_PITFALL_TRAPPING,),
)
