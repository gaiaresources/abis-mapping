"""Provides basis of record vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
HUMAN_OBSERVATION = utils.vocabs.Term(
    labels=("HUMAN OBSERVATION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d8a47898-e5cb-45f5-be87-e4a7dc5d053e"),  # real URI
    description="An output of a human observation.",
)
OCCURRENCE = utils.vocabs.Term(
    labels=("OCCURRENCE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4008182b-422e-400e-8957-13ca13dbac6b"),  # real URI
    description=(
        "An existence of an Organism (sensu http://rs.tdwg.org/dwc/terms/Organism)"
        " at a particular place at a particular time."
    ),
)
PRESERVED_SPECIMEN = utils.vocabs.Term(
    labels=("PRESERVED SPECIMEN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/1644f015-216f-4691-bb42-44d3a93bb277"),  # real URI
    description="A specimen that has been preserved.",
)
FOSSIL_SPECIMEN = utils.vocabs.Term(
    labels=("FOSSIL SPECIMEN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/0f876e28-1175-41be-a8e5-ca040444421b"),  # real URI
    description="A preserved specimen that is a fossil.",
)
LIVING_SPECIMEN = utils.vocabs.Term(
    labels=("LIVING SPECIMEN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d7457b40-94dc-4b18-b7ef-dd3c6744fd02"),  # real URI
    description="A specimen that is alive.",
)
MACHINE_OBSERVATION = utils.vocabs.Term(
    labels=("MACHINE OBSERVATION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/90cf285e-ed6d-41f6-aaea-8331e9bd07df"),  # real URI
    description="An output of a machine observation process.",
)
MATERIAL_SAMPLE = utils.vocabs.Term(
    labels=("MATERIAL SAMPLE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6ad1354b-3131-4663-9c78-45c015d42a35"),  # real URI
    description=(
        "A physical result of a sampling (or subsampling) event. In biological collections, the "
        "material sample is typically collected, and either preserved or destructively processed."
    ),
)


# Vocabulary
class BasisOfRecord(utils.vocabs.FlexibleVocabulary):
    vocab_id = "BASIS_OF_RECORD"
    definition = rdflib.Literal("A type of basisOfRecord.")
    base = "bdr-cv/attribute/basisOfRecord/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/633119a9-6c8a-46ae-a78a-23a4fd371eb2")
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
utils.vocabs.register(BasisOfRecord)
