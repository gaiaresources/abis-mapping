"""Provides threat status vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
EPBC_EX = utils.vocabs.Term(
    labels=(
        "EPBC/EX",
        "EPBC/EXTINCT",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EX",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/EX", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_XW = utils.vocabs.Term(
    labels=(
        "EPBC/XW",
        "EPBC/EXTINCT IN THE WILD",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/XW",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EXTINCT IN THE WILD",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/XW", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CE = utils.vocabs.Term(
    labels=(
        "EPBC/CE",
        "EPBC/CRITICALLY ENDANGERED",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CE",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CRITICALLY ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/CE", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_E = utils.vocabs.Term(
    labels=(
        "EPBC/E",
        "EPBC/ENDANGERED",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/E",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/E", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_V = utils.vocabs.Term(
    labels=(
        "EPBC/V",
        "EPBC/VULNERABLE",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/V",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/V", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CD = utils.vocabs.Term(
    labels=(
        "EPBC/CD",
        "EPBC/CONSERVATION DEPENDENT",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CD",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CONSERVATION DEPENDENT",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/CD", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_CR = utils.vocabs.Term(
    labels=(
        "WA/CR",
        "WA/CRITICALLY ENDANGERED",
        "WA/CRITICALLY ENDANGERED SPECIES",
        "WESTERN AUSTRALIA/CR",
        "WESTERN AUSTRALIA/CRITICALLY ENDANGERED",
        "WESTERN AUSTRALIA/CRITICALLY ENDANGERED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/CR", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EN = utils.vocabs.Term(
    labels=(
        "WA/EN",
        "WA/ENDANGERED",
        "WA/ENDANGERED SPECIES",
        "WESTERN AUSTRALIA/EN",
        "WESTERN AUSTRALIA/ENDANGERED",
        "WESTERN AUSTRALIA/ENDANGERED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/EN", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_VU = utils.vocabs.Term(
    labels=(
        "WA/VU",
        "WA/VULNERABLE",
        "WA/VULNERABLE SPECIES",
        "WESTERN AUSTRALIA/VU",
        "WESTERN AUSTRALIA/VULNERABLE",
        "WESTERN AUSTRALIA/VULNERABLE SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/VU", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EX = utils.vocabs.Term(
    labels=(
        "WA/EX",
        "WA/EXTINCT",
        "WA/EXTINCT SPECIES",
        "WESTERN AUSTRALIA/EX",
        "WESTERN AUSTRALIA/EXTINCT",
        "WESTERN AUSTRALIA/EXTINCT SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/EX", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EW = utils.vocabs.Term(
    labels=(
        "WA/EW",
        "WA/EXTINCT IN THE WILD",
        "WESTERN AUSTRALIA/EW",
        "WESTERN AUSTRALIA/EXTINCT IN THE WILD",
    ),
    iri=utils.rdf.uri("threatStatus/WA/EW", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_MI = utils.vocabs.Term(
    labels=(
        "WA/MI",
        "WA/MIGRATORY SPECIES",
        "WESTERN AUSTRALIA/MI",
        "WESTERN AUSTRALIA/MIGRATORY SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/MI", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_CD = utils.vocabs.Term(
    labels=(
        "WA/CD",
        "WA/CONSERVATION DEPENDENT",
        "WA/CONSERVATION DEPENDENT FAUNA",
        "WESTERN AUSTRALIA/CD",
        "WESTERN AUSTRALIA/CONSERVATION DEPENDENT",
        "WESTERN AUSTRALIA/CONSERVATION DEPENDENT FAUNA",
    ),
    iri=utils.rdf.uri("threatStatus/WA/CD", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_OS = utils.vocabs.Term(
    labels=(
        "WA/OS",
        "WA/OTHER SPECIFICALLY PROTECTED FAUNA",
        "WESTERN AUSTRALIA/OS",
        "WESTERN AUSTRALIA/OTHER SPECIFICALLY PROTECTED FAUNA",
    ),
    iri=utils.rdf.uri("threatStatus/WA/OS", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P1 = utils.vocabs.Term(
    labels=(
        "WA/P1",
        "WA/PRIORITY 1",
        "WA/PRIORITY 1 POORLY KNOWN SPECIES"
        "WESTERN AUSTRALIA/P1",
        "WESTERN AUSTRALIA/PRIORITY 1",
        "WESTERN AUSTRALIA/PRIORITY 1 POORLY KNOWN SPECIES"
    ),
    iri=utils.rdf.uri("threatStatus/WA/P1", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P2 = utils.vocabs.Term(
    labels=(
        "WA/P2",
        "WA/PRIORITY 2",
        "WA/PRIORITY 2 POORLY KNOWN SPECIES",
        "WESTERN AUSTRALIA/P2",
        "WESTERN AUSTRALIA/PRIORITY 2",
        "WESTERN AUSTRALIA/PRIORITY 2 POORLY KNOWN SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P2", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P3 = utils.vocabs.Term(
    labels=(
        "WA/P3",
        "WA/PRIORITY 3",
        "WA/PRIORITY 3 POORLY KNOWN SPECIES",
        "WESTERN AUSTRALIA/P3",
        "WESTERN AUSTRALIA/PRIORITY 3",
        "WESTERN AUSTRALIA/PRIORITY 3 POORLY KNOWN SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P3", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P4 = utils.vocabs.Term(
    labels=(
        "WA/P4",
        "WA/PRIORITY 4",
        "WA/PRIORITY 4 RARE NEAR THREATENED AND OTHER SPECIES IN NEED OF MONITORING",
        "WESTERN AUSTRALIA/P4",
        "WESTERN AUSTRALIA/PRIORITY 4",
        "WESTERN AUSTRALIA/PRIORITY 4 RARE NEAR THREATENED AND OTHER SPECIES IN NEED OF MONITORING",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P4", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)

# Vocabulary
THREAT_STATUS = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of threatStatus."),
    base=utils.rdf.uri("bdr-cv/parameter/threatStatus/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/threatStatus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(
        EPBC_EX,
        EPBC_XW,
        EPBC_CE,
        EPBC_E,
        EPBC_V,
        EPBC_CD,
        WA_CR,
        WA_EN,
        WA_VU,
        WA_EX,
        WA_EW,
        WA_MI,
        WA_CD,
        WA_OS,
        WA_P1,
        WA_P2,
        WA_P3,
        WA_P4
    ),
)
