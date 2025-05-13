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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/86586db3-6e5e-4e3f-8e67-9e9c39161fe3"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4b2f5fc9-3dc9-499c-b334-3563f757cf0a"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/3af18778-ea6e-4e5e-8ec0-da9d59f4d075"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/3af18778-ea6e-4e5e-8ec0-da9d59f4d075"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a7239472-6773-4ba0-b420-4b233fc7c13a"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4e24b030-b2a2-476a-9c9b-bac2b636eb98"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/591a8af1-dd89-4b79-a663-2ef18d3a5258"),  # real URI
    description="The specimen has not been related to any known species nor genus; also species.",
)
SP = utils.vocabs.Term(
    labels=(
        "SPECIES",
        "SP",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/0325eb2d-e89d-4976-8e3e-9a6ff8c0d460"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/681bb140-cbbb-4f4a-a572-9364e9ccd99d"),  # real URI
    description="More than one species belonging to the same genus (or higher-rank taxon) are included.",
)
SPECIES_AFFINIS = utils.vocabs.Term(
    labels=(
        "SPECIES AFFINIS",
        "AFF.",
        "SP. AFF.",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/f17e64f8-02c1-40c5-9ad2-51155c92e0a3"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/1eca8b2f-0d8a-4638-ba85-6f380005901b"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/81f8cfa5-f4f5-4434-b140-04402835d346"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2586fc89-269d-468a-9f43-87de53408519"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e09b5da0-8a77-4b33-b051-a616a3ccf087"),  # real URI
    description=(
        "The specimen is near to a known species but it is not identical to it; see also affinis and ex grege."
    ),
)
STETIT = utils.vocabs.Term(
    labels=(
        "STETIT",
        "STET.",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/8ff9701a-af67-435b-a1bf-030125235fc2"),  # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/aa8f0f92-83d1-4b54-9a09-16b26a407f70"),  # real URI
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
    broader = iri = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/88f031cb-fed1-46fd-985d-f31ba0fd603e")
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
