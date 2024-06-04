"""Provides taxon rank vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
CLASS = utils.vocabs.Term(
    labels=("CLASS", ),
    iri=utils.rdf.uri("class", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Class",
)
CULTIVAR = utils.vocabs.Term(
    labels=("CULTIVAR", ),
    iri=utils.rdf.uri("cultivar", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "The epithet is usually output in single quotes and may contain multiple "
        "words, see ICBN §28. Examples: Taxus baccata 'Variegata', Juniperus "
        "×pfitzeriana 'Wilhelm Pfitzer'; Magnolia 'Elizabeth' (= a hybrid, no species "
        "epithet)."
    ),
)
CULTIVARGROUP = utils.vocabs.Term(
    labels=("CULTIVAR GROUP", "GREX", ),
    iri=utils.rdf.uri("cultivargroup", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Cultivar group",
)
FAMILY = utils.vocabs.Term(
    labels=("FAMILY", ),
    iri=utils.rdf.uri("family", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Family",
)
FORM = utils.vocabs.Term(
    labels=("FORM", "FORMA", ),
    iri=utils.rdf.uri("form", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Form",
)
GENUS = utils.vocabs.Term(
    labels=("GENUS", ),
    iri=utils.rdf.uri("genus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Genus",
)
INFORMAL = utils.vocabs.Term(
    labels=("INFORMAL", ),
    iri=utils.rdf.uri("informal", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Informal",
)
INFRAGENERICNAME = utils.vocabs.Term(
    labels=("INFRAGENERIC NAME", ),
    iri=utils.rdf.uri("infragenericname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Used for any other unspecific rank below genera and above species.",
)
INFRAORDER = utils.vocabs.Term(
    labels=("INFRAORDER", ),
    iri=utils.rdf.uri("infraorder", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Infraorder",
)
INFRASPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASPECIFIC NAME", ),
    iri=utils.rdf.uri("infraspecificname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Used for any other unspecific rank below genera and above species.",
)
INFRASUBSPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASUBSPECIFIC NAME", ),
    iri=utils.rdf.uri("infrasubspecificname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Used for any other unspecific rank below subspecies.",
)
KINGDOM = utils.vocabs.Term(
    labels=("KINGDOM", "REGNUM", ),
    iri=utils.rdf.uri("kingdom", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Kingdom",
)
ORDER = utils.vocabs.Term(
    labels=("ORDER", "ALLIANCE", ),
    iri=utils.rdf.uri("order", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Order",
)
PHYLUM = utils.vocabs.Term(
    labels=("PHYLUM", "DIVISION", ),
    iri=utils.rdf.uri("phylum", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Phylum",
)
SECTION = utils.vocabs.Term(
    labels=("SECTION", ),
    iri=utils.rdf.uri("section", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "Section within a genus. In Zoology a section sometimes refers to a group "
        "above family level, this is NOT meant"
    ),
)
SERIES = utils.vocabs.Term(
    labels=("SERIES", ),
    iri=utils.rdf.uri("series", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Series within a genus."
)
SPECIES = utils.vocabs.Term(
    labels=("SPECIES", ),
    iri=utils.rdf.uri("species", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Species",
)
SPECIESAGGREGATE = utils.vocabs.Term(
    labels=("SPECIES AGGREGATE", "AGGREGATE", "SPECIES GROUP", "SPECIES COMPLEX", ),
    iri=utils.rdf.uri("speciesaggregate", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A loosely defined group of species. Zoology: 'Aggregate - a group of "
        "species, other than a subgenus, within a genus. An aggregate may be "
        "denoted by a group name interpolated in parentheses.' -- The "
        "Berlin/MoreTax model notes:'[these] aren't taxonomic ranks but "
        "circumscriptions because on the one hand they are necessary for the "
        "concatenation of the fullname and on the other hand they are necessary "
        "for distinguishing the aggregate or species group from the microspecies.' "
        "Compare subspecific aggregate for a group of subspecies within a "
        "species."
    ),
)
SUBFAMILY = utils.vocabs.Term(
    labels=("SUBFAMILY", ),
    iri=utils.rdf.uri("subfamily", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subfamily",
)
SUBFORM = utils.vocabs.Term(
    labels=("SUBFORM", "SUBFORMA", ),
    iri=utils.rdf.uri("subform", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subform",
)
SUBGENUS = utils.vocabs.Term(
    labels=("SUBGENUS", ),
    iri=utils.rdf.uri("subgenus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subgenus",
)
SUBKINGDOM = utils.vocabs.Term(
    labels=("SUBKINGDOM", ),
    iri=utils.rdf.uri("subkingdom", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subkingdom",
)
SUBORDER = utils.vocabs.Term(
    labels=("SUBORDER", ),
    iri=utils.rdf.uri("suborder", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Suborder",
)
SUBSECTION = utils.vocabs.Term(
    labels=("SUBSECTION", ),
    iri=utils.rdf.uri("subsection", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subsection within a genus.",
)
SUBSERIES = utils.vocabs.Term(
    labels=("SUBSERIES", ),
    iri=utils.rdf.uri("subseries", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subseries within a genus.",
)
SUBSPECIES = utils.vocabs.Term(
    labels=("SUBSPECIES", ),
    iri=utils.rdf.uri("subspecies", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subspecies",
)
SUBSPECIFICAGGREGATE = utils.vocabs.Term(
    labels=("SUBSPECIFIC AGGREGATE", ),
    iri=utils.rdf.uri("subspecificaggregate", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A loosely defined group of subspecies. Zoology:'Aggregate - a group of "
        "subspecies within a species. An aggregate may be denoted by a group "
        "name interpolated in parentheses.'"
    ),
)
SUBTRIBE = utils.vocabs.Term(
    labels=("SUBTRIBE", ),
    iri=utils.rdf.uri("subtribe", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subtribe",
)
SUBVARIETY = utils.vocabs.Term(
    labels=("SUBVARIETY", "SUBVARIETAS", ),
    iri=utils.rdf.uri("subvariety", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subvariety",
)
SUPERFAMILY = utils.vocabs.Term(
    labels=("SUPERFAMILY", ),
    iri=utils.rdf.uri("superfamily", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Superfamily",
)
SUPRAGENERICNAME = utils.vocabs.Term(
    labels=("SUPRAGENERIC NAME", ),
    iri=utils.rdf.uri("supragenericname", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Used for any other unspecific rank above genera."
)
TRIBE = utils.vocabs.Term(
    labels=("TRIBE", ),
    iri=utils.rdf.uri("tribe", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Tribe",
)
UNRANKED = utils.vocabs.Term(
    labels=("UNRANKED", ),
    iri=utils.rdf.uri("unranked", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Unranked",
)
VARIETY = utils.vocabs.Term(
    labels=("VARIETY", "VARIETAS", ),
    iri=utils.rdf.uri("variety", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Variety",
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
