"""Provides rdf namespaces for the package"""

# Third-Party
import rdflib


# Default Base IRI Namespace
EXAMPLE = rdflib.Namespace("http://example.com/")

# Namespaces
GEO = rdflib.Namespace("http://www.opengis.net/ont/geosparql#")
TERN = rdflib.Namespace("https://w3id.org/tern/ontologies/tern/")
DWC = rdflib.Namespace("http://rs.tdwg.org/dwc/terms/")
BDR = rdflib.Namespace("https://linked.data.gov.au/def/bdr/")
ABIS = rdflib.Namespace("https://linked.data.gov.au/def/abis/")
BDR_DATATYPES = rdflib.Namespace("https://linked.data.gov.au/dataset/bdr/datatypes/")
DATASET_BDR = rdflib.Namespace("https://linked.data.gov.au/dataset/bdr/")
