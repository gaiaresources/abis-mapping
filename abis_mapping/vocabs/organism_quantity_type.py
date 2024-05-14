"""Provides organism quantity vocabulary for the package"""

# Local
from abis_mapping import utils

# Third-party
import rdflib

# Terms
PERCENTAGE_OF_SPECIES = utils.vocabs.Term(
    labels=("PERCENTAGEOFSPECIES", "%OFSPECIES", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfSpecies")
)

PERCENTAGE_OF_BIOVOLUME = utils.vocabs.Term(
    labels=("PERCENTAGEOFBIOVOLUME", "%OFBIOVOLUME", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiovolume")
)

PERCENTAGE_OF_BIOMASS = utils.vocabs.Term(
    labels=("PERCENTAGEOFBIOMASS", "%OFBIOMASS", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageOfBiomass"),
)

PERCENTAGE_COVERAGE = utils.vocabs.Term(
    labels=("PERCENTAGECOVERAGE", "%COVERAGE", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/percentageCoverage"),
)

INDIVIDUALS = utils.vocabs.Term(
    labels=("INDIVIDUALS", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/individuals")
)

DOMIN_SCALE = utils.vocabs.Term(
    labels=("DOMINSCALE", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/dominScale"),
)

BRAUN_BLANQUET_SCALE = utils.vocabs.Term(
    labels=("BRAUNBLANQUETSCALE", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/braunBlanquetScale"),
)

BIOMASS_AFDG = utils.vocabs.Term(
    labels=("BIOMASSAFDG", "BIOMASSASHFREEDRYWEIGHTINGRAMS", "BIOMASSASHFREEDRYWEIGHTGRAMS",),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassAFDG"),
)

BIOMASS_G = utils.vocabs.Term(
    labels=("BIOMASSG", "BIOMASSINGRAMS", "BIOMASSGRAMS", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassG"),
)

BIOMASS_KG = utils.vocabs.Term(
    labels=("BIOMASSKG", "BIOMASSINKILOGRAMS", "BIOMASSKILOGRAMS", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biomassKg"),
)

BIOVOLUME_CUBIC_MICRONS = utils.vocabs.Term(
    labels=("BIOVOLUMECUBICMICRONS", "BIOVOLUMEINCUBICMICRONS", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biovolumeCubicMicrons"),
)

BIOVOLUME_ML = utils.vocabs.Term(
    labels=("BIOVOLUMEML", "BIOVOLUMEINMILLILITRES", "BIOVOLUMEMILLILITRES", ),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/biovolumeMl")
)


# Vocab
ORGANISM_QUANTITY_TYPE = utils.vocabs.FlexibleVocabulary(
    vocab_id="ORGANISM_QUANTITY_TYPE",
    definition=rdflib.Literal("A type of organism quantity."),
    base=utils.rdf.uri("bdr-cv/concept/organismQuantityType"),
    scheme=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType"),
    broader=utils.rdf.uri("bdr-cv/concept/organismQuantityType", utils.namespaces.EXAMPLE),
    default=None,  # No default, ommitted if not provided.
    terms=(
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
    ),
)

# Register
utils.vocabs.Vocabulary.register(ORGANISM_QUANTITY_TYPE)
