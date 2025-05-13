"""Provides taxon rank vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
CLASS = utils.vocabs.Term(
    labels=("CLASS",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/db985a35-6edb-4ba1-8939-b0a7b1efa287"), # real URI
    description="Class",
)
CULTIVAR = utils.vocabs.Term(
    labels=("CULTIVAR",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/892fed0b-70cc-48d4-ac3f-0b0b495cc0c0"), # real URI
    description=(
        "The epithet is usually output in single quotes and may contain multiple "
        "words, see ICBN §28. Examples: Taxus baccata 'Variegata', Juniperus "
        "×pfitzeriana 'Wilhelm Pfitzer'; Magnolia 'Elizabeth' (= a hybrid, no species "
        "epithet)."
    ),
)
CULTIVARGROUP = utils.vocabs.Term(
    labels=(
        "CULTIVAR GROUP",
        "GREX",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45d214c6-894b-4fe5-a9ce-2db3a1fc3a7d"), # real URI
    description="Cultivar group",
)
FAMILY = utils.vocabs.Term(
    labels=("FAMILY",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/f2e2f14f-56d4-4d2f-9a37-7e140133cbd2"), # real URI
    description="Family",
)
FORM = utils.vocabs.Term(
    labels=(
        "FORM",
        "FORMA",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dae4d56e-7440-4ddd-90e7-9924b455ca40"), # real URI
    description="Form",
)
GENUS = utils.vocabs.Term(
    labels=("GENUS",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5fb9982c-8249-4d58-9f38-659e8c7c6daf"), # real URI
    description="Genus",
)
INFORMAL = utils.vocabs.Term(
    labels=("INFORMAL",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d43fd16c-73c3-4578-a359-7168a0876aaf"), # real URI
    description="Informal",
)
INFRAGENERICNAME = utils.vocabs.Term(
    labels=("INFRAGENERIC NAME",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/8d227e73-f906-4d5f-9f15-8ae8bf29b2ce"), # real URI
    description="Used for any other unspecific rank below genera and above species.",
)
INFRAORDER = utils.vocabs.Term(
    labels=("INFRAORDER",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b49af045-88c2-44c0-ad34-901d1ff46d7a"), # real URI
    description="Infraorder",
)
INFRASPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASPECIFIC NAME",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/445b6830-8e31-4fab-889b-f18f88f382c0"), # real URI
    description="Used for any other unspecific rank below genera and above species.",
)
INFRASUBSPECIFICNAME = utils.vocabs.Term(
    labels=("INFRASUBSPECIFIC NAME",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b06ee648-55e2-435f-b453-2f6639addbcb"), # real URI
    description="Used for any other unspecific rank below subspecies.",
)
KINGDOM = utils.vocabs.Term(
    labels=(
        "KINGDOM",
        "REGNUM",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a27dc8c9-25ed-4a82-b797-b9dd0add6da2"), # real URI
    description="Kingdom",
)
ORDER = utils.vocabs.Term(
    labels=(
        "ORDER",
        "ALLIANCE",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6605eecb-e8ba-47fc-a364-81aa3ba5ce69"), # real URI
    description="Order",
)
PHYLUM = utils.vocabs.Term(
    labels=(
        "PHYLUM",
        "DIVISION",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/3ade9854-d90f-4709-bb5a-260d62a2c647"), # real URI
    description="Phylum",
)
SECTION = utils.vocabs.Term(
    labels=("SECTION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/22829f2d-461d-4cf6-acbc-5b8f7d2d9c77"), # real URI
    description=(
        "Section within a genus. In Zoology a section sometimes refers to a group above family level, this is NOT meant"
    ),
)
SERIES = utils.vocabs.Term(
    labels=("SERIES",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/d3f48baa-7a29-4b4f-9d92-bb5276ab8710"), # real URI
    description="Series within a genus.",
)
SPECIES = utils.vocabs.Term(
    labels=("SPECIES",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2b6fae57-f28e-4f24-b6f9-19f114dbb61e"), # real URI
    description="Species",
)
SPECIESAGGREGATE = utils.vocabs.Term(
    labels=(
        "SPECIES AGGREGATE",
        "AGGREGATE",
        "SPECIES GROUP",
        "SPECIES COMPLEX",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/bc6b552f-5ab0-4d46-a236-a99fc2005c93"), # real URI
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
    labels=("SUBFAMILY",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/49849796-fc73-444f-a375-32fc0048a18b"), # real URI
    description="Subfamily",
)
SUBFORM = utils.vocabs.Term(
    labels=(
        "SUBFORM",
        "SUBFORMA",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/9eeb2dcf-ec0c-4541-a409-28722e9b4f26"), # real URI
    description="Subform",
)
SUBGENUS = utils.vocabs.Term(
    labels=("SUBGENUS",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/86a64fd0-7aa6-4ef1-93cc-45ae722ec6a7"), # real URI
    description="Subgenus",
)
SUBKINGDOM = utils.vocabs.Term(
    labels=("SUBKINGDOM",),
    iri=utils.rdf.uri("subkingdom", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description="Subkingdom",
)
SUBORDER = utils.vocabs.Term(
    labels=("SUBORDER",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a68fa217-969b-48ea-a08a-bb7618079edb"), # real URI
    description="Suborder",
)
SUBSECTION = utils.vocabs.Term(
    labels=("SUBSECTION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/367a27ee-7c6f-48a0-ba50-ff137ed1fe0c"), # real URI
    description="Subsection within a genus.",
)
SUBSERIES = utils.vocabs.Term(
    labels=("SUBSERIES",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/61a34b22-555e-431d-848c-95bb6a364a9a"), # real URI
    description="Subseries within a genus.",
)
SUBSPECIES = utils.vocabs.Term(
    labels=("SUBSPECIES",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/7abb3e62-ec02-4b7d-b057-e4380d66dd72"), # real URI
    description="Subspecies",
)
SUBSPECIFICAGGREGATE = utils.vocabs.Term(
    labels=("SUBSPECIFIC AGGREGATE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fdbe211f-33d6-4446-a1fb-5eb8de45dd57"), # real URI
    description=(
        "A loosely defined group of subspecies. Zoology:'Aggregate - a group of "
        "subspecies within a species. An aggregate may be denoted by a group "
        "name interpolated in parentheses.'"
    ),
)
SUBTRIBE = utils.vocabs.Term(
    labels=("SUBTRIBE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/baefb9ce-5f98-44a7-acc3-5bd1247c8d54"), # real URI
    description="Subtribe",
)
SUBVARIETY = utils.vocabs.Term(
    labels=(
        "SUBVARIETY",
        "SUBVARIETAS",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/cb2627f0-e121-474b-a354-dd0e392daa84"), # real URI
    description="Subvariety",
)
SUPERFAMILY = utils.vocabs.Term(
    labels=("SUPERFAMILY",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/50d96a8d-aa2a-4629-9caa-76637c619851"), # real URI
    description="Superfamily",
)
SUPRAGENERICNAME = utils.vocabs.Term(
    labels=("SUPRAGENERIC NAME",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/a8889e2e-8eb3-4ed3-8d32-3974adae6158"), # real URI
    description="Used for any other unspecific rank above genera.",
)
TRIBE = utils.vocabs.Term(
    labels=("TRIBE",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/40d5f3d3-dfbb-4718-9f66-29b5f735142f"), # real URI
    description="Tribe",
)
UNRANKED = utils.vocabs.Term(
    labels=("UNRANKED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6e50f0de-0847-4db3-8bc3-f7e796ed32bf"), # real URI
    description="Unranked",
)
VARIETY = utils.vocabs.Term(
    labels=(
        "VARIETY",
        "VARIETAS",
    ),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/6fa4ff0a-acc8-482b-a574-0ffbbab83ca5"), # real URI
    description="Variety",
)


# Vocabulary
class TaxonRank(utils.vocabs.FlexibleVocabulary):
    vocab_id = "TAXON_RANK"
    definition = rdflib.Literal("A type of taxonRank.")
    base = "bdr-cv/attribute/taxonRank/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924")
    broader = iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/1e4d7110-5f07-45ec-98e7-738236a8d8e0")
    default = None  # No default, ommitted if not provided
    terms = (
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


# Register
utils.vocabs.register(TaxonRank)
