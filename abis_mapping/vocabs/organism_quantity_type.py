"""Provides organism quantity vocabulary for the package"""

# Local
from abis_mapping import utils

# Third-party
import rdflib

# Terms
PERCENTAGE_OF_SPECIES = utils.vocabs.Term(
    labels=(
        "PERCENTAGE OF SPECIES",
        "% OF SPECIES",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfSpecies"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded as "
        "a percentage of the total individual count of all species."
    ),
)

PERCENTAGE_OF_BIOVOLUME = utils.vocabs.Term(
    labels=(
        "PERCENTAGE OF BIOVOLUME",
        "% OF BIOVOLUME",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiovolume"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as a percentage of the total biovolume of all species."
    ),
)

PERCENTAGE_OF_BIOMASS = utils.vocabs.Term(
    labels=(
        "PERCENTAGE OF BIOMASS",
        "% OF BIOMASS",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiomass"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as a percentage of the total biomass of all species."
    ),
)

PERCENTAGE_COVERAGE = utils.vocabs.Term(
    labels=(
        "PERCENTAGE COVERAGE",
        "% COVERAGE",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageCoverage"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the percentage coverage of the total area being sampled."
    ),
)

INDIVIDUALS = utils.vocabs.Term(
    labels=("INDIVIDUALS",),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/individuals"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the number of individuals (e.g.per litre, per square metre, per cubic metre, per hour, per day)."
    ),
)

DOMIN_SCALE = utils.vocabs.Term(
    labels=("DOMIN SCALE",),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/dominScale"),
    description=("A measurement type where the cover of a species in a sample is recorded using the Domin scale."),
)

BRAUN_BLANQUET_SCALE = utils.vocabs.Term(
    labels=("BRAUN BLANQUET SCALE",),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/braunBlanquetScale"),
    description=(
        "A measurement type where the cover of a species in a sample is recorded using the Braun-Blanquet scale."
    ),
)

BIOMASS_AFDG = utils.vocabs.Term(
    labels=(
        "BIOMASS AFDG",
        "BIOMASS ASH FREE DRY WEIGHT IN GRAMS",
        "BIOMASS ASH FREE DRY WEIGHT GRAMS",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassAFDG"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the ash free dry weight biomass in grams (g)."
    ),
)

BIOMASS_G = utils.vocabs.Term(
    labels=(
        "BIOMASS G",
        "BIOMASS IN GRAMS",
        "BIOMASS GRAMS",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassG"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded as the biomass in grams (g)."
    ),
)

BIOMASS_KG = utils.vocabs.Term(
    labels=(
        "BIOMASS KG",
        "BIOMASS IN KILOGRAMS",
        "BIOMASS KILOGRAMS",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassKg"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded as the biomass in kilograms (kg)."
    ),
)

BIOVOLUME_CUBIC_MICRONS = utils.vocabs.Term(
    labels=(
        "BIOVOLUME CUBIC MICRONS",
        "BIOVOLUME IN CUBIC MICRONS",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biovolumeCubicMicrons"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the biovolume in cubic microns (µ ^ 3)."
    ),
)

BIOVOLUME_ML = utils.vocabs.Term(
    labels=(
        "BIOVOLUME ML",
        "BIOVOLUME IN MILLILITRES",
        "BIOVOLUME MILLILITRES",
    ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biovolumeMl"),
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the biovolume in millilitres (ml)."
    ),
)


# Vocab
class OrganismQuantityType(utils.vocabs.FlexibleVocabulary):
    vocab_id = "ORGANISM_QUANTITY_TYPE"
    definition = rdflib.Literal("A type of organism quantity.")
    base = "bdr-cv/concept/organismQuantityType/"
    proposed_scheme = rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType")
    broader = utils.rdf.uri("bdr-cv/concept/organismQuantityType", utils.namespaces.DATASET_BDR)
    default = None  # No default, ommitted if not provided.
    terms = (
        PERCENTAGE_OF_SPECIES,
        PERCENTAGE_OF_BIOVOLUME,
        PERCENTAGE_OF_BIOMASS,
        PERCENTAGE_COVERAGE,
        INDIVIDUALS,
        DOMIN_SCALE,
        BRAUN_BLANQUET_SCALE,
        BIOMASS_AFDG,
        BIOMASS_G,
        BIOMASS_KG,
        BIOVOLUME_CUBIC_MICRONS,
        BIOVOLUME_ML,
    )


# Register
utils.vocabs.register(OrganismQuantityType)
