"""Provides identification qualifier vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ANIMALIA_CETERA = utils.vocabs.Term(
    labels=(
        "ANIMALIA CETERA",
        "A.C.",
    ),
    iri=utils.rdf.uri("identificationQualifier/animalia-cetera", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "It groups all the unidentified specimens that are not listed as separate "
        "taxa. The term cetera (abbreviated c. or cet.) may be applied to a given "
        "high-rank taxon, meaning that identification at a lower taxonomic level has "
        "not been attempted (see also stetit) but explicitly not including "
        "subordinate taxa that may have been identified."
    ),
)
CONFER = utils.vocabs.Term(
    labels=(
        "CONFER",
        "CF.",
        "CFR.",
        "CONF.",
        "SP. CF.",
    ),
    iri=utils.rdf.uri("identificationQualifier/confer", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        '"Compare with". Specimens should be compared to reference material, '
        "since most of the diagnostic characters correspond to a given species but "
        "some are unclear. Also used in the sense of affinis and species incerta "
        "(these usages are discouraged)."
    ),
)
EX_GREGE = utils.vocabs.Term(
    labels=(
        "EX GREGE",
        "EX GR.",
        "GR.",
    ),
    iri=utils.rdf.uri("identificationQualifier/ex-grege", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        '"Of the group including". The specimen has some affinity to a known '
        "species or it belongs to a species group or species complex; see also "
        "affinis and species proxima."
    ),
)
FAMILIA_GENUS_SPECIES = utils.vocabs.Term(
    labels=(
        "FAMILIA GENUS SPECIES",
        "FAM. GEN. SP.",
    ),
    iri=utils.rdf.uri(
        "identificationQualifier/familia-genus-species", utils.namespaces.EXAMPLE
    ),  # TODO -> Need real URI
    description="The specimen has not been attributed to any known species nor family; see also species.",
)
GENUS_ET_SPECIES_NOVA = utils.vocabs.Term(
    labels=(
        "GENUS ET SPECIES NOVA",
        "GEN. ET SP.",
        "GEN. NOV.",
        "SP. NOV.",
        "NOV. GEN. ET SP.",
    ),
    iri=utils.rdf.uri(
        "identificationQualifier/genus-et-species-nova", utils.namespaces.EXAMPLE
    ),  # TODO -> Need real URI
    description=(
        "The specimen is considered to belong to a new species and a new genus; for more details, see species nova."
    ),
)
GENUS_NOVUM = utils.vocabs.Term(
    labels=(
        "GENUS NOVUM",
        "GEN. NOV.",
        "G. NOV.",
        "GEN. N.",
        "G. N.",
        "NOV. GEN",
    ),
    iri=utils.rdf.uri("identificationQualifier/genus-novum", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The specimen is considered to belong to a new species and a new genus; for more details, see species nova"
    ),
)
GENUS_SPECIES = utils.vocabs.Term(
    labels=(
        "GENUS SPECIES",
        "GEN. SP.",
        "G. SP.",
    ),
    iri=utils.rdf.uri("identificationQualifier/genus-species", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="The specimen has not been related to any known species nor genus; also species.",
)
SP = utils.vocabs.Term(
    labels=(
        "SPECIES",
        "SP",
    ),
    iri=utils.rdf.uri("identificationQualifier/sp", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The specimen has not been identified, nor it has been related to any "
        "known species; the uncertainty is potentially provisional: it could be due to "
        "the lack of suitable dichotomous keys, or to the occurrence of a species "
        "not previously described. Also used in the sense of species "
        "indeterminabilis and stetit (these usages are discouraged."
    ),
)
SPECIES_PL = utils.vocabs.Term(
    labels=(
        "SPECIES (PL.)",
        "SPP.",
        "SP. PL.",
    ),
    iri=utils.rdf.uri("identificationQualifier/species-pl", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="More than one species belonging to the same genus (or higher-rank taxon) are included.",
)
SPECIES_AFFINIS = utils.vocabs.Term(
    labels=(
        "SPECIES AFFINIS",
        "AFF.",
        "SP. AFF.",
    ),
    iri=utils.rdf.uri("identificationQualifier/species-affinis", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        '"Has affinity with". The specimen has some affinity to a known species but '
        "it is not identical to it; it generally implies distinction more than a possible "
        "identity, in contrast with the qualifier confer; see also species Proxima and "
        "ex grege. It is often used in combination with the ON qualifier species "
        "nova. Also used in the sense of confer (this usage is discouraged)."
    ),
)
SPECIES_INCERTA = utils.vocabs.Term(
    labels=(
        "SPECIES INCERTA",
        "SP. INC.",
    ),
    iri=utils.rdf.uri("identificationQualifier/species-incerta", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The identification is uncertain; it usually indicates a higher reliability with ?, sp. Inc "
        'respect to confer. The sign "sp. inc." is also used in the sense of species, '
        "species indeterminabilis and species inquirenda (these usages are "
        "discouraged)."
    ),
)
SPECIES_INDETERMINABILIS = utils.vocabs.Term(
    labels=(
        "SPECIES INDETERMINABILIS",
        "INDET.",
        "IND.",
        "SP. INDET.",
        "SP. IND.",
    ),
    iri=utils.rdf.uri(
        "identificationQualifier/species-indeterminabilis", utils.namespaces.EXAMPLE
    ),  # TODO -> Need real URI
    description=(
        "The specimen is indeterminable beyond a certain taxonomic level due to "
        "the deterioration or lack of diagnostic characters. Also used in the sense "
        "of species and stetit (these usages are discouraged."
    ),
)
SPECIES_NOVA = utils.vocabs.Term(
    labels=(
        "SPECIES NOVA",
        "SP. NOV.",
        "SPEC. NOV.",
        "SP. N.",
        "NOV. SP.",
        "NOV. SPEC.",
        "N. SP.",
    ),
    iri=utils.rdf.uri("identificationQualifier/species-nova", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The specimen is considered to belong to a new, previously undescribed "
        "(1) When describing a new species, the use of the qualifier is required by "
        "the ICZN (1999) to explicitly indicate the taxa name as intentionally new. "
        "(2) Used as ON qualifier to refer to a new, still unnamed species before "
        "the formal publication of the description."
    ),
)
SPECIES_PROXIMA = utils.vocabs.Term(
    labels=(
        "SPECIES PROXIMA",
        "PROX.",
        "SP. PROX.",
        "NR.",
        "SP.NR.",
    ),
    iri=utils.rdf.uri("identificationQualifier/species-proxima", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The specimen is near to a known species but it is not identical to it; see also affinis and ex grege."
    ),
)
STETIT = utils.vocabs.Term(
    labels=(
        "STETIT",
        "STET.",
    ),
    iri=utils.rdf.uri("identificationQualifier/stetit", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "Identification at a lower taxonomic level has not been attempted, even if "
        "allowed by the sample conditions. It may also be used when more records "
        "with different ON qualifiers need to be merged at a safe taxonomic level."
    ),
)
SUBSPECIES = utils.vocabs.Term(
    labels=(
        "SUBSPECIES",
        "SSP.",
        "SUBSP.",
    ),
    iri=utils.rdf.uri("identificationQualifier/subspecies", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The only infraspecific rank regulated by the ICZN (1999). As ON qualifier, "
        "it indicates that the specimen probably belongs to a subspecies but it has "
        "not been related to any known one; see also species."
    ),
)


# Vocabulary
class IdentificationQualifier(utils.vocabs.FlexibleVocabulary):
    vocab_id = "IDENTIFICATION_QUALIFIER"
    definition = rdflib.Literal("A type of identificationQualifier.")
    base = "bdr-cv/attribute/identificationQualifier/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = utils.rdf.uri("bdr-cv/attribute/identificationQualifier", utils.namespaces.DATASET_BDR)
    default = None  # No default, ommitted if not provided
    terms = (
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
        STETIT,
        SUBSPECIES,
    )


# Register
utils.vocabs.register(IdentificationQualifier)
