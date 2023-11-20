"""Provides site type vocabulary for the package."""

# Local
from abis_mapping import utils

# Third-party
import rdflib

# Vocabulary
SITE_TYPE = utils.vocabs.FlexibleVocabulary(
    definition=rdflib.Literal("A type of site."),
    base=utils.rdf.uri("bdr-cv/concept/siteType/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/74aa68d3-28fd-468d-8ff5-7e791d9f7159"),
    broader=utils.rdf.uri("bdr-cv/concept/siteType", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, omitted if not provided.
    terms=(),
)
