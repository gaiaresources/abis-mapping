"""Provides establishment means vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
INTRODUCED = utils.vocabs.Term(
    labels=("INTRODUCED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/3e956639-7ee2-4495-a008-9ddc8522712a"),  # real URI
    description="Establishment of a taxon by numan agency into an area that is not part of its natural range.",
)
INTRODUCED_ASSISTED_COLONISATION = utils.vocabs.Term(
    labels=(
        "INTRODUCED ASSISTED COLONISATION",
        "ASSISTED COLONISATION",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b3aaaa05-5864-42ea-ba63-027f6886bdfe"),  # real URI
    description=(
        "Establishment of a taxon specifically with the intention of creating a self-sustaining wild "
        "population in an area that is not part of the taxon's natural range."
    ),
)
NATIVE = utils.vocabs.Term(
    labels=(
        "NATIVE",
        "NATIVE (INDIGENOUS)",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/0b910634-3f24-4a8c-a7a8-7508c0549a1c"),  # real URI
    description="A taxon occurring within its natural range.",
)
NATIVE_REINTRODUCED = utils.vocabs.Term(
    labels=(
        "NATIVE REINTRODUCED",
        "NATIVE: REINTRODUCED",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6898d732-aa8b-469a-952b-b74a750b01e5"),  # real URI
    description=(
        "A taxon re-established by direct introduction by humans into an area that is not part of "
        "its natural range, but from where it had become extinct."
    ),
)
UNCERTAIN = utils.vocabs.Term(
    labels=(
        "UNCERTAIN",
        "UNKNOWN",
        "CRYPTOGENIC",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fd284078-bb78-4e22-ad49-d9b53166f806"),  # real URI
    description="The origin of the occurrence of the taxon in an area is obscure.",
)
VAGRANT = utils.vocabs.Term(
    labels=(
        "VAGRANT",
        "CASUAL",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/65efed14-5d82-46a9-826a-0f81f48b64ce"),  # real URI
    description="The temporary occurrence of a taxon far outside its natural or migratory range.",
)


# Vocabulary
class EstablishmentMeans(utils.vocabs.FlexibleVocabulary):
    vocab_id = "ESTABLISHMENT_MEANS"
    definition = rdflib.Literal("A type of establishmentMeans.")
    base = "bdr-cv/parameter/establishmentMeans/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/58eaac1c-4c8b-4a95-897f-86dfc83e660f")
    default = None  # No default, omitted if not provided
    terms = (INTRODUCED, INTRODUCED_ASSISTED_COLONISATION, NATIVE, NATIVE_REINTRODUCED, UNCERTAIN, VAGRANT)


# Register
utils.vocabs.register(EstablishmentMeans)
