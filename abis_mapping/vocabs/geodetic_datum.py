"""Provides geodetic datum vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
AGD66 = utils.vocabs.Term(
    labels=("AGD66", "EPSG:4202"),
    iri=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4202"),
    description="Australian Geodetic Datum 1966",
)
AGD84 = utils.vocabs.Term(
    labels=("AGD84", "EPSG:4203"),
    iri=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4203"),
    description="Australian Geodetic Datum 1984",
)
GDA2020 = utils.vocabs.Term(
    labels=("GDA2020", "EPSG:7844"),
    iri=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/7844"),
    description="Geocentric Datum of Australia 2020",
)
GDA94 = utils.vocabs.Term(
    labels=("GDA94", "EPSG:4283"),
    iri=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4283"),
    description="Geocentric Datum of Australia 1994",
)
WGS84 = utils.vocabs.Term(
    labels=("WGS84", "EPSG:4326"),
    iri=rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4326"),
    description="World Geodetic System 1984, used in GPS",
)


# Vocabulary
class GeodeticDatum(utils.vocabs.RestrictedVocabulary):
    vocab_id = "GEODETIC_DATUM"
    terms = (AGD66, AGD84, GDA2020, GDA94, WGS84)


# Register
utils.vocabs.Vocabulary.register(GeodeticDatum)
