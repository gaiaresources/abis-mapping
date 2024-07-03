"""Provides life stage vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ADULT = utils.vocabs.Term(
    labels=("ADULT", "IMAGO", ),
    iri=utils.rdf.uri("lifeStage/adult", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "An adult is a plant, animal, or person who has reached full growth or "
        "alternatively is capable of reproduction."
    ),
)
EMBRYO = utils.vocabs.Term(
    labels=("EMBRYO", "EGG", "SEED", ),
    iri=utils.rdf.uri("lifeStage/embryo", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "An embryo is a multicellular diploid eukaryote in its earliest stage of "
        "development, from the time of first cell division until birth, hatching, or "
        "germination."
    ),
)
GAMETE = utils.vocabs.Term(
    labels=("GAMETE", "OVUM", "SPERM", "POLLEN", ),
    iri=utils.rdf.uri("lifeStage/gamete", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A gamete is a cell that fuses with another gamete during fertilisation in "
        "organisms that reproduce sexually. In species that produce two "
        "morphologically distinct types of gametes, and in which each individual "
        "produces only one type, a female is any individual that produces the "
        "larger type of gamete — called an ovum (or egg) — and a male produces "
        "the smaller tadpole-like type — called a sperm. This is an example of "
        "anisogamy or heterogamy, the condition wherein females and males "
        "produce gametes of different sizes. In contrast, isogamy is the state of "
        "gametes from both sexes being the same size and shape, and given "
        "arbitrary designators for mating type. Gametes carry half the genetic "
        "information of an individual, one chromosome of each type."
    ),
)
GAMETOPHYTE = utils.vocabs.Term(
    labels=("GAMETOPHYTE", "GAMONT", "PROTONEMA", "POLLEN", "OVULE", ),
    iri=utils.rdf.uri("lifeStage/gametophyte", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "In plants and algae that undergo alternation of generations, a "
        "gametophyte is the multicellular structure, or phase, that is haploid, "
        "containing a single set of chromosomes. The gametophyte produces male "
        "or female gametes (or both), by a process of cell division called mitosis. In "
        "mosses, liverworts and hornworts (bryophytes), the gametophyte is the "
        "commonly known phase of the plant. An early developmental stage in the "
        "gametophyte of mosses (immediately following germination of the "
        "meiospore) is called the protonema. In most other land plants the "
        "gametophyte is very small (as in ferns and their relatives) or even "
        "reduced as in flowering plants (angiosperms), where the female "
        "gametophyte (ovule) is known as a megagametophyte and the male "
        "gametophyte (pollen) is called a microgametophyte."
    ),
)
JUVENILE = utils.vocabs.Term(
    labels=(
        "JUVENILE",
        "SEEDLING",
        "EFT",
        "CALF",
        "HATCHLING",
        "INFANT",
        "FOAL",
        "KITTEN",
        "KIT",
        "CHICK",
        "NYMPH",
        "FAWN",
        "WHELP",
        "PUP",
        "ELVER",
        "FRY",
    ),
    iri=utils.rdf.uri("lifeStage/juvenile", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A juvenile is an individual organism that has not yet reached its adult "
        "form, sexual maturity or size. Juveniles sometimes look very different "
        "from the adult form, particularly in terms of their colour. In many "
        "organisms the juvenile has a different name from the adult."
    ),
)
LARVA = utils.vocabs.Term(
    labels=(
        "LARVA",
        "LARVAE",
        "TADPOLE",
        "POLLIWOG",
        "POLLYWOG",
        "POLLIWIG",
        "POLEWIG",
        "POLWIG",
        "PLANULA",
        "NAUPLIUS",
        "ZOEA",
        "NYMPH",
        "CATERPILLAR",
    ),
    iri=utils.rdf.uri("lifeStage/larva", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A larva (Latin; plural larvae) is a young (juvenile) form of animal with "
        "indirect development, going through or undergoing metamorphosis (for "
        "example, insects, amphibians, or cnidarians). The larva can look "
        "completely different from the adult form, for example, a caterpillar differs "
        "from a butterfly. Larvae often have special (larval) organs which do not "
        "occur in the adult form. The larvae of some species can become "
        "pubescent and not further develop into the adult form (for example, in "
        "some newts). This is a type of neoteny. It is a misunderstanding that the "
        "larval form always reflects the group's evolutionary history. It could be the "
        "case, but often the larval stage has evolved secondarily, as in insects. In "
        "these cases the larval form might differ more from the group's common "
        "origin than the adult form. The early life stages of most fish species are "
        "considerably different from juveniles and adults of their species and are "
        "called larvae."
    )
)
PUPA = utils.vocabs.Term(
    labels=("PUPA", "PUPPE", ),
    iri=utils.rdf.uri("lifeStage/pupa", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A pupa is the life stage of some insects undergoing transformation "
        "between immature and mature stages. The pupal stage is found only in "
        "holometabolous insects, those that undergo a complete metamorphosis, "
        "with four life stages: egg (-> embryo), larva, pupa, and imago (-> adult)."
    ),
)
SPORE = utils.vocabs.Term(
    labels=("SPORE", ),
    iri=utils.rdf.uri("lifeStage/spore", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A spore is a reproductive structure that is adapted for dispersal and "
        "surviving for extended periods of time in unfavorable conditions. Spores "
        "form part of the life cycles of many bacteria, plants, algae, fungi and some "
        "protozoans. A chief difference between spores and seeds as dispersal "
        "units is that spores have very little stored food resources compared with "
        "seeds. Spores are usually haploid and unicellular and are produced by "
        "meiosis in the sporangium by the sporophyte. Once conditions are "
        "favorable, the spore can develop into a new organism using mitotic "
        "division, producing a multicellular gametophyte, which eventually goes on "
        "to produce gametes. Many ferns, especially those adapted to dry "
        "conditions, produce diploid spores. In this case spores are the units of "
        "asexual reproduction, because a single spore develops into a new "
        "organism. By contrast, gametes are the units of sexual reproduction, as "
        "two gametes need to fuse to create a new organism."
    ),
)
SPOROPHYTE = utils.vocabs.Term(
    labels=("SPOROPHYTE", "AGAMONT", ),
    iri=utils.rdf.uri("lifeStage/sporophyte", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "All land plants, and some algae, have life cycles in which a haploid "
        "gametophyte generation alternates with a diploid sporophyte, the "
        "generation of a plant or alga that has a double set of chromosomes. A "
        "multicellular sporophyte generation or phase is present in the life cycle of "
        "all land plants and in some green algae. For common flowering plants "
        "(Angiosperms), the sporophyte generation comprises almost their whole "
        "life cycle (that is whole green plant, roots etc), except phases of small "
        "reproductive structures (pollen and ovule)."
    ),
)
ZYGOTE = utils.vocabs.Term(
    labels=("ZYGOTE", "BLASTOMERE", ),
    iri=utils.rdf.uri("lifeStage/zygote", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    description=(
        "A zygote (or zygocyte) describes the first stage of a new unique organism blastomere "
        "when it consists of just a single cell. The term is also used more loosely to "
        "refer to the group of cells formed by the first few cell divisions, although "
        "this is properly referred to as a blastomere. A zygote is usually produced "
        "by a fertilisation event between two haploid cells - an ovum from a female "
        "and a sperm cell from a male - which combine to form the single diploid "
        "cell. Thus the zygote contains DNA originating from both mother and "
        "father and this provides all the genetic information necessary to form a "
        "new individual"
    ),
)


# Vocabulary
class LifeStage(utils.vocabs.FlexibleVocabulary):
    vocab_id = "LIFE_STAGE"
    definition = rdflib.Literal("A type of lifeStage.")
    base = utils.rdf.uri("bdr-cv/parameter/lifeStage/")
    scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = utils.rdf.uri("bdr-cv/parameter/lifeStage", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
    default = None  # No default, omitted if not provided
    terms = (
        ADULT,
        EMBRYO,
        GAMETE,
        GAMETOPHYTE,
        JUVENILE,
        LARVA,
        PUPA,
        SPORE,
        SPOROPHYTE,
        ZYGOTE,
    )


# Register
utils.vocabs.Vocabulary.register(LifeStage)
