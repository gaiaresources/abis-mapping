"""Provides vocab handling for the package"""


# Third-Party
import rdflib

# Local
from . import rdf

# Typing
from typing import Optional, Iterable


# Constants
a = rdflib.RDF.type


class Term:
    def __init__(
        self,
        labels: Iterable[str],
        iri: rdflib.URIRef,
    ) -> None:
        """Instantiates a Vocabulary Term.

        Args:
            labels (Iterable[str]): Labels for the vocabulary term to match on.
            iri: rdflib.URIRef: IRI for the vicabulary term.
        """
        # Set Instance Attributes
        self.labels = tuple(label.upper() for label in labels)  # Uppercase
        self.iri = iri

    def to_mapping(self) -> dict[str, rdflib.URIRef]:
        """Converts the term to a mapping of all labels to IRI.

        Returns:
            dict[str, rdflib.URIRef]: Mapping of labels to IRI.
        """
        # Generate and Return
        return {key: self.iri for key in self.labels}

    def match(self, value: str) -> bool:
        """Determines whether a specified value matches this term.

        Args:
            value (str): Value to check against this term.

        Returns:
            bool: Whether the value matches this term.
        """
        # Check and Return
        return value.upper() in self.labels


class RestrictedVocabulary:
    """Restricted Vocabulary"""

    def __init__(
        self,
        terms: Iterable[Term],
    ) -> None:
        """Initialises a Restricted Vocabulary.

        Args:
            terms (Iterable[Term]): Terms for the vocabulary.
        """
        # Set Instance Variables
        self.terms = tuple(terms)

        # Generate Dictionary Mapping from Terms
        self.mapping: dict[str, rdflib.URIRef] = {}
        for term in self.terms:
            self.mapping.update(**term.to_mapping())

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
        default: Optional[Term],
        terms: Iterable[Term],
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
            default (Optional[Term]): Optional default term to fall back on if
                a value is not supplied.
            terms (Iterable[Term]): Terms for the vocabulary.
        """
        # Set Instance Variables
        self.definition = definition
        self.base = rdflib.Namespace(base)  # Cast to a Namespace
        self.scheme = scheme
        self.broader = broader
        self.default = default
        self.terms = tuple(terms)

        # Generate Dictionary Mapping from Terms
        self.mapping: dict[Optional[str], Optional[rdflib.URIRef]] = {}
        for term in self.terms:
            self.mapping.update(**term.to_mapping())

        # Add Default if Applicable
        if self.default:
            self.mapping.update({None: self.default.iri})

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
