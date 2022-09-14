"""Provides threat status vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
EPBC_EX = utils.vocabs.Term(
    labels=("EPBC/EX", ),
    iri=utils.rdf.uri("threatStatus/EPBC/EX", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_XW = utils.vocabs.Term(
    labels=("EPBC/XW", ),
    iri=utils.rdf.uri("threatStatus/EPBC/XW", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CE = utils.vocabs.Term(
    labels=("EPBC/CE", ),
    iri=utils.rdf.uri("threatStatus/EPBC/CE", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_E = utils.vocabs.Term(
    labels=("EPBC/E", ),
    iri=utils.rdf.uri("threatStatus/EPBC/E", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_V = utils.vocabs.Term(
    labels=("EPBC/V", ),
    iri=utils.rdf.uri("threatStatus/EPBC/V", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CD = utils.vocabs.Term(
    labels=("EPBC/CD", ),
    iri=utils.rdf.uri("threatStatus/EPBC/CD", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_CR = utils.vocabs.Term(
    labels=("WA/CR", ),
    iri=utils.rdf.uri("threatStatus/WA/CR", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EN = utils.vocabs.Term(
    labels=("WA/EN", ),
    iri=utils.rdf.uri("threatStatus/WA/EN", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_VU = utils.vocabs.Term(
    labels=("WA/VU", ),
    iri=utils.rdf.uri("threatStatus/WA/VU", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EX = utils.vocabs.Term(
    labels=("WA/EX", ),
    iri=utils.rdf.uri("threatStatus/WA/EX", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EW = utils.vocabs.Term(
    labels=("WA/EW", ),
    iri=utils.rdf.uri("threatStatus/WA/EW", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_MI = utils.vocabs.Term(
    labels=("WA/MI", ),
    iri=utils.rdf.uri("threatStatus/WA/MI", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_CD = utils.vocabs.Term(
    labels=("WA/CD", ),
    iri=utils.rdf.uri("threatStatus/WA/CD", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_OS = utils.vocabs.Term(
    labels=("WA/OS", ),
    iri=utils.rdf.uri("threatStatus/WA/OS", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P1 = utils.vocabs.Term(
    labels=("WA/P1", ),
    iri=utils.rdf.uri("threatStatus/WA/P1", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P2 = utils.vocabs.Term(
    labels=("WA/P2", ),
    iri=utils.rdf.uri("threatStatus/WA/P2", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P3 = utils.vocabs.Term(
    labels=("WA/P3", ),
    iri=utils.rdf.uri("threatStatus/WA/P3", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P4 = utils.vocabs.Term(
    labels=("WA/P4", ),
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
