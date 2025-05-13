"""Provides sampling effort unit vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
HOURS = utils.vocabs.Term(
    labels=("Hours",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/936cbae5-5d16-4d98-89c9-315cc3f88f8d"), # real URI
    description="The total time spent actively surveying using the specified protocol, expressed in hours.",
)
MINUTES = utils.vocabs.Term(
    labels=("Minutes",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/91ac9f1f-be73-40a0-b652-c06b289885e0"), # real URI
    description="The total time spent actively surveying using the specified protocol, expressed in minutes.",
)
PERSON_HOURS = utils.vocabs.Term(
    labels=("Person Hours",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/8aeac7d6-39fe-4ce9-b25b-e694a08d3516"), # real URI
    description=(
        "The cumulative amount of time spent by individuals conducting the survey using the specified protocol. "
        "For example, if two people survey for 2 hours each, the total would be 4 person-hours."
    ),
)
TRAP_NIGHTS = utils.vocabs.Term(
    labels=("Trap Nights",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/772b070d-10c0-42f4-8abb-8981b4708861"), # real URI
    description=(
        "The total number of nights traps are left in the field. One trap night refers to one trap set for one night."
    ),
)
METRE_HOURS = utils.vocabs.Term(
    labels=("Metre Hours",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/796b12df-925f-4341-a4d3-c27259d2571f"), # real URI
    description=(
        "The distance (metres) and time (hours) of specific survey activities such as walking or transect surveys "
        "(measure of effort across both space and time)."
    ),
)
METRES = utils.vocabs.Term(
    labels=("Metres",),
    iri=utils.rdf.uri("sampling-effort/metres", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description="A measure of linear distance, to describe the length of transects or areas covered.",
)
HECTARES = utils.vocabs.Term(
    labels=("Hectares",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/67455483-1389-4666-aea1-77162ec149d8"), # real URI
    description="The total area surveyed or sampled, measured in hectares.",
)


class SamplingEffortUnit(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SAMPLING_EFFORT_UNIT"
    definition = rdflib.Literal(
        (
            "In conjunction with the sampling effort value, the sampling effort unit "
            "gives an indication of the effort applied to the specified protocol."
        ),
    )
    base = "bdr-cv/attribute/samplingEffortUnit/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e473bcb9-64b8-409e-a764-fea8bbb92c9c")
    default = None
    terms = (
        HOURS,
        MINUTES,
        PERSON_HOURS,
        TRAP_NIGHTS,
        METRE_HOURS,
        METRES,
        HECTARES,
    )


# Register
utils.vocabs.register(SamplingEffortUnit)
