"""Provides rdf namespaces for the package"""

# Third-Party
import rdflib


# Default Base IRI Namespace
EXAMPLE = rdflib.Namespace("http://example.com/")

# Namespaces
GEO = rdflib.Namespace("http://www.opengis.net/ont/geosparql#")
TERN = rdflib.Namespace("https://w3id.org/tern/ontologies/tern/")
DWC = rdflib.Namespace("http://rs.tdwg.org/dwc/terms/")
REG = rdflib.Namespace("http://purl.org/linked-data/registry#")
BDR = rdflib.Namespace("https://linked.data.gov.au/def/bdr/")
ABIS = rdflib.Namespace("https://linked.data.gov.au/def/abis/")

# Namespaces used for IRIs, but not bound to the graph
LINKED_DATA = rdflib.Namespace("https://linked.data.gov.au/")
DATASET_BDR = rdflib.Namespace("https://linked.data.gov.au/dataset/bdr/")
