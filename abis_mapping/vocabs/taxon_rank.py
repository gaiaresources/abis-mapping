"""Provides taxon rank vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
CLASS = utils.vocabs.Term(
    labels=("CLASS", ),
    iri=utils.rdf.uri("class", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
CULTIVAR = utils.vocabs.Term(
    labels=("CULTIVAR", ),
    iri=utils.rdf.uri("cultivar", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
CULTIVARGROUP = utils.vocabs.Term(
    labels=("CULTIVAR GROUP", ),
    iri=utils.rdf.uri("cultivargroup", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
FAMILY = utils.vocabs.Term(
    labels=("FAMILY", ),
    iri=utils.rdf.uri("family", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
FORM = utils.vocabs.Term(
    labels=("FORM", ),
    iri=utils.rdf.uri("form", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
GENUS = utils.vocabs.Term(
    labels=("GENUS", ),
    iri=utils.rdf.uri("genus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INFORMAL = utils.vocabs.Term(
    labels=("INFORMAL", ),
    iri=utils.rdf.uri("informal", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INFRAGENERICNAME = utils.vocabs.Term(
    labels=("INFRAGENERIC NAME", ),
    iri=utils.rdf.uri("infragenericname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INFRAORDER = utils.vocabs.Term(
    labels=("INFRAORDER", ),
    iri=utils.rdf.uri("infraorder", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INFRASPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASPECIFIC NAME", ),
    iri=utils.rdf.uri("infraspecificname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
INFRASUBSPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASUBSPECIFIC NAME", ),
    iri=utils.rdf.uri("infrasubspecificname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
KINGDOM = utils.vocabs.Term(
    labels=("KINGDOM", ),
    iri=utils.rdf.uri("kingdom", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
ORDER = utils.vocabs.Term(
    labels=("ORDER", ),
    iri=utils.rdf.uri("order", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
PHYLUM = utils.vocabs.Term(
    labels=("PHYLUM", ),
    iri=utils.rdf.uri("phylum", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SECTION = utils.vocabs.Term(
    labels=("SECTION", ),
    iri=utils.rdf.uri("section", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SERIES = utils.vocabs.Term(
    labels=("SERIES", ),
    iri=utils.rdf.uri("series", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIES = utils.vocabs.Term(
    labels=("SPECIES", ),
    iri=utils.rdf.uri("species", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SPECIESAGGREGATE = utils.vocabs.Term(
    labels=("SPECIES AGGREGATE", ),
    iri=utils.rdf.uri("speciesaggregate", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBFAMILY = utils.vocabs.Term(
    labels=("SUBFAMILY", ),
    iri=utils.rdf.uri("subfamily", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBFORM = utils.vocabs.Term(
    labels=("SUBFORM", ),
    iri=utils.rdf.uri("subform", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBGENUS = utils.vocabs.Term(
    labels=("SUBGENUS", ),
    iri=utils.rdf.uri("subgenus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBKINGDOM = utils.vocabs.Term(
    labels=("SUBKINGDOM", ),
    iri=utils.rdf.uri("subkingdom", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBORDER = utils.vocabs.Term(
    labels=("SUBORDER", ),
    iri=utils.rdf.uri("suborder", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBSECTION = utils.vocabs.Term(
    labels=("SUBSECTION", ),
    iri=utils.rdf.uri("subsection", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBSERIES = utils.vocabs.Term(
    labels=("SUBSERIES", ),
    iri=utils.rdf.uri("subseries", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBSPECIES = utils.vocabs.Term(
    labels=("SUBSPECIES", ),
    iri=utils.rdf.uri("subspecies", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBSPECIFICAGGREGATE = utils.vocabs.Term(
    labels=("SUBSPECIFIC AGGREGATE", ),
    iri=utils.rdf.uri("subspecificaggregate", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBTRIBE = utils.vocabs.Term(
    labels=("SUBTRIBE", ),
    iri=utils.rdf.uri("subtribe", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUBVARIETY = utils.vocabs.Term(
    labels=("SUBVARIETY", ),
    iri=utils.rdf.uri("subvariety", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUPERFAMILY = utils.vocabs.Term(
    labels=("SUPERFAMILY", ),
    iri=utils.rdf.uri("superfamily", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
SUPRAGENERICNAME = utils.vocabs.Term(
    labels=("SUPRAGENERIC NAME", ),
    iri=utils.rdf.uri("supragenericname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
TRIBE = utils.vocabs.Term(
    labels=("TRIBE", ),
    iri=utils.rdf.uri("tribe", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
UNRANKED = utils.vocabs.Term(
    labels=("UNRANKED", ),
    iri=utils.rdf.uri("unranked", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)
VARIETY = utils.vocabs.Term(
    labels=("VARIETY", ),
    iri=utils.rdf.uri("variety", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
)

# Vocabulary
TAXON_RANK = utils.vocabs.FlexibleVocabulary(
    vocab_id="TAXON_RANK",
    definition=rdflib.Literal("A type of taxonRank."),
    base=utils.rdf.uri("bdr-cv/attribute/taxonRank/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=utils.rdf.uri("bdr-cv/attribute/taxonRank", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(
        CLASS,
        CULTIVAR,
        CULTIVARGROUP,
        FAMILY,
        FORM,
        GENUS,
        INFORMAL,
        INFRAGENERICNAME,
        INFRAORDER,
        INFRASPECIFICNAME,
        INFRASUBSPECIFICNAME,
        KINGDOM,
        ORDER,
        PHYLUM,
        SECTION,
        SERIES,
        SPECIES,
        SPECIESAGGREGATE,
        SUBFAMILY,
        SUBFORM,
        SUBGENUS,
        SUBKINGDOM,
        SUBORDER,
        SUBSECTION,
        SUBSERIES,
        SUBSPECIES,
        SUBSPECIFICAGGREGATE,
        SUBTRIBE,
        SUBVARIETY,
        SUPERFAMILY,
        SUPRAGENERICNAME,
        TRIBE,
        UNRANKED,
        VARIETY,
    )
)

# Register
utils.vocabs.Vocabulary.register(TAXON_RANK)
