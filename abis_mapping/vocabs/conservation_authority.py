"""Provides conservation authority vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ACT = utils.vocabs.Term(
    labels=("ACT", "AUSTRALIAN CAPITAL TERRITORY"),
    iri=rdflib.URIRef("https://sws.geonames.org/2177478/"),
    description="Australian Capital Territory",
)
EPBC = utils.vocabs.Term(
    labels=("EPBC", "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION"),
    iri=rdflib.URIRef("https://sws.geonames.org/2077456/"),
    description="Environment Protection and Biodiversity Conservation",
)
NSW = utils.vocabs.Term(
    labels=("NSW", "NEW SOUTH WALES"),
    iri=rdflib.URIRef("https://sws.geonames.org/2155400/"),
    description="New South Wales",
)
NT = utils.vocabs.Term(
    labels=("NT", "NORTHERN TERRITORY"),
    iri=rdflib.URIRef("https://sws.geonames.org/2064513/"),
    description="Northern Territory",
)
QLD = utils.vocabs.Term(
    labels=("QLD", "QUEENSLAND"),
    iri=rdflib.URIRef("https://sws.geonames.org/2152274/"),
    description="Queensland",
)
SA = utils.vocabs.Term(
    labels=("SA", "SOUTH AUSTRALIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2061327/"),
    description="South Australia",
)
TAS = utils.vocabs.Term(
    labels=("TAS", "TASMANIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2147291/"),
    description="Tasmania",
)
VIC = utils.vocabs.Term(
    labels=("VIC", "VICTORIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2145234/"),
    description="Victoria",
)
WA = utils.vocabs.Term(
    labels=("WA", "WESTERN AUSTRALIA"),
    iri=rdflib.URIRef("https://sws.geonames.org/2058645/"),
    description="Western Australia",
)


# Vocabulary
class ConservationAuthority(utils.vocabs.RestrictedVocabulary):
    vocab_id = "CONSERVATION_AUTHORITY"
    terms = (ACT, EPBC, NSW, NT, QLD, SA, TAS, VIC, WA)
    publish = False


# Register
utils.vocabs.Vocabulary.register(ConservationAuthority)
