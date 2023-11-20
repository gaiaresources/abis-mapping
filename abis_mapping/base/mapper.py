"""Provides Mapper Base Class for the Package"""


# Standard
import abc
import functools
import inspect
import json
import pathlib
import datetime

# Third-Party
import frictionless
import rdflib

# Local
from . import types
from abis_mapping import utils

# Typing
from typing import Any, Iterator, Optional, final


# Constants
a = rdflib.RDF.type


class ABISMapper(abc.ABC):
    """ABIS Mapper Base Class"""

    # ABIS Mapper Registry
    registry: dict[str, type["ABISMapper"]] = {}

    # ABIS Mapper Template ID and Instructions File
    template_id: str = NotImplemented  # Must be implemented
    instructions_file: str = NotImplemented  # Must be implemented

    # List of frictionless errors to be skipped by default
    skip_errors: list[str] = ["extra-label", "extra-cell"]

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Dataset by Gaia Resources"

    @abc.abstractmethod
    def apply_validation(
        self,
        data: types.ReadableType,
    ) -> frictionless.Report:
        """Applies Frictionless Validation to Raw Data to Generate Report.

        Args:
            data (ReadableType): Readable raw data.

        Returns:
            frictionless.Report: Validation report for the data.
        """

    @abc.abstractmethod
    def apply_mapping(
        self,
        data: types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping from Raw Data to ABIS conformant RDF.

        Args:
            data (ReadableType): Readable raw data.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.
            **kwargs (Any): Additional keyword arguments.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """

    def add_default_dataset(
        self,
        uri: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Default Example Dataset to the Graph

        Args:
            uri (rdflib.URIRef): IRI of the dataset.
            graph (rdflib.Graph): Graph to add to.
        """
        # Add Default Dataset to Graph
        graph.add((uri, a, utils.namespaces.TERN.RDFDataset))
        graph.add((uri, rdflib.DCTERMS.title, rdflib.Literal(self.DATASET_DEFAULT_NAME)))
        graph.add((uri, rdflib.DCTERMS.description, rdflib.Literal(self.DATASET_DEFAULT_DESCRIPTION)))
        graph.add((uri, rdflib.DCTERMS.issued, utils.rdf.toTimestamp(datetime.date.today())))

    @classmethod
    def add_extra_fields_json(
        cls,
        subject_uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds additional fields data to graph as JSON if values exist.

        Args:
            subject_uri (rdflib.URIRef): Node for the JSON data to be attached.
            row (frictionless.Row): Row containing all data including extras.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract fields and determine if any values
        extra_fields = cls.extract_extra_fields(row)
        if extra_fields == {}:
            return

        # Create JSON string literal
        json_str = json.dumps(extra_fields)
        json_node = rdflib.Literal(json_str, datatype=rdflib.RDF.JSON)

        # Add to graph
        graph.add((subject_uri, rdflib.RDFS.comment, json_node))

    @final
    @classmethod
    def extract_extra_fields(
        cls,
        row: frictionless.Row
    ) -> dict[str, Any]:
        """Extracts extra values from a row not in template schema.

        Args:
            row (frictionless.Row): Row of data including extra rows.

        Returns:
            dict[str, Any]: Dictionary containing extra values, if any.
        """
        # Get schema consisting of extra fields
        extra_schema = cls.extra_fields_schema(row)

        # Create dictionary consisting row data from extra fields only
        return {field: row[field] for field in extra_schema.field_names if row[field] is not None}

    @final
    @classmethod
    def extra_fields_schema(
        cls,
        data: frictionless.Row | types.ReadableType,
        full_schema: bool = False
    ) -> frictionless.Schema:
        """Creates a schema with all extra fields found in data.

        The fields of data are expected to be the same or a superset of the template's
        official schema. It is expected that validation has occurred prior to calling.

        Args:
            data (frictionless.Row | types.ReadableType): Row or data expected to
                contain more columns than included in the template's schema.
            full_schema (bool): Flag to indicate whether full schema for row or data
                should be returned or just the difference.

        Returns:
            frictionless.Schema: A schema object, the fields of which are only
                the extra fields not a part of a template's official schema if full_schema = False
                else the schema will be the concatenation of the official schema fields and the
                extra fields.
        """
        # Construct official schema
        existing_schema: frictionless.Schema = frictionless.Schema.from_descriptor(cls.schema())

        if isinstance(data, frictionless.Row):
            # Get list of fieldnames of row
            actual_fieldnames = data.field_names

            # Create schema from row fields
            actual_schema = frictionless.Schema(fields=data.fields)
        else:
            # Create resource and infer
            resource = frictionless.Resource(
                data=data,
                format="csv",
            )
            resource.infer()

            # Get actual schema
            actual_schema = resource.schema

            # Get list of actual fieldnames
            actual_fieldnames = resource.schema.field_names

        # Find list of extra fieldnames
        existing_fieldnames = existing_schema.field_names
        if len(actual_fieldnames) > len(existing_fieldnames):
            extra_fieldnames = actual_fieldnames[len(existing_fieldnames):]
        else:
            extra_fieldnames = []

        # Construct list of extra Fields
        extra_fields = [actual_schema.get_field(fieldname) for fieldname in extra_fieldnames]

        if full_schema:
            # Append the extra fields onto the official schema and return
            for field in extra_fields:
                existing_schema.add_field(field)

            return existing_schema

        # Create difference schema and return
        return frictionless.Schema(fields=extra_fields)

    @final
    @classmethod
    @functools.lru_cache
    def template(cls) -> pathlib.Path:
        """Retrieves and Caches the Template Filepath

        Returns:
            pathlib.Path: Filepath for this Template
        """
        # Retrieve Template Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        template_file = directory / cls.template_id  # Template File is the Template ID

        # Return
        return template_file

    @final
    @classmethod
    @functools.lru_cache
    def metadata(cls) -> dict[str, Any]:
        """Retrieves and Caches the Template Metadata for this Template

        Returns:
            dict[str, Any]: Template Metadata for this Template
        """
        # Retrieve Metadata Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        metadata_file = directory / "metadata.json"

        # Read Metadata and Return
        return json.loads(metadata_file.read_text())  # type: ignore[no-any-return]

    @final
    @classmethod
    @functools.lru_cache
    def schema(cls) -> dict[str, Any]:
        """Retrieves and Caches the Frictionless Schema for this Template

        Returns:
            dict[str, Any]: Frictionless Schema for this Template
        """
        # Retrieve Schema Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        schema_file = directory / "schema.json"

        # Read Schema and Return
        return json.loads(schema_file.read_text())  # type: ignore[no-any-return]

    @final
    @classmethod
    @functools.lru_cache
    def instructions(cls) -> pathlib.Path:
        """Retrieves and Caches the Template Instructions

        Returns:
            pathlib.Path: Filepath for this Template's Instructions
        """
        # Retrieve Template Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        instructions_file = directory / cls.instructions_file

        # Return
        return instructions_file

    @final
    @classmethod
    def register_mapper(
        cls,
        mapper: type["ABISMapper"],
    ) -> None:
        """Registers a concrete ABIS Mapper with the Base Class

        Args:
            mapper (type[ABISMapper]): Mapper to be registered.
        """
        # Register the mapper with its template id
        cls.registry[mapper.template_id] = mapper


def get_mapper(template_id: str) -> Optional[type[ABISMapper]]:
    """Retrieves ABIS Mapper class for the specified template ID.

    Args:
        template_id (str): Template ID to retrieve the mapper for.

    Returns:
        Optional[type[ABISMapper]]: ABIS mapper class associated with the
            specified template ID if found, otherwise `None`.
    """
    # Retrieve and return the mapper
    return ABISMapper.registry.get(template_id)


def get_mappers() -> dict[str, type[ABISMapper]]:
    """Retrieves the full registry of ABIS Mappers.

    Returns:
        dict[str, type[ABISMapper]]: Dictionary of template ID to ABIS Mapper.
    """
    # Retrieve and return the mappers
    return ABISMapper.registry
