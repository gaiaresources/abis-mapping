"""Provides conservation jurisdiction vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
EPBC = utils.vocabs.Term(
    labels=("EPBC", "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION"),
    iri=rdflib.URIRef("https://sws.geonames.org/2077456/"),
)
WA = utils.vocabs.Term(
    labels=("WA", "WESTERN AUSTRALIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2058645/"),
)
QLD = utils.vocabs.Term(
    labels=("QLD", "QUEENSLAND"),
    iri=rdflib.URIRef("https://sws.geonames.org/2152274/"),
)

# Vocabulary
CONSERVATION_JURISDICTION = utils.vocabs.RestrictedVocabulary(
    terms=(EPBC, WA, QLD),
)
