"""Provides basis of record vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
HUMAN_OBSERVATION = utils.vocabs.Term(
    labels=("HUMAN OBSERVATION", ),
    iri=utils.rdf.uri("basisOfRecord/HumanObservation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
OCCURRENCE = utils.vocabs.Term(
    labels=("OCCURRENCE", ),
    iri=utils.rdf.uri("basisOfRecord/Occurrence", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
PRESERVED_SPECIMEN = utils.vocabs.Term(
    labels=("PRESERVED SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/PreservedSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
FOSSIL_SPECIMEN = utils.vocabs.Term(
    labels=("FOSSIL SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/FossilSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
LIVING_SPECIMEN = utils.vocabs.Term(
    labels=("LIVING SPECIMEN", ),
    iri=utils.rdf.uri("basisOfRecord/LivingSpecimen", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
MACHINE_OBSERVATION = utils.vocabs.Term(
    labels=("MACHINE OBSERVATION", ),
    iri=utils.rdf.uri("basisOfRecord/MachineObservation", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
MATERIAL_SAMPLE = utils.vocabs.Term(
    labels=("MATERIAL SAMPLE", ),
    iri=utils.rdf.uri("basisOfRecord/MaterialSample", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)


# Vocabulary
BASIS_OF_RECORD = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of basisOfRecord."),
    base=utils.rdf.uri("bdr-cv/attribute/basisOfRecord/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=utils.rdf.uri("bdr-cv/attribute/basisOfRecord", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(
        HUMAN_OBSERVATION,
        OCCURRENCE,
        PRESERVED_SPECIMEN,
        FOSSIL_SPECIMEN,
        LIVING_SPECIMEN,
        MACHINE_OBSERVATION,
        MATERIAL_SAMPLE,
    )
)
