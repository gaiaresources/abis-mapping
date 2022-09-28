"""Provides conservation jurisdiction vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ACT = utils.vocabs.Term(
    labels=("ACT", "AUSTRALIAN CAPITAL TERRITORY"),
    iri=rdflib.URIRef("https://sws.geonames.org/2177478/"),
)
EPBC = utils.vocabs.Term(
    labels=("EPBC", "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION"),
    iri=rdflib.URIRef("https://sws.geonames.org/2077456/"),
)
NSW = utils.vocabs.Term(
    labels=("NSW", "NEW SOUTH WALES"),
    iri=rdflib.URIRef("https://sws.geonames.org/2155400/"),
)
NT = utils.vocabs.Term(
    labels=("NT", "NORTHERN TERRITORY"),
    iri=rdflib.URIRef("https://sws.geonames.org/2064513/"),
)
QLD = utils.vocabs.Term(
    labels=("QLD", "QUEENSLAND"),
    iri=rdflib.URIRef("https://sws.geonames.org/2152274/"),
)
SA = utils.vocabs.Term(
    labels=("SA", "SOUTH AUSTRALIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2061327/"),
)
TAS = utils.vocabs.Term(
    labels=("TAS", "TASMANIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2147291/"),
)
VIC = utils.vocabs.Term(
    labels=("VIC", "VICTORIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2145234/"),
)
WA = utils.vocabs.Term(
    labels=("WA", "WESTERN AUSTRALIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2058645/"),
)

# Vocabulary
CONSERVATION_JURISDICTION = utils.vocabs.RestrictedVocabulary(
    terms=(ACT, EPBC, NSW, NT, QLD, SA, TAS, VIC, WA),
)
