"""Provides reproductive condition vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Vocabulary
class ReproductiveCondition(utils.vocabs.FlexibleVocabulary):
    vocab_id = "REPRODUCTIVE_CONDITION"
    definition = rdflib.Literal("A type of reproductiveCondition.")
    base = "bdr-cv/parameter/reproductiveCondition/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4b2e788d-260b-4cfc-91f4-99e7c2ad2c42")
    default = None  # No default, ommitted if not provided
    terms = ()  # No baseline vocabulary values
    publish = False


# Register
utils.vocabs.register(ReproductiveCondition)
