"""Provides vocab handling for the package"""

# Standard
import abc

# Third-Party
import rdflib

# Local
from abis_mapping.utils import rdf
from abis_mapping.utils import strings

# Typing
from typing import Optional, Iterable, final, Final


# Constants
a = rdflib.RDF.type


class Term:
    def __init__(
        self,
        labels: Iterable[str],
        iri: rdflib.URIRef,
        description: str,
    ) -> None:
        """Instantiates a Vocabulary Term.

        Args:
            labels (Iterable[str]): Labels for the vocabulary term to match on.
            iri: rdflib.URIRef: IRI for the vicabulary term.
            description (str): Description for the term.
        """
        # Set Instance Attributes
        self.labels: Final[tuple[str, ...]] = tuple(labels)
        self.sanitized_labels: Final[tuple[str, ...]] = tuple(strings.sanitise(label) for label in labels)  # Sanitise
        self.iri: Final[rdflib.URIRef] = iri
        self.description: Final[str] = description

    def to_mapping(self) -> dict[str, rdflib.URIRef]:
        """Converts the term to a mapping of all labels to IRI.

        Returns:
            dict[str, rdflib.URIRef]: Mapping of labels to IRI.
        """
        # Generate and Return
        return {key: self.iri for key in self.sanitized_labels}

    def match(self, value: str) -> bool:
        """Determines whether a specified value matches this term.

        Args:
            value (str): Value to check against this term.

        Returns:
            bool: Whether the value matches this term.
        """
        # Sanitise, Check and Return
        return strings.sanitise(value) in self.sanitized_labels

    @property
    def preferred_label(self) -> str | None:
        """Getter for the preferred label

        Returns:
            str | None: Preferred label if it exists else None.
        """
        return self.labels[0] if len(self.labels) > 0 else None

    @property
    def alternative_labels(self) -> Iterable[str]:
        """Getter for alternative labels

        Returns:
            Iterable[str]: Alternative labels.
        """
        return (lbl for lbl in self.labels if lbl != self.preferred_label)


class Vocabulary(abc.ABC):
    """Base Vocabulary class."""
    # Dictionary to hold all vocabs for mapping by their id.
    id_registry: dict[str, "Vocabulary"] = {}

    def __init__(
        self,
        vocab_id: str,
        terms: Iterable[Term],
        publish: bool = True,
    ):
        """Vocabulary constructor.

        Args:
            vocab_id (str): ID to assign vocabulary.
            publish (bool, optional): Whether to publish vocabulary
                in documentation. Defaults to True.
        """
        # Assign object internal variables
        self.vocab_id: Final[str] = vocab_id
        self.publish: Final[bool] = publish

        # Set Instance Variables
        self.terms: Final[tuple[Term, ...]] = tuple(terms)

        # Generate Dictionary Mapping from Terms
        self._mapping: dict[str | None, rdflib.URIRef | None] = {}
        for term in self.terms:
            self._mapping.update(**term.to_mapping())

    @final
    @classmethod
    def register(
        cls,
        vocab: "Vocabulary",
    ) -> None:
        """Register a Vocabulary within the centralise vocabulary id registry.

        Args:
            vocab (Vocabulary): Corresponding Vocabulary.

        Raises:
            KeyError: The Vocabulary ID is already registered.
        """
        if vocab.vocab_id in cls.id_registry:
            raise KeyError(f"Vocabulary ID {vocab.vocab_id} already registered.")

        cls.id_registry[vocab.vocab_id] = vocab


class RestrictedVocabulary(Vocabulary):
    """Restricted Vocabulary"""

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
        # Sanitise Value
        sanitised_value = strings.sanitise(value)

        # Retrieve if Applicable
        if iri := self._mapping.get(sanitised_value):
            # Return
            return iri

        # Raise Error
        raise VocabularyError(f"Invalid vocabulary value: '{value}'")


class FlexibleVocabulary(Vocabulary):
    """Flexible Vocabulary"""

    def __init__(
        self,
        vocab_id: str,
        definition: rdflib.Literal,
        base: rdflib.URIRef,
        scheme: rdflib.URIRef,
        broader: Optional[rdflib.URIRef],
        default: Optional[Term],
        terms: Iterable[Term],
        publish: bool = True,
    ) -> None:
        """Initialises a Flexible Vocabulary.

        Args:
            vocab_id (str): ID to assign vocabulary.
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
            publish (bool, optional): Whether to publish vocabulary
                within documentation. Defaults to True.
        """
        # Call parent constructor
        super().__init__(vocab_id, terms, publish)

        # Set Instance Variables
        self.definition = definition
        self.base = rdflib.Namespace(base)  # Cast to a Namespace
        self.scheme = scheme
        self.broader = broader
        self.default = default

        # Add Default mapping if Applicable
        if self.default:
            self._mapping.update({None: self.default.iri})

    def get(
        self,
        graph: rdflib.Graph,
        value: Optional[str],
        source: Optional[rdflib.URIRef] = None,
    ) -> rdflib.URIRef:
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
            source (Optional[rdflib.URIRef]): Optional source URI to attribute
                a new vocabulary term to.

        Returns:
            rdflib.URIRef: Default, matching or created vocabulary IRI.

        Raises:
            VocabularyError: Raised if a value is not supplied and there is no
                default fall-back value in the vocabulary.
        """
        # Sanitise Value if Applicable
        sanitised_value = strings.sanitise(value) if value else None

        # Retrieve if Applicable
        if iri := self._mapping.get(sanitised_value):
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

        # Check for Source URI
        if source:
            # Construct Source URI Literal
            uri = rdflib.Literal(source, datatype=rdflib.XSD.anyURI)

            # Add Source
            graph.add((iri, rdflib.DCTERMS.source, uri))

        # Return
        return iri


class VocabularyError(Exception):
    """Error Raised in Vocabulary Handling"""


def get_vocab(key: str) -> Vocabulary | None:
    """Retrieves vocab object for given key.

    Args:
        key (str): Key to retrieve vocab for.

    Returns:
        Vocabulary | None: Corresponding vocabulary for given key or None.
    """
    return Vocabulary.id_registry.get(key)
