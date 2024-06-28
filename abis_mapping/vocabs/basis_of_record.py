"""Provides basis of record vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
HUMAN_OBSERVATION = utils.vocabs.Term(
    labels=("HUMAN OBSERVATION", ),
    iri=utils.rdf.uri("basisOfRecord/HumanObservation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="An output of a human observation.",
)
OCCURRENCE = utils.vocabs.Term(
    labels=("OCCURRENCE", ),
    iri=utils.rdf.uri("basisOfRecord/Occurrence", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "An existence of an Organism (sensu http://rs.tdwg.org/dwc/terms/Organism)"
        " at a particular place at a particular time."
    ),
)
PRESERVED_SPECIMEN = utils.vocabs.Term(
    labels=("PRESERVED SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/PreservedSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="A specimen that has been preserved.",
)
FOSSIL_SPECIMEN = utils.vocabs.Term(
    labels=("FOSSIL SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/FossilSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="A preserved specimen that is a fossil.",
)
LIVING_SPECIMEN = utils.vocabs.Term(
    labels=("LIVING SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/LivingSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="A specimen that is alive.",
)
MACHINE_OBSERVATION = utils.vocabs.Term(
    labels=("MACHINE OBSERVATION", ),
    iri=utils.rdf.uri("basisOfRecord/MachineObservation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="An output of a machine observation process.",
)
MATERIAL_SAMPLE = utils.vocabs.Term(
    labels=("MATERIAL SAMPLE", ),
    iri=utils.rdf.uri("basisOfRecord/MaterialSample", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A physical result of a sampling (or subsampling) event. In biological collections, the "
        "material sample is typically collected, and either preserved or destructively processed."
    ),
)


# Vocabulary
class BasisOfRecord(utils.vocabs.FlexibleVocabulary):
    vocab_id = "BASIS_OF_RECORD"
    definition = rdflib.Literal("A type of basisOfRecord.")
    base = utils.rdf.uri("bdr-cv/attribute/basisOfRecord/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/basisOfRecord", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None  # No default, omitted if not provided
    terms = (
        HUMAN_OBSERVATION,
        OCCURRENCE,
        PRESERVED_SPECIMEN,
        FOSSIL_SPECIMEN,
        LIVING_SPECIMEN,
        MACHINE_OBSERVATION,
        MATERIAL_SAMPLE,
    )


# Register vocabulary
utils.vocabs.Vocabulary.register(BasisOfRecord)
