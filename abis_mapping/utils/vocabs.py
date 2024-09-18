"""Provides vocab handling for the package"""

# Standard
import abc

# Third-Party
import rdflib

# Local
from abis_mapping.utils import rdf
from abis_mapping.utils import strings

# Typing
from typing import Optional, Iterable, final, Final, Type


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
            iri: rdflib.URIRef: IRI for the vocabulary term.
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
    """Base Vocabulary class.

    Attributes:
        id_registry (dict[str, Vocabulary]): Dictionary to hold all vocabs for
            mapping by their id.
        vocab_id (str): ID to assign vocabulary.
        terms (Iterable[Term]): Terms to add to the vocabulary.
        publish (bool, optional): Whether to publish vocabulary
            in documentation. Defaults to True.
    """
    # Dictionary to hold all vocabs for mapping by their id.
    id_registry: dict[str, Type["Vocabulary"]] = {}

    # Attributes assigned per vocabulary
    vocab_id: str
    terms: Iterable[Term]
    publish: bool = True

    def __init__(
        self,
        graph: rdflib.Graph,
        source: Optional[rdflib.URIRef] = None,
    ):
        """Vocabulary constructor.

        Args:
            graph (rdflib.Graph): Graph to reference
                within vocabulary
            source (Optional[rdflib.URIRef]): Optional source URI to attribute
                a new vocabulary term to.
        """
        # Assign instance variables
        self.graph = graph
        self.source: Optional[rdflib.URIRef] = source

        # Generate Dictionary Mapping from Terms
        self._mapping: dict[str | None, rdflib.URIRef | None] = {}
        for term in self.terms:
            self._mapping.update(**term.to_mapping())

    @abc.abstractmethod
    def get(self, value: str | None) -> rdflib.URIRef:
        """Retrieve na IRI from the vocabulary.

        Args:
            value (Optional[str]): Possible raw string value to search for in
                vocabulary.

        Returns:
            rdflib.URIRef: Matching vocabulary IRI.
        """

    @final
    @classmethod
    def register(
        cls,
        vocab: Type["Vocabulary"],
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

    def get(self, value: str | None) -> rdflib.URIRef:
        """Retrieves an IRI from the Vocabulary.

        Args:
            value (str): Raw string value to search for in vocabulary.

        Returns:
            rdflib.URIRef: Matching vocabulary IRI.

        Raises:
            VocabularyError: Raised if supplied value does not match an
                existing vocabulary term.
        """
        # Check for Value
        if not value:
            # Raise Error
            raise VocabularyError("Value not supplied for vocabulary with no default")

        # Sanitise Value
        sanitised_value = strings.sanitise(value)

        # Retrieve if Applicable
        if iri := self._mapping.get(sanitised_value):
            # Return
            return iri

        # Raise Error
        raise VocabularyError(f"Invalid vocabulary value: '{value}'")


class FlexibleVocabulary(Vocabulary):
    """Flexible Vocabulary.

    Attributes:
        definition (rdflib.Literal): Definition to use when creating a new
            vocabulary term 'on the fly'.
        base_ns (rdflib.URIRef): Base IRI namespace to use when creating a new
            vocabulary term 'on the fly'.
        scheme (rdflib.URIRef): Scheme IRI to use when creating a new
            vocabulary term 'on the fly'.
        broader (Optional[rdflib.URIRef]): Optional broader IRI to use when
            creating a new vocabulary term 'on the fly'.
        scope_note (Optional[rdflib.Literal]): Optional scope note to use when
            creating a new vocabulary term 'on the fly'.
            This can be set on the subclass as a global default, and/or set on individual
            instances, which will override that default.
        default (Optional[Term]): Optional default term to fall back on if
            a value is not supplied.
    """
    # Declare attributes applicable to a flexible vocab
    definition: rdflib.Literal
    base: rdflib.URIRef
    scheme: rdflib.URIRef
    broader: Optional[rdflib.URIRef]
    scope_note: Optional[rdflib.Literal] = None
    default: Optional[Term]

    def __init__(
        self,
        graph: rdflib.Graph,
        source: Optional[rdflib.URIRef] = None,
    ):
        """Flexible Vocabulary constructor.

        Args:
            graph (rdflib.Graph): Graph to reference
                within vocabulary
            source (Optional[rdflib.URIRef]): Optional source URI to attribute
                a new vocabulary term to.
        """
        # Call parent constructor
        super().__init__(graph=graph, source=source)

        # Set Instance Variables
        self.base_ns = rdflib.Namespace(self.base)  # Cast to a Namespace

        # Add Default mapping if Applicable
        if self.default:
            self._mapping.update({None: self.default.iri})

    def _add_pref_label(
        self,
        iri: rdflib.URIRef,
        value: str,
    ) -> None:
        """Adds the prefLabel predicated triple for a new concept to the graph.

        This can be overridden in subclasses to change its behavior, e.g.
            Kingdom Occurrence and Kingdom Specimen have done this.

        Args:
            iri (rdflib.URIRef): Subject of the triple
            value (str): Raw string value provided in supplied data.
        """
        # Add triple to graph.
        self.graph.add((iri, rdflib.SKOS.prefLabel, rdflib.Literal(value)))

    def get(
        self,
        value: Optional[str],
    ) -> rdflib.URIRef:
        """Retrieves an IRI from the Vocabulary.

        If the value supplied is `None` (i.e., it was left blank in the CSV)
        then the default vocabulary term is returned if available, otherwise
        an exception is raised.

        If the value cannot be found in the mapping, then a new one is created
        'on the fly'.

        Args:
            value (Optional[str]): Possible raw string value to search for in
                vocabulary.

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
        iri = rdf.uri(value, namespace=self.base_ns)

        # Add to Graph
        self.graph.add((iri, a, rdflib.SKOS.Concept))
        self.graph.add((iri, rdflib.SKOS.definition, self.definition))
        self.graph.add((iri, rdflib.SKOS.inScheme, self.scheme))
        self._add_pref_label(iri, value)

        # Check for Broader IRI
        if self.broader:
            # Add Broader
            self.graph.add((iri, rdflib.SKOS.broader, self.broader))

        # Check for Source URI
        if self.source:
            # Construct Source URI Literal
            uri = rdflib.Literal(self.source, datatype=rdflib.XSD.anyURI)

            # Add Source
            self.graph.add((iri, rdflib.DCTERMS.source, uri))

        if self.scope_note is not None:
            self.graph.add((iri, rdflib.SKOS.scopeNote, self.scope_note))

        # Return
        return iri


class VocabularyError(Exception):
    """Error Raised in Vocabulary Handling"""


def get_vocab(key: str) -> Type[Vocabulary]:
    """Retrieves vocab object for given key.

    Args:
        key (str): Key to retrieve vocab for.

    Returns:
        Type[Vocabulary] | None: Corresponding vocabulary class
            for given key or None.

    Raises:
        ValueError: If supplied key doesn't exist within the registry.
    """
    try:
        return Vocabulary.id_registry[key]
    except KeyError:
        # Transform to ValueError, to assist with validation libraries.
        raise ValueError(f"Key {key} not found in registry.")
