"""Provides vocab handling for the package"""


# Third-Party
import rdflib

# Local
from . import rdf

# Typing
from typing import Optional


# Constants
a = rdflib.RDF.type


class RestrictedVocabulary:
    """Restricted Vocabulary"""

    def __init__(
        self,
        mapping: dict[str, rdflib.URIRef],
    ) -> None:
        """Initialises a Restricted Vocabulary.

        Args:
            mapping (dict[str, str]): Mapping of raw string values that can be
                entered into a CSV, to vocabulary IRIs.
        """
        # Set Instance Variables
        self.mapping = mapping

    def get(self, value: str) -> rdflib.URIRef:
        """Retrieves an IRI from the Vocabulary.

        Args:
            value (str): Raw string value to search for in vocabulary.

        Returns:
            rdflib.URIRef: Matching vocabulary IRI.

        Raises:
            VocabularyError: Raised if supplied value does not match an
                existing vocabulary term.
        """
        # Retrieve if Applicable
        if iri := self.mapping.get(value.upper()):  # Uppercase
            # Return
            return iri

        # Raise Error
        raise VocabularyError(f"Invalid vocabulary value: '{value}'")


class FlexibleVocabulary:
    """Flexible Vocabulary"""

    def __init__(
        self,
        definition: rdflib.Literal,
        base: rdflib.URIRef,
        scheme: rdflib.URIRef,
        broader: Optional[rdflib.URIRef],
        default: Optional[rdflib.URIRef],
        mapping: dict[str, rdflib.URIRef],
    ) -> None:
        """Initialises a Flexible Vocabulary.

        Args:
            definition (rdflib.Literal): Definition to use when creating a new
                vocabulary term 'on the fly'.
            base (rdflib.URIRef): Base IRI namespace to use when creating a new
                vocabulary term 'on the fly'.
            scheme (rdflib.URIRef): Scheme IRI to use when creating a new
                vocabulary term 'on the fly'.
            broader (Optional[rdflib.URIRef]): Optional broader IRI to use when
                creating a new vocabulary term 'on the fly'.
            default (Optional[rdflib.URIRef]): Optional default IRI to fall
                back on if a value is not supplied.
            mapping (dict[str, str]): Mapping of raw string values that can be
                entered into a CSV, to vocabulary IRIs.
        """
        # Set Instance Variables
        self.definition = definition
        self.base = rdflib.Namespace(base)  # Cast to a Namespace
        self.scheme = scheme
        self.broader = broader
        self.default = default
        self.mapping = mapping | {None: self.default}  # Add Default Value

    def get(self, graph: rdflib.Graph, value: Optional[str]) -> rdflib.URIRef:
        """Retrieves an IRI from the Vocabulary.

        If the value supplied is `None` (i.e., it was left blank in the CSV)
        then the default vocabulary term is returned if available, otherwise
        an exception is raised.

        If the value cannot be found in the mapping, then a new one is created
        'on the fly'.

        Args:
            graph (rdflib.Graph): Graph to create a new vocabulary term in.
            value (Optional[str]): Possible raw string value to search for in
                vocabulary.

        Returns:
            rdflib.URIRef: Default, matching or created vocabulary IRI.

        Raises:
            VocabularyError: Raised if a value is not supplied and there is no
                default fall-back value in the vocabulary.
        """
        # Retrieve if Applicable
        if iri := self.mapping.get(value.upper() if value else None):  # Uppercase
            # Return
            return iri

        # Check for Value
        if not value:
            # Raise Error
            raise VocabularyError("Value not supplied for vocabulary with no default")

        # Create our Own Concept IRI
        iri = rdf.uri(value, namespace=self.base)

        # Add to Graph
        graph.add((iri, a, rdflib.SKOS.Concept))
        graph.add((iri, rdflib.SKOS.definition, self.definition))
        graph.add((iri, rdflib.SKOS.inScheme, self.scheme))
        graph.add((iri, rdflib.SKOS.prefLabel, rdflib.Literal(value)))

        # Check for Broader IRI
        if self.broader:
            # Add Broader
            graph.add((iri, rdflib.SKOS.broader, self.broader))

        # Return
        return iri


class VocabularyError(Exception):
    """Error Raised in Vocabulary Handling"""
