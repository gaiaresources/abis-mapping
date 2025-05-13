"""Provides preparations vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ALCOHOL = utils.vocabs.Term(
    labels=("ALCOHOL",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2466c02f-db6f-4317-ae1c-87d8d372ca37"),  # real URI
    description="Alcohol",
)
DEEPFROZEN = utils.vocabs.Term(
    labels=("DEEP FROZEN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/04c3c50c-fe5c-4536-98bc-8d1fa3cec299"),  # real URI
    description="Deep frozen",
)
DRIED = utils.vocabs.Term(
    labels=("DRIED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e0df7a3e-a1d4-466e-ab9c-c4c3f5face89"),  # real URI
    description="Dried",
)
DRIEDANDPRESSED = utils.vocabs.Term(
    labels=("DRIED AND PRESSED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/0186e0a4-593c-4fd6-a133-d57d62157854"),  # real URI
    description="Dried and pressed",
)
FORMALIN = utils.vocabs.Term(
    labels=("FORMALIN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/aee6e4c5-8d68-40b4-a590-812b757092b9"),  # real URI
    description="Formalin",
)
FREEZEDRIED = utils.vocabs.Term(
    labels=("FREEZE DRIED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fe463c50-2106-43b3-8973-1a369ff16015"),  # real URI
    description="Freeze-dried",
)
GLYCERIN = utils.vocabs.Term(
    labels=("GLYCERIN",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e5c2ee21-c019-47c3-9187-d570e3b7f272"),  # real URI
    description="Glycerin",
)
GUMARABIC = utils.vocabs.Term(
    labels=("GUM ARABIC",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d56d3d1f-4fe8-43ae-9a25-d3762b573d94"),  # real URI
    description="Gum arabic",
)
MICROSCOPICPREPARATION = utils.vocabs.Term(
    labels=("MICROSCOPIC PREPARATION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/f7e7db96-2b3b-445d-a800-d3402176d07f"),  # real URI
    description="Microscopic preparation",
)
MOUNTED = utils.vocabs.Term(
    labels=("MOUNTED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/3c54dec1-f1f7-430a-a15c-47bf5767270b"),  # real URI
    description="Mounted",
)
NOTREATMENT = utils.vocabs.Term(
    labels=("NO TREATMENT",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ad15ae23-4e6e-40dc-80fd-0af65f51e1ce"),  # real URI
    description="No treatment",
)
OTHER = utils.vocabs.Term(
    labels=("OTHER",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a73eb3fe-42d2-424d-974d-cc3562394983"),  # real URI
    description="Other",
)
PINNED = utils.vocabs.Term(
    labels=("PINNED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d4b4e586-ff92-4749-9754-5c20f41e3df3"),  # real URI
    description="Pinned",
)
REFRIGERATED = utils.vocabs.Term(
    labels=("REFRIGERATED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/0ca8c5bb-3d89-48f0-8846-84551eb96bb0"),  # real URI
    description="Refrigerated",
)


# Vocabulary
class Preparations(utils.vocabs.FlexibleVocabulary):
    vocab_id = "PREPARATIONS"
    definition = rdflib.Literal("A type of preparation.")
    base = "bdr-cv/attribute/preparations/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/9694c614-7bb5-4403-bba4-fd01d40bf5c3")
    default = None  # No default, ommitted if not provided
    terms = (
        ALCOHOL,
        DEEPFROZEN,
        DRIED,
        DRIEDANDPRESSED,
        FORMALIN,
        FREEZEDRIED,
        GLYCERIN,
        GUMARABIC,
        MICROSCOPICPREPARATION,
        MOUNTED,
        NOTREATMENT,
        OTHER,
        PINNED,
        REFRIGERATED,
    )


# Register
utils.vocabs.register(Preparations)
