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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6a4642d8-516c-4b7f-a413-d1bfa9bf5d82"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/78ed8b0f-453c-4c76-b02c-adb5cb1bef8c"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/369c3d2c-fcf7-4fda-b0b1-3ca10ab4809c"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b50a5896-8561-4b0c-b489-b1ffcc64f2d1"), # real URI
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the percentage coverage of the total area being sampled."
    ),
)

INDIVIDUALS = utils.vocabs.Term(
    labels=("INDIVIDUALS",),
    iri=rdflib.URIRef("http://rs.gbif.org/vocabulary/gbif/quantityType/individuals"), # TODO -> Need real URI
    description=(
        "A measurement type where the quantity of a species in a sample is recorded "
        "as the number of individuals (e.g.per litre, per square metre, per cubic metre, per hour, per day)."
    ),
)

DOMIN_SCALE = utils.vocabs.Term(
    labels=("DOMIN SCALE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/34587ea2-99dd-4362-b5c2-d2f5e567f1fe"), # real URI
    description=("A measurement type where the cover of a species in a sample is recorded using the Domin scale."),
)

BRAUN_BLANQUET_SCALE = utils.vocabs.Term(
    labels=("BRAUN BLANQUET SCALE",),
    iri=utils.rdf.uri("quantityType/braunBlanquetScale", utils.namespaces.EXAMPLE),  # TODO -> Need real URI"
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/bd5262cb-e741-4634-b555-2880fa80d910"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e0831c45-e14a-42e1-9bc0-edb1f6892ce4"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/953a274c-d1ce-4515-8c6a-9e2424ea67eb"), # real URI
    description=(
        "A measurement type where the quantity of a species in a sample is recorded as the biomass in kilograms (kg)."
    ),
)

BIOVOLUME_CUBIC_MICRONS = utils.vocabs.Term(
    labels=(
        "BIOVOLUME CUBIC MICRONS",
        "BIOVOLUME IN CUBIC MICRONS",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/85cf64d9-1ee6-456b-bba2-d24ee4be6812"), # real URI
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
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/e95e5513-3153-4d8e-b64b-846fb60730a2"), # real URI
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
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b633eb85-9f0f-4660-af56-4bdec94dc1c6")
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
