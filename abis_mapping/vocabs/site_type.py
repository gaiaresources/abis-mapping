"""Provides site type vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


# Terms
SITE = utils.vocabs.Term(
    labels=("SITE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5bf7ae21-a454-440b-bdd7-f2fe982d8de4"),
    description="A place in which study/protocol/sampling activities are conducted.",
)
PARENT_SITE = utils.vocabs.Term(
    labels=("PARENT SITE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ffbe3c8c-23f1-4fc4-8aaf-dfba9f12576c"),
    description="Parent site.",
)
PLOT = utils.vocabs.Term(
    labels=("PLOT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/8cadf069-01d7-4420-b454-cae37740c2a2"),
    description="Land area selected from within a survey region which abiotic and biotic properties are sampled.",
)
QUADRAT = utils.vocabs.Term(
    labels=("QUADRAT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4362c8f2-b3cc-4816-b5a2-fb7bb4c0cff5"),
    description=(
        "A transportable frame (usually a square made out of PVC tube, metal rod or wood) "
        "used to isolate a standard unit of area for study of the distribution of item(s) "
        "over a large area (e.g. a plot)."
    ),
)
TRANSECT = utils.vocabs.Term(
    labels=("TRANSECT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/de46fa49-d1c9-4bef-8462-d7ee5174e1e1"),
    description="A line along which biotic and abiotic characteristics are sampled",
)


# Vocabulary
class SiteType(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SITE_TYPE"
    definition = rdflib.Literal("A type of site.")
    base = "bdr-cv/concept/siteType/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/74aa68d3-28fd-468d-8ff5-7e791d9f7159")
    broader = None
    default = None
    terms = (
        SITE,
        PARENT_SITE,
        PLOT,
        QUADRAT,
        TRANSECT,
    )


# Register
utils.vocabs.Vocabulary.register(SiteType)
