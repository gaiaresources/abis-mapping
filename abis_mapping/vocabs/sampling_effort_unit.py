"""Provides sampling effort unit vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
HOURS = utils.vocabs.Term(
    labels=("Hours",),
    iri=utils.rdf.uri("sampling-effort/hours", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description="The total time spent actively surveying using the specified protocol, expressed in hours.",
)
MINUTES = utils.vocabs.Term(
    labels=("Minutes",),
    iri=utils.rdf.uri("sampling-effort/minutes", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description="The total time spent actively surveying using the specified protocol, expressed in minutes.",
)
PERSON_HOURS = utils.vocabs.Term(
    labels=("Person Hours",),
    iri=utils.rdf.uri("sampling-effort/person-hours", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description=(
        "The cumulative amount of time spent by individuals conducting the survey using the specified protocol. "
        "For example, if two people survey for 2 hours each, the total would be 4 person-hours."
    ),
)
TRAP_NIGHTS = utils.vocabs.Term(
    labels=("Trap Nights",),
    iri=utils.rdf.uri("sampling-effort/trap-nights", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description=(
        "The total number of nights traps are left in the field. "
        "One trap night refers to one trap set for one night."
    ),
)
KHZ = utils.vocabs.Term(
    labels=("kHz",),
    iri=utils.rdf.uri("sampling-effort/khz", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
    description="The frequency of sound is measured in kilohertz, for acoustic monitoring.",
)
METRE_HOURS = utils.vocabs.Term(
    labels=("Metre Hours",),
    iri=utils.rdf.uri("sampling-effort/metre-hours", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
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
    iri=utils.rdf.uri("sampling-effort/hectares", utils.namespaces.EXAMPLE),  # TODO -> Need real IRI
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
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = None
    default = None
    terms = (
        HOURS,
        MINUTES,
        PERSON_HOURS,
        TRAP_NIGHTS,
        KHZ,
        METRE_HOURS,
        METRES,
        HECTARES,
    )


# Register
utils.vocabs.register(SamplingEffortUnit)
