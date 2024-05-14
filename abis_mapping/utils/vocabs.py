"""Provides vocab handling for the package"""

# Standard
import abc
import collections

# Third-Party
import rdflib

# Local
from abis_mapping.utils import rdf
from abis_mapping.utils import strings

# Typing
from typing import Optional, Iterable, NamedTuple, final


# Constants
a = rdflib.RDF.type


class TemplateField(NamedTuple):
    """Named tuple to hold combinations of template and field."""
    template_id: str
    field_name: str


class Vocabulary(abc.ABC):
    """Base Vocabulary class."""

    template_field_registry: dict[TemplateField, "Vocabulary"] = {}
    id_registry: dict[str, "Vocabulary"] = {}

    def __init__(
        self,
        vocab_id: str,
    ):
        """Vocabulary constructor.

        Args:
            vocab_id (str): ID to assign vocabulary.
        """
        self._vocab_id = vocab_id

    @property
    def vocab_id(self) -> str:
        """Getter for the Vocabulary's ID.

        Returns:
            str: The Vocabulary's ID.
        """
        return self._vocab_id

    @final
    @classmethod
    def register_template_field(
        cls,
        template_field: TemplateField,
        vocab: "Vocabulary",
    ) -> None:
        """Register a Vocabulary within the centralised template field registry.

        Args:
            template_field (TemplateField): Template and field combo vocab is to be used.
            vocab (Vocabulary): Vocabulary to register against.

        Raises:
            KeyError: The template field has already been registered against a Vocabulary.
        """
        if template_field in cls.template_field_registry:
            raise KeyError(f"Template field {template_field} already registered.")

        cls.template_field_registry[template_field] = vocab

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

    @abc.abstractmethod
    def terms(self) -> dict[str, rdflib.URIRef]:
        """Getter for the vocabs terms"""


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
        self.labels = tuple(strings.sanitise(label) for label in labels)  # Sanitise
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
        # Sanitise, Check and Return
        return strings.sanitise(value) in self.labels


class RestrictedVocabulary(Vocabulary):
    """Restricted Vocabulary"""

    def __init__(
        self,
        vocab_id: str,
        terms: Iterable[Term],
    ) -> None:
        """Initialises a Restricted Vocabulary.

        Args:
            vocab_id (str): ID to assign vocabulary.
            terms (Iterable[Term]): Terms for the vocabulary.
        """
        # Call parent constructor
        super().__init__(vocab_id)

        # Set Instance Variables
        self._terms = tuple(terms)

        # Generate Dictionary Mapping from Terms
        self._mapping: dict[str, rdflib.URIRef] = {}
        for term in self._terms:
            self._mapping.update(**term.to_mapping())

    @property
    def terms(self) -> dict[str, rdflib.URIRef]:
        return self._mapping

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
        """
        # Call parent constructor
        super().__init__(vocab_id)

        # Set Instance Variables
        self.definition = definition
        self.base = rdflib.Namespace(base)  # Cast to a Namespace
        self.scheme = scheme
        self.broader = broader
        self.default = default
        self._terms = tuple(terms)

        # Generate Dictionary Mapping from Terms
        self._mapping: dict[Optional[str], Optional[rdflib.URIRef]] = {}
        for term in self._terms:
            self._mapping.update(**term.to_mapping())

        # Add Default if Applicable
        if self.default:
            self._mapping.update({None: self.default.iri})

    @property
    def terms(self) -> dict[str, rdflib.URIRef]:
        """Getter for the vocabs terms"""
        return self._mapping

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


def get_vocab(key: str | TemplateField) -> Vocabulary | None:
    """Retrieves vocab object for given key.

    Args:
        key (str | TemplateField): Key to retrieve vocab for.

    Returns:
        Vocabulary: Corresponding vocabulary for given key.
    """
    # Check type of key supplied
    if isinstance(key, str):
        return Vocabulary.id_registry.get(key)

    return Vocabulary.template_field_registry.get(key)
