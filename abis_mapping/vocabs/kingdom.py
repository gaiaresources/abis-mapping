"""Provides kingdom vocabularies for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
# Kingdom
ANIMALIA = utils.vocabs.Term(
    labels=("ANIMALIA",),
    iri=utils.rdf.uri("kingdom/animalia", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Kingdom Animalia",
)
PLANTAE = utils.vocabs.Term(
    labels=(
        "PLANTAE",
        "PLANTAE HAECKEL",
    ),
    iri=utils.rdf.uri("kingdom/plantae", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Kingdom (taxonRank: Regnum) Fungi",
)
FUNGI = utils.vocabs.Term(
    labels=("FUNGI",),
    iri=utils.rdf.uri("kingdom/fungi", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Kingdom (taxonRank: Regnum) Fungi",
)
# Kingdom Occurrences
ANIMALIA_OCCURRENCE = utils.vocabs.Term(
    labels=("ANIMALIA",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"),
    description="Kingdom Animalia",
)
PLANTAE_OCCURRENCE = utils.vocabs.Term(
    labels=(
        "PLANTAE",
        "PLANTAE HAECKEL",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b311c0d3-4a1a-4932-a39c-f5cdc1afa611"),
    description="Kingdom (taxonRank: Regnum) Plantae",
)
FUNGI_OCCURRENCE = utils.vocabs.Term(
    labels=("FUNGI",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"),
    description="Kingdom (taxonRank: Regnum) Fungi",
)
# Kingdom Specimens
ANIMALIA_SPECIMEN = utils.vocabs.Term(
    labels=("ANIMALIA",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"),
    description="Kingdom Animalia",
)
PLANTAE_SPECIMEN = utils.vocabs.Term(
    labels=(
        "PLANTAE",
        "PLANTAE HAECKEL",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2e122e23-881c-43fa-a921-a8745f016ceb"),
    description="Kingdom (taxonRank: Regnum) Plantae",
)
FUNGI_SPECIMEN = utils.vocabs.Term(
    labels=("FUNGI",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"),
    description="Kingdom (taxonRank: Regnum) Fungi",
)


# Vocabularies
class Kingdom(utils.vocabs.FlexibleVocabulary):
    """DEPRECATED: Do not use this vocabulary for new templates."""

    vocab_id = "KINGDOM"
    definition = rdflib.Literal("A type of kingdom.")
    base = "bdr-cv/attribute/kingdom/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/kingdom", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None  # No default, kingdom is required in the CSV
    terms = (ANIMALIA, PLANTAE, FUNGI)


class KingdomOccurrence(utils.vocabs.FlexibleVocabulary):
    vocab_id = "KINGDOM_OCCURRENCE"
    definition = rdflib.Literal(
        "The existence of the organism from this kingdom sampled at a particular place at a particular time."
    )
    base = "bdr-cv/featureType/occurrence/kingdom/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/68af3d25-c801-4089-afff-cf701e2bd61d")
    broader = None  # No broader, top level concept
    default = None  # No default, kingdom is required in the CSV
    terms = (ANIMALIA_OCCURRENCE, PLANTAE_OCCURRENCE, FUNGI_OCCURRENCE)

    def _add_pref_label(
        self,
        iri: rdflib.URIRef,
        value: str,
    ) -> None:
        """Overrides the adding of the skos:prefLabel predicated triple for a new concept.

        Args:
            iri (rdflib.URIRef): The iri of the concept.
            value (str): Raw value provided within the supplied data.
        """
        # Add triple to graph
        self.graph.add((iri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{value} occurrence")))


class KingdomSpecimen(utils.vocabs.FlexibleVocabulary):
    vocab_id = "KINGDOM_SPECIMEN"
    definition = rdflib.Literal("A specimen sampled from an organism of this kingdom.")
    base = "bdr-cv/featureType/specimen/kingdom/"
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/68af3d25-c801-4089-afff-cf701e2bd61d")
    broader = None  # No broader, top level concept
    default = None  # No default, kingdom is required in the CSV
    terms = (ANIMALIA_SPECIMEN, PLANTAE_SPECIMEN, FUNGI_SPECIMEN)

    def _add_pref_label(
        self,
        iri: rdflib.URIRef,
        value: str,
    ) -> None:
        """Overrides the adding of the skos:prefLabel predicated triple for a new concept.

        Args:
            iri (rdflib.URIRef): The iri of the concept.
            value (str): Raw value provided within the supplied data.
        """
        # Add triple to graph
        self.graph.add((iri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{value} specimen")))


# Register
utils.vocabs.register(Kingdom)
utils.vocabs.register(KingdomOccurrence)
utils.vocabs.register(KingdomSpecimen)
