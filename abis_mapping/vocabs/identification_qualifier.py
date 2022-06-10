"""Provides identification qualifier vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ANIMALIA_CETERA = utils.vocabs.Term(
    labels=("ANIMALIACETERA", "ANIMALIA CETERA", "ANIMALIA_CETERA", "ANIMALIA-CETERA"),
    iri=utils.rdf.uri("identificationQualifier/animalia-cetera", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
CONFER = utils.vocabs.Term(
    labels=("CONFER", ),
    iri=utils.rdf.uri("identificationQualifier/confer", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
EX_GREGE = utils.vocabs.Term(
    labels=("EXGREGE", "EX GREGE", "EX_GREGE", "EX-GREGE"),
    iri=utils.rdf.uri("identificationQualifier/ex-grege", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
FAMILIA_GENUS_SPECIES = utils.vocabs.Term(
    labels=("FAMILIAGENUSSPECIES", "FAMILIA GENUS SPECIES", "FAMILIA_GENUS_SPECIES", "FAMILIA-GENUS-SPECIES"),
    iri=utils.rdf.uri("identificationQualifier/familia-genus-species", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
)
GENUS_ET_SPECIES_NOVA = utils.vocabs.Term(
    labels=("GENUSETSPECIESNOVA", "GENUS ET SPECIES NOVA", "GENUS_ET_SPECIES_NOVA", "GENUS-ET-SPECIES-NOVA"),
    iri=utils.rdf.uri("identificationQualifier/genus-et-species-nova", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
)
GENUS_NOVUM = utils.vocabs.Term(
    labels=("GENUSNOVUM", "GENUS NOVUM", "GENUS_NOVUM", "GENUS-NOVUM"),
    iri=utils.rdf.uri("identificationQualifier/genus-novum", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
GENUS_SPECIES = utils.vocabs.Term(
    labels=("GENUSSPECIES", "GENUS SPECIES", "GENUS_SPECIES", "GENUS-SPECIES"),
    iri=utils.rdf.uri("identificationQualifier/genus-species", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SP = utils.vocabs.Term(
    labels=("SP", ),
    iri=utils.rdf.uri("identificationQualifier/sp", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIES_AFFINIS = utils.vocabs.Term(
    labels=("SPECIESAFFINIS", "SPECIES AFFINIS", "SPECIES_AFFINIS", "SPECIES-AFFINIS",),
    iri=utils.rdf.uri("identificationQualifier/species-affinis", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIES_INCERTA = utils.vocabs.Term(
    labels=("SPECIESINCERTA", "SPECIES INCERTA", "SPECIES_INCERTA", "SPECIES-INCERTA",),
    iri=utils.rdf.uri("identificationQualifier/species-incerta", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIES_INDETERMINABILIS = utils.vocabs.Term(
    labels=("SPECIESINDETERMINABILIS", "SPECIES INDETERMINABILIS", "SPECIES_INDETERMINABILIS", "SPECIES-INDETERMINABILIS",),  # noqa: E501
    iri=utils.rdf.uri("identificationQualifier/species-indeterminabilis", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
)
SPECIES_NOVA = utils.vocabs.Term(
    labels=("SPECIESNOVA", "SPECIES NOVA", "SPECIES_NOVA", "SPECIES-NOVA",),
    iri=utils.rdf.uri("identificationQualifier/species-nova", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIES_PROXIMA = utils.vocabs.Term(
    labels=("SPECIESPROXIMA", "SPECIES PROXIMA", "SPECIES_PROXIMA", "SPECIES-PROXIMA",),
    iri=utils.rdf.uri("identificationQualifier/species-proxima", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPP = utils.vocabs.Term(
    labels=("SPP", ),
    iri=utils.rdf.uri("identificationQualifier/spp", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
STETIT = utils.vocabs.Term(
    labels=("STETIT", ),
    iri=utils.rdf.uri("identificationQualifier/stetit", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBSPECIES = utils.vocabs.Term(
    labels=("SUBSPECIES", ),
    iri=utils.rdf.uri("identificationQualifier/subspecies", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
)

# Vocabulary
IDENTIFICATION_QUALIFIER = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of identificationQualifier."),
    base=utils.rdf.uri("bdr-cv/attribute/identificationQualifier/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=utils.rdf.uri("bdr-cv/attribute/identificationQualifier", utils.namespaces.EXAMPLE),  # TODO -> Need real URI  # noqa: E501
    default=None,  # No default, ommitted if not provided
    terms=(
        ANIMALIA_CETERA,
        CONFER,
        EX_GREGE,
        FAMILIA_GENUS_SPECIES,
        GENUS_ET_SPECIES_NOVA,
        GENUS_NOVUM,
        GENUS_SPECIES,
        SP,
        SPECIES_AFFINIS,
        SPECIES_INCERTA,
        SPECIES_INDETERMINABILIS,
        SPECIES_NOVA,
        SPECIES_PROXIMA,
        SPP,
        STETIT,
        SUBSPECIES,
    ),
)
