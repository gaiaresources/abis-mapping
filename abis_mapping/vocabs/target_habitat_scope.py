"""Provides target habitat scope vocabulary for the package."""

# Third-party
import rdflib

# Local
from abis_mapping import utils


BEACH = utils.vocabs.Term(
    labels=("BEACH",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/63960cfe-9e04-52b7-8940-4d6c2ebe0a02"),
)

BILLABONG_OR_SWAMP = utils.vocabs.Term(
    labels=("BILLABONG OR SWAMP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/55f988ef-b922-5ae6-a23e-748aefd62d21"),
)

CAVE = utils.vocabs.Term(
    labels=("CAVE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/03ee0064-f289-52ae-91a8-ed0aace9a1f2"),
)

CHENOPOD_SHRUBLAND = utils.vocabs.Term(
    labels=("CHENOPOD SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/99807739-a552-5004-9105-6e580a123002"),
)

CLOSED_CHENOPOD_SHRUBLAND = utils.vocabs.Term(
    labels=("CLOSED CHENOPOD SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7cf0b84b-3277-5bfd-9fd0-0a799cda4588"),
)

CLOSED_FERNLAND = utils.vocabs.Term(
    labels=("CLOSED FERNLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/77dc385f-c9a0-56f3-b14e-4485f7adcb78"),
)

CLOSED_FORBLAND = utils.vocabs.Term(
    labels=("CLOSED FORBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7a9329ca-a03d-5c22-9c3c-3ca03d038fb9"),
)

CLOSED_FOREST = utils.vocabs.Term(
    labels=("CLOSED FOREST",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/ac2238c8-b7bc-5a89-8cc3-774bc3a53064"),
)

CLOSED_HEATHLAND = utils.vocabs.Term(
    labels=("CLOSED HEATHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c1781447-eaa9-534a-8d3a-4935cc0ab29e"),
)

CLOSED_HUMMOCK_GRASSLAND = utils.vocabs.Term(
    labels=("CLOSED HUMMOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/5a0039b6-1652-59cf-95ba-0ea41b7626e8"),
)

CLOSED_LICHENLAND = utils.vocabs.Term(
    labels=("CLOSED LICHENLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/936bf21a-191e-50c2-a767-695931abefeb"),
)

CLOSED_LIVERWORTLAND = utils.vocabs.Term(
    labels=("CLOSED LIVERWORTLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b190259a-9301-55bd-bf66-07d98a0d9af6"),
)

CLOSED_MALLEE_FOREST = utils.vocabs.Term(
    labels=("CLOSED MALLEE FOREST",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/36a6499f-b1f6-5405-a2ec-73498ac874eb"),
)

CLOSED_MALLEE_SHRUBLAND = utils.vocabs.Term(
    labels=("CLOSED MALLEE SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c751ff0d-e9a4-5a3d-bf46-27fbb352a1e4"),
)

CLOSED_MOSSLAND = utils.vocabs.Term(
    labels=("CLOSED MOSSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/44f77309-6690-5e04-a873-7418632d1420"),
)

CLOSED_RUSHLAND = utils.vocabs.Term(
    labels=("CLOSED RUSHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/230bb275-6421-539b-9852-07a5f76c660f"),
)

CLOSED_SEDGELAND = utils.vocabs.Term(
    labels=("CLOSED SEDGELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/193d73c9-b3e8-59b5-860e-109eae4efd16"),
)

CLOSED_SHRUBLAND = utils.vocabs.Term(
    labels=("CLOSED SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/97fa02b0-f5c2-5cae-a822-aa0385e299b7"),
)

CLOSED_SOD_GRASSLAND = utils.vocabs.Term(
    labels=("CLOSED SOD GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/18d6c67c-5a1e-5146-a49a-a17615eb6656"),
)

CLOSED_TUSSOCK_GRASSLAND = utils.vocabs.Term(
    labels=("CLOSED TUSSOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/2879f1a4-9a89-5faa-b43c-ae04aeeb9d23"),
)

CLOSED_VINELAND = utils.vocabs.Term(
    labels=("CLOSED VINELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/49b4614a-b1ad-5ba3-8157-f884b61d09c5"),
)

COASTAL_WATERS = utils.vocabs.Term(
    labels=("COASTAL WATERS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/09b57b74-ee2d-5270-8e32-4368989eac08"),
)

CROP_LAND = utils.vocabs.Term(
    labels=("CROP LAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c742f5dd-15e7-5212-8304-a34a46b93d78"),
)

ESTUARY = utils.vocabs.Term(
    labels=("ESTUARY",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7cb2f197-c3e8-5491-b0db-78b839405fd7"),
)

FERNLAND = utils.vocabs.Term(
    labels=("FERNLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/87e02dde-35a9-5ee3-b919-5bd34d83a2ff"),
)

FORBLAND = utils.vocabs.Term(
    labels=("FORBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/6f68413c-4dcd-5d02-a0c7-0ad3a56d62d3"),
)

FRESHWATER_LAKE = utils.vocabs.Term(
    labels=("FRESHWATER LAKE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9f69fdbd-4d86-5116-8822-8c79ee64702e"),
)

GRAZING_LAND = utils.vocabs.Term(
    labels=("GRAZING LAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4f1acfe6-f8bc-5318-ba80-d40402109504"),
)

HEATHLAND = utils.vocabs.Term(
    labels=("HEATHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/517d2f98-9d24-5b68-b8d8-f5393eba310a"),
)

HUMMOCK_GRASSLAND = utils.vocabs.Term(
    labels=("HUMMOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b77c7b89-0dd2-52cb-9eb3-7319d4465cfe"),
)

ISOLATED_CHENOPOD_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED CHENOPOD SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9435f240-8da8-5b84-83fa-ffdd0692c6dc"),
)

ISOLATED_CLUMP_OF_CHENOPOD_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF CHENOPOD SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/1928d26f-10b6-5a61-84cb-feac377781b0"),
)

ISOLATED_CLUMP_OF_HEATH_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF HEATH SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e1dd0210-be1b-548e-aa4b-5567d973a9f5"),
)

ISOLATED_CLUMP_OF_HUMMOCK_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF HUMMOCK GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f62e2bf1-408f-536e-9da1-82d7e980498c"),
)

ISOLATED_CLUMP_OF_LIVERWORTS = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF LIVERWORTS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/2aad6ae5-d64f-55b7-a394-a90394c30d29"),
)

ISOLATED_CLUMP_OF_MALLEE_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF MALLEE SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d2f7baae-9238-5978-972c-179fa11e39ad"),
)

ISOLATED_CLUMP_OF_MALLEE_TREES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF MALLEE TREES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/541a8566-33f2-5998-af10-c89046b17a1c"),
)

ISOLATED_CLUMP_OF_MOSSES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF MOSSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4f1dc06e-910b-50a9-890a-d8d7ba3665b9"),
)

ISOLATED_CLUMP_OF_RUSHES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF RUSHES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9a309ff4-8499-5bf4-92cc-8d394a53e6b9"),
)

ISOLATED_CLUMP_OF_SEDGES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF SEDGES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/032937cf-f227-570d-a20d-9e2e04c27be8"),
)

ISOLATED_CLUMP_OF_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3d57e6c5-e288-56c2-89c3-1d1f8abd5847"),
)

ISOLATED_CLUMP_OF_SOD_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF SOD GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f2c496b6-ea23-546b-83f2-14ebb6f5ca82"),
)

ISOLATED_CLUMP_OF_TREES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF TREES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7e8f9627-8796-5e1e-ad72-33f2a863de98"),
)

ISOLATED_CLUMP_OF_TUSSOCK_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF TUSSOCK GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f51c20dd-6026-5b24-9f5f-a705b8d88a95"),
)

ISOLATED_CLUMP_OF_VINES = utils.vocabs.Term(
    labels=("ISOLATED CLUMP OF VINES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f8c0c37c-3021-5f90-bb23-658966b5326d"),
)

ISOLATED_CLUMPS_OF_FERNS = utils.vocabs.Term(
    labels=("ISOLATED CLUMPS OF FERNS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e692ff93-02cd-5bdf-bc4e-8f76de59089a"),
)

ISOLATED_CLUMPS_OF_FORBS = utils.vocabs.Term(
    labels=("ISOLATED CLUMPS OF FORBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/37b756c2-5607-58de-a31b-eb5b1ce626ed"),
)

ISOLATED_CLUP_OF_LICHENS = utils.vocabs.Term(
    labels=("ISOLATED CLUP OF LICHENS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f5a80ba0-7b0b-51ee-bfd3-8e96199e8298"),
)

ISOLATED_FERNS = utils.vocabs.Term(
    labels=("ISOLATED FERNS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/aa9b68be-a749-537e-baf9-6880088198cc"),
)

ISOLATED_FORBS = utils.vocabs.Term(
    labels=("ISOLATED FORBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f03afa59-394c-50e6-ba58-3b7dc38a1363"),
)

ISOLATED_HEATH_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED HEATH SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/824bdcd9-2c63-5a01-9c14-d38479118daa"),
)

ISOLATED_HUMMOCK_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED HUMMOCK GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/a137d32b-5133-52f0-a127-ab64ad4e9331"),
)

ISOLATED_LICHENS = utils.vocabs.Term(
    labels=("ISOLATED LICHENS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/69a2aa31-2a87-5306-87e0-baa53745032b"),
)

ISOLATED_LIVERWORTS = utils.vocabs.Term(
    labels=("ISOLATED LIVERWORTS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d228dc9f-9e51-567b-8fde-f3bac5f57265"),
)

ISOLATED_MALLEE_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED MALLEE SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/02056871-964d-5bc5-b5eb-dcd4c761f0ff"),
)

ISOLATED_MALLEE_TREES = utils.vocabs.Term(
    labels=("ISOLATED MALLEE TREES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8c26e6d6-6287-5139-89c3-03c730b544e0"),
)

ISOLATED_MOSSES = utils.vocabs.Term(
    labels=("ISOLATED MOSSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3f630070-deb6-596f-92ac-9906008d0f07"),
)

ISOLATED_RUSHES = utils.vocabs.Term(
    labels=("ISOLATED RUSHES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3a1e4a07-df4a-5a18-9f61-72f7c87306f5"),
)

ISOLATED_SEDGES = utils.vocabs.Term(
    labels=("ISOLATED SEDGES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/150a361f-0b85-59da-93d0-65206b6eae9e"),
)

ISOLATED_SHRUBS = utils.vocabs.Term(
    labels=("ISOLATED SHRUBS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/97d1820d-545f-5694-b379-9f360b8d123b"),
)

ISOLATED_SOD_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED SOD GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/cf2c27f3-1f44-50cc-a382-4a18c5c24985"),
)

ISOLATED_TREES = utils.vocabs.Term(
    labels=("ISOLATED TREES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9935b7bc-2bfa-5b34-ae38-12da54c24bbc"),
)

ISOLATED_TUSSOCK_GRASSES = utils.vocabs.Term(
    labels=("ISOLATED TUSSOCK GRASSES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d958b180-ff63-56c5-a39a-4d04bd07207b"),
)

ISOLATED_VINES = utils.vocabs.Term(
    labels=("ISOLATED VINES",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d42312a8-1e09-5dc4-ae32-df980671e7d7"),
)

LICHENLAND = utils.vocabs.Term(
    labels=("LICHENLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/700fd743-4b00-59cf-87fd-a2bb56d93002"),
)

LIVERWORTLAND = utils.vocabs.Term(
    labels=("LIVERWORTLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/1ad6b767-f8f0-51ed-8430-50819e0ad899"),
)

MALLEE_SHRUBLAND = utils.vocabs.Term(
    labels=("MALLEE SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f5e68c19-0e4c-5aa9-8076-7879f2a6cce4"),
)

MALLEE_WOODLAND = utils.vocabs.Term(
    labels=("MALLEE WOODLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3de3bfd1-7d1c-5656-8439-85f56f487c40"),
)

MOSSLAND = utils.vocabs.Term(
    labels=("MOSSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9ad6291c-900f-5538-af2d-6e241b0264ba"),
)

MUDFLAT = utils.vocabs.Term(
    labels=("MUDFLAT",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3e8b4e76-de24-557c-93c0-a71219a0931b"),
)

OPEN_OCEAN = utils.vocabs.Term(
    labels=("OPEN OCEAN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b17ea99e-d037-5f41-adc1-1323fe3fbdce"),
)

OPEN_CHENOPOD_SHRUBLAND = utils.vocabs.Term(
    labels=("OPEN CHENOPOD SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/740661b3-4178-508a-a7a4-64f07c6c3a8a"),
)

OPEN_FERNLAND = utils.vocabs.Term(
    labels=("OPEN FERNLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/5deef8a7-e536-57a9-9b7a-caf9f5d4d39d"),
)

OPEN_FORBLAND = utils.vocabs.Term(
    labels=("OPEN FORBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/32532a0a-3b85-5ebd-b72e-2b87666baf62"),
)

OPEN_FOREST = utils.vocabs.Term(
    labels=("OPEN FOREST",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9b644ae5-6279-5794-8535-b56cef440f3d"),
)

OPEN_HEATH = utils.vocabs.Term(
    labels=("OPEN HEATH",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c904cc78-d7f8-5645-9d28-632af88c1d98"),
)

OPEN_HUMMOCK_GRASSLAND = utils.vocabs.Term(
    labels=("OPEN HUMMOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9c0fd421-510f-56f5-92e6-e18ceb62419d"),
)

OPEN_LICHENLAND = utils.vocabs.Term(
    labels=("OPEN LICHENLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/5291eed4-b125-51fc-bf5a-6deff5d3e0d8"),
)

OPEN_LIVERWORTLAND = utils.vocabs.Term(
    labels=("OPEN LIVERWORTLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/30d4c6a6-5558-5fd3-bed3-487c6fd7d015"),
)

OPEN_MALLEE_FOREST = utils.vocabs.Term(
    labels=("OPEN MALLEE FOREST",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3f0f6d0b-e136-5cad-bd74-f229aeb6fe04"),
)

OPEN_MALLEE_SHRUBLAND = utils.vocabs.Term(
    labels=("OPEN MALLEE SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9baa87b2-346a-595c-bcb9-f50a2e7101f2"),
)

OPEN_MALLEE_WOODLAND = utils.vocabs.Term(
    labels=("OPEN MALLEE WOODLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/484d51eb-c1ee-597c-aed0-664a28e7b1d1"),
)

OPEN_MOSSLAND = utils.vocabs.Term(
    labels=("OPEN MOSSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/06328712-eb21-5ed1-8ac3-91d4e753deff"),
)

OPEN_RUSHLAND = utils.vocabs.Term(
    labels=("OPEN RUSHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4e22f9a2-1bc6-53ba-8226-e18fef762fb9"),
)

OPEN_SEDGELAND = utils.vocabs.Term(
    labels=("OPEN SEDGELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/1f71cccb-10a3-5dad-a1f1-2007c1c670c3"),
)

OPEN_SHRUBLAND = utils.vocabs.Term(
    labels=("OPEN SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c5fb3713-be56-56e3-8fb7-922c27dd2ae9"),
)

OPEN_SOD_GRASSLAND = utils.vocabs.Term(
    labels=("OPEN SOD GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/a0aa9bd3-3256-54f1-a5bf-746b3025743f"),
)

OPEN_TUSSOCK_GRASSLAND = utils.vocabs.Term(
    labels=("OPEN TUSSOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/021ac7e0-af3f-5c5f-9835-6566cd7d45dd"),
)

OPEN_VINELAND = utils.vocabs.Term(
    labels=("OPEN VINELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4bc3fcb1-26c6-5b11-93df-9381fa12282e"),
)

OPEN_WOODLAND = utils.vocabs.Term(
    labels=("OPEN WOODLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/09fdd99f-e627-542c-afed-824af660bf48"),
)

ROCK_OUTCROP = utils.vocabs.Term(
    labels=("ROCK OUTCROP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/dc4aeb3c-5a67-5232-89d3-9ee250cf3cda"),
)

RUSHLAND = utils.vocabs.Term(
    labels=("RUSHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3de9060b-389c-5340-9e1c-288719d05007"),
)

SALTWATER_LAKE = utils.vocabs.Term(
    labels=("SALTWATER LAKE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/1b65f313-89bd-57ac-8506-07cfdc72e757"),
)

SEDGELAND = utils.vocabs.Term(
    labels=("SEDGELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/6e866ca0-1492-5e47-a520-8bac223f2dc8"),
)

SHRUBLAND = utils.vocabs.Term(
    labels=("SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/18e5a444-f39c-50ea-84a5-9f677ee46601"),
)

SOD_GRASSLAND = utils.vocabs.Term(
    labels=("SOD GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/585bbfcc-cb43-5d7a-9a58-1c90031300fd"),
)

SPARSE_CHENOPOD_SHRUBLAND = utils.vocabs.Term(
    labels=("SPARSE CHENOPOD SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c8a4a268-54ef-5327-9530-3acb1c6bb048"),
)

SPARSE_FERNLAND = utils.vocabs.Term(
    labels=("SPARSE FERNLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/30c6a39a-211b-5526-93b3-467bbb9e56b4"),
)

SPARSE_FORBLAND = utils.vocabs.Term(
    labels=("SPARSE FORBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/bff147ed-4af8-50d5-be4e-b2d817686767"),
)

SPARSE_GRASSLAND = utils.vocabs.Term(
    labels=("SPARSE GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e28adc38-5e40-5795-93d1-6582d0013f7e"),
)

SPARSE_HEATH = utils.vocabs.Term(
    labels=("SPARSE HEATH",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8a8ac1b4-3906-58ea-be1f-9bc51c2d17f1"),
)

SPARSE_LICHENLAND = utils.vocabs.Term(
    labels=("SPARSE LICHENLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3a884e64-9ead-5a93-96af-594709e77fd4"),
)

SPARSE_LIVERWORTLAND = utils.vocabs.Term(
    labels=("SPARSE LIVERWORTLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/64c1dc43-cde9-55b4-b1bb-fe58a340e20a"),
)

SPARSE_MALLEE_SHRUBLAND = utils.vocabs.Term(
    labels=("SPARSE MALLEE SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3c2c0ce9-5d47-5e85-952d-1e8584d9d9d0"),
)

SPARSE_MOSSLAND = utils.vocabs.Term(
    labels=("SPARSE MOSSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/dacaf8da-6064-5374-89c5-01606b54d774"),
)

SPARSE_RUSHLAND = utils.vocabs.Term(
    labels=("SPARSE RUSHLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/3c0c31d0-7360-55cd-bd02-5e2a2e47b11b"),
)

SPARSE_SEDGELAND = utils.vocabs.Term(
    labels=("SPARSE SEDGELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/864f2e87-9c4c-59c5-936d-557ac7942996"),
)

SPARSE_SHRUBLAND = utils.vocabs.Term(
    labels=("SPARSE SHRUBLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7ecfb199-be34-5656-887b-c6205faf0cd1"),
)

SPARSE_SOD_GRASSLAND = utils.vocabs.Term(
    labels=("SPARSE SOD GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/a4fccf87-04df-5982-a89f-4aaf6b089777"),
)

SPARSE_TUSSOCK_GRASSLAND = utils.vocabs.Term(
    labels=("SPARSE TUSSOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/eba388b7-bf44-5c65-b468-aebb1afbc5e2"),
)

SPARSE_VINELAND = utils.vocabs.Term(
    labels=("SPARSE VINELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f20b4449-da26-5423-ad11-eeed042e4072"),
)

STREAM_OR_RIVER = utils.vocabs.Term(
    labels=("STREAM OR RIVER",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/353214cb-0cda-55f9-9e5e-e3c0bd8dd07c"),
)

TUSSOCK_GRASSLAND = utils.vocabs.Term(
    labels=("TUSSOCK GRASSLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d474a334-fb65-5496-917c-7f879697157e"),
)

URBAN = utils.vocabs.Term(
    labels=("URBAN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/6fb7d262-c3d5-5b65-baf0-3fd82fa924a7"),
)

VINELAND = utils.vocabs.Term(
    labels=("VINELAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/329d8b4e-fb69-5786-af63-8fc92ec018f7"),
)

WOODLAND = utils.vocabs.Term(
    labels=("WOODLAND",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e2193542-9203-532b-99d3-853a4640114d"),
)

TARGET_HABITAT_SCOPE = utils.vocabs.FlexibleVocabulary(
    vocab_id="TARGET_HABITAT_SCOPE",
    definition=rdflib.Literal("A type of targetHabitatScope"),
    base=utils.rdf.uri("bdr-cv/attribute/targetHabitatScope/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"),
    broader=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c19a0098-1f3f-4bc2-b84d-fdb6d4e24d6f"),
    default=None,
    terms=(
        BEACH,
        BILLABONG_OR_SWAMP,
        CAVE,
        CHENOPOD_SHRUBLAND,
        CLOSED_CHENOPOD_SHRUBLAND,
        CLOSED_FERNLAND,
        CLOSED_FORBLAND,
        CLOSED_FOREST,
        CLOSED_HEATHLAND,
        CLOSED_HUMMOCK_GRASSLAND,
        CLOSED_LICHENLAND,
        CLOSED_LIVERWORTLAND,
        CLOSED_MALLEE_FOREST,
        CLOSED_MALLEE_SHRUBLAND,
        CLOSED_MOSSLAND,
        CLOSED_RUSHLAND,
        CLOSED_SEDGELAND,
        CLOSED_SHRUBLAND,
        CLOSED_SOD_GRASSLAND,
        CLOSED_TUSSOCK_GRASSLAND,
        CLOSED_VINELAND,
        COASTAL_WATERS,
        CROP_LAND,
        ESTUARY,
        FERNLAND,
        FORBLAND,
        FRESHWATER_LAKE,
        GRAZING_LAND,
        HEATHLAND,
        HUMMOCK_GRASSLAND,
        ISOLATED_CHENOPOD_SHRUBS,
        ISOLATED_CLUMP_OF_CHENOPOD_SHRUBS,
        ISOLATED_CLUMP_OF_HEATH_SHRUBS,
        ISOLATED_CLUMP_OF_HUMMOCK_GRASSES,
        ISOLATED_CLUMP_OF_LIVERWORTS,
        ISOLATED_CLUMP_OF_MALLEE_SHRUBS,
        ISOLATED_CLUMP_OF_MALLEE_TREES,
        ISOLATED_CLUMP_OF_MOSSES,
        ISOLATED_CLUMP_OF_RUSHES,
        ISOLATED_CLUMP_OF_SEDGES,
        ISOLATED_CLUMP_OF_SHRUBS,
        ISOLATED_CLUMP_OF_SOD_GRASSES,
        ISOLATED_CLUMP_OF_TREES,
        ISOLATED_CLUMP_OF_TUSSOCK_GRASSES,
        ISOLATED_CLUMP_OF_VINES,
        ISOLATED_CLUMPS_OF_FERNS,
        ISOLATED_CLUMPS_OF_FORBS,
        ISOLATED_CLUP_OF_LICHENS,
        ISOLATED_FERNS,
        ISOLATED_FORBS,
        ISOLATED_HEATH_SHRUBS,
        ISOLATED_HUMMOCK_GRASSES,
        ISOLATED_LICHENS,
        ISOLATED_LIVERWORTS,
        ISOLATED_MALLEE_SHRUBS,
        ISOLATED_MALLEE_TREES,
        ISOLATED_MOSSES,
        ISOLATED_RUSHES,
        ISOLATED_SEDGES,
        ISOLATED_SHRUBS,
        ISOLATED_SOD_GRASSES,
        ISOLATED_TREES,
        ISOLATED_TUSSOCK_GRASSES,
        ISOLATED_VINES,
        LICHENLAND,
        LIVERWORTLAND,
        MALLEE_SHRUBLAND,
        MALLEE_WOODLAND,
        MOSSLAND,
        MUDFLAT,
        OPEN_OCEAN,
        OPEN_CHENOPOD_SHRUBLAND,
        OPEN_FERNLAND,
        OPEN_FORBLAND,
        OPEN_FOREST,
        OPEN_HEATH,
        OPEN_HUMMOCK_GRASSLAND,
        OPEN_LICHENLAND,
        OPEN_LIVERWORTLAND,
        OPEN_MALLEE_FOREST,
        OPEN_MALLEE_SHRUBLAND,
        OPEN_MALLEE_WOODLAND,
        OPEN_MOSSLAND,
        OPEN_RUSHLAND,
        OPEN_SEDGELAND,
        OPEN_SHRUBLAND,
        OPEN_SOD_GRASSLAND,
        OPEN_TUSSOCK_GRASSLAND,
        OPEN_VINELAND,
        OPEN_WOODLAND,
        ROCK_OUTCROP,
        RUSHLAND,
        SALTWATER_LAKE,
        SEDGELAND,
        SHRUBLAND,
        SOD_GRASSLAND,
        SPARSE_CHENOPOD_SHRUBLAND,
        SPARSE_FERNLAND,
        SPARSE_FORBLAND,
        SPARSE_GRASSLAND,
        SPARSE_HEATH,
        SPARSE_LICHENLAND,
        SPARSE_LIVERWORTLAND,
        SPARSE_MALLEE_SHRUBLAND,
        SPARSE_MOSSLAND,
        SPARSE_RUSHLAND,
        SPARSE_SEDGELAND,
        SPARSE_SHRUBLAND,
        SPARSE_SOD_GRASSLAND,
        SPARSE_TUSSOCK_GRASSLAND,
        SPARSE_VINELAND,
        STREAM_OR_RIVER,
        TUSSOCK_GRASSLAND,
        URBAN,
        VINELAND,
        WOODLAND,
    ),
)
