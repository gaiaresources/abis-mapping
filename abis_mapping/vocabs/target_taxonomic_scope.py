"""Provides target taxonomic scope vocabulary for the package"""

# Third-party
import rdflib

# Local
from abis_mapping import utils


AMPHIBIAN = utils.vocabs.Term(
    labels=("AMPHIBIAN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/538e423a-3f73-5c52-8a30-13ef2ba5e77f"),
)

BIRD = utils.vocabs.Term(
    labels=("BIRD",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f9874c91-f61d-5b74-90d1-aa71d3805b45"),
)

INVERTEBRATE = utils.vocabs.Term(
    labels=("INVERTEBRATE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f03ce044-9c2c-52ec-adf9-5aa4960d58a8"),
)

MAMMALS = utils.vocabs.Term(
    labels=("MAMMALS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e537a3de-6b76-5638-8d95-0a47cc00359a"),
)

NON_VASCULAR_PLANT = utils.vocabs.Term(
    labels=("NON-VASCULAR PLANT",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/599d9085-baad-5f32-86dc-3d112ecdae9c")
)

REPTILE = utils.vocabs.Term(
    labels=("REPTILE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/51bf988a-8672-56f7-96cb-9c363eb0cfd4")
)

VASCULAR_PLANT = utils.vocabs.Term(
    labels=("VASCULAR PLANT",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7def5e09-00a6-5ace-b48b-6f93b4d4bf8a")
)

TARGET_TAXONOMIC_SCOPE = utils.vocabs.FlexibleVocabulary(
    vocab_id="TARGET_TAXONOMIC_SCOPE",
    definition=rdflib.Literal("A type of targetTaxonomicScope"),
    base=utils.rdf.uri("bdr-cv/attribute/targetTaxonomicScope/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7ea12fed-6b87-4c20-9ab4-600b32ce15ec"),
    default=None,
    terms=(
        AMPHIBIAN,
        BIRD,
        INVERTEBRATE,
        MAMMALS,
        NON_VASCULAR_PLANT,
        REPTILE,
        VASCULAR_PLANT,
    ),
)
