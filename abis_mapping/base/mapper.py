"""Provides Mapper Base Class for the Package"""

# Standard
import abc
import functools
import inspect
import json
import pathlib

# Third-Party
import frictionless
import frictionless.errors
import rdflib
import rdflib.term

# Local
from . import types as base_types
from abis_mapping import models
from abis_mapping import utils


# Typing
from collections.abc import Iterator, Set
from typing import Any, Final, Optional, final


# Constants
a = rdflib.RDF.type


class ABISMapper(abc.ABC):
    """ABIS Mapper Base Class"""

    @abc.abstractmethod
    def apply_validation(
        self,
        data: base_types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation to Raw Data to Generate Report.

        Args:
            data (ReadableType): Readable raw data.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            frictionless.Report: Validation report for the data.
        """

    def apply_mapping(
        self,
        *,
        data: base_types.ReadableType,
        chunk_size: int | None,
        dataset_iri: rdflib.URIRef,
        base_iri: rdflib.Namespace,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping from Raw Data to ABIS conformant RDF.

        Args:
            data: Readable raw data.
            chunk_size: Size of chunks to split raw data into. None to disabled chunking.
            dataset_iri: IRI of the Dataset this raw data is part of.
            base_iri: Namespace to use when generating new IRIs as part of this mapping.
            **kwargs: Additional keyword arguments.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """
        # Check chunk size
        if chunk_size is not None and chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        # Construct Schema and extra fields schema
        schema = self.extra_fields_schema(
            data=data,
            full_schema=True,
        )
        extra_schema = self.extra_fields_schema(
            data=data,
            full_schema=False,
        )

        # Construct Resource
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=schema,
            encoding="utf-8",
        )

        # Initialise Graph
        graph = utils.rdf.create_graph()
        graph_has_rows: bool = False
        # Add per-chunk mapping for first chunk
        self.apply_mapping_chunk(dataset=dataset_iri, graph=graph)

        # Open the Resource to allow row streaming
        with resource.open() as r:
            # Loop through rows
            for row_num, row in enumerate(r.row_stream, start=1):
                # Map row
                self.apply_mapping_row(
                    row=row,
                    dataset=dataset_iri,
                    graph=graph,
                    extra_schema=extra_schema,
                    base_iri=base_iri,
                    **kwargs,
                )
                graph_has_rows = True

                # yield chunk if required
                if chunk_size is not None and row_num % chunk_size == 0:
                    yield graph
                    # Initialise New Graph for next chunk
                    graph = utils.rdf.create_graph()
                    graph_has_rows = False
                    self.apply_mapping_chunk(dataset=dataset_iri, graph=graph)

            # yield final chunk, or whole graph if not chunking.
            if graph_has_rows or chunk_size is None:
                yield graph

    def apply_mapping_chunk(
        self,
        *,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Applies mapping for RDF that should be present in every chunk.

        This method can be extended by subclasses, remember to call super()!

        Args:
            dataset: The Dataset URI
            graph: The graph for the chunk to add the mapping to.
        """
        # This should be in every chunk, so the type of the dataset can be resolved.
        graph.add((dataset, a, utils.namespaces.TERN.Dataset))

    @abc.abstractmethod
    def apply_mapping_row(
        self,
        *,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        extra_schema: frictionless.Schema,
        base_iri: rdflib.Namespace,
        **kwargs: Any,
    ) -> None:
        """Applies Mapping for a Row in the template by mutating the passed Graph.

        Args:
            row: Row from the template to be processed.
            dataset: Dataset URI.
            graph: Graph to map row into.
            extra_schema: Template schema including any extra fields.
            base_iri: Base IRI namespace to use for mapping.
            kwargs: Additional keyword arguments.
        """

    def add_geometry_supplied_as(
        self,
        subj: rdflib.term.Node,
        pred: rdflib.term.Node,
        obj: rdflib.term.Node,
        geom: models.spatial.Geometry,
        graph: rdflib.Graph,
        spatial_accuracy: rdflib.Literal | None = None,
    ) -> None:
        """Add geometry supplied as originally to the graph.

        Args:
            subj: Subject identifying geometry use.
            pred: Predicate of where transformed
                geometry used.
            obj: Object containing the transformed geometry.
            geom: Geometry object containing values.
            graph: Graph to be added to.
            spatial_accuracy: Tolerance of the supplied geometry.
        """
        # Create top blank node to hold statement
        top_node = rdflib.BNode()

        # Add details of the already created geometry
        graph.add((top_node, a, rdflib.RDF.Statement))
        graph.add((top_node, rdflib.RDF.subject, subj))
        graph.add((top_node, rdflib.RDF.predicate, pred))
        graph.add((top_node, rdflib.RDF.object, obj))
        graph.add((top_node, rdflib.RDFS.comment, rdflib.Literal("supplied as")))

        # Add the supplied as geometry from raw data
        supplied_as = rdflib.BNode()
        graph.add((supplied_as, a, utils.namespaces.GEO.Geometry))
        graph.add((supplied_as, utils.namespaces.GEO.asWKT, geom.to_rdf_literal()))
        if spatial_accuracy is not None:
            graph.add((supplied_as, utils.namespaces.GEO.hasMetricSpatialAccuracy, spatial_accuracy))
        graph.add((top_node, utils.namespaces.GEO.hasGeometry, supplied_as))

    @classmethod
    def add_extra_fields_json(
        cls,
        subject_uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        extra_schema: frictionless.Schema,
    ) -> None:
        """Adds additional fields data to graph as JSON if values exist.

        Args:
            subject_uri: Node for the JSON data to be attached.
            row: Row containing all data including extras.
            graph: Graph to be modified.
            extra_schema: Schema of extra fields. From calling extra_fields_schema(..., full_schema=False).
        """
        # Extract fields and determine if any values
        extra_fields = cls.extract_extra_fields(row, extra_schema)
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
        row: frictionless.Row,
        extra_schema: frictionless.Schema,
    ) -> dict[str, Any]:
        """Extracts extra values from a row not in template schema.

        Args:
            row: Row of data including extra rows.
            extra_schema: Schema of extra fields. From calling extra_fields_schema(..., full_schema=False).

        Returns:
            dict[str, Any]: Dictionary containing extra values, if any.
        """
        # Create dictionary consisting row data from extra fields only
        return {field: row[field] for field in extra_schema.field_names if row[field] is not None}

    @final
    @classmethod
    def extra_fields_schema(
        cls,
        data: frictionless.Row | base_types.ReadableType,
        full_schema: bool = False,
    ) -> frictionless.Schema:
        """Creates a schema with all extra fields found in data.

        The fields of data are expected to be the same or a superset of the template's
        official schema.

        Args:
            data: Row or data expected to
                contain more columns than included in the template's schema.
            full_schema: Flag to indicate whether full schema for row or data
                should be returned or just the difference.

        Returns:
            A schema object, the fields of which are only the extra fields not a part of a
                template's official schema if full_schema = False else the schema will be the
                concatenation of the official schema fields and the extra fields. Extra fields
                are deemed to be any fields not named within the existing schema, as well as
                any fields that are duplicated within the labels of the supplied data.
        """
        # Construct schema
        existing_schema: frictionless.Schema = frictionless.Schema.from_descriptor(cls.schema())

        if isinstance(data, frictionless.Row):
            # Get list of fieldnames of row
            actual_fieldnames = data.field_names

        else:
            # Create resource and infer
            resource = frictionless.Resource(
                source=data,
                format="csv",
                encoding="utf-8",
            )
            resource.infer()

            # Get list of actual fieldnames
            actual_fieldnames = resource.schema.field_names

        # Find list of extra fieldnames
        existing_fieldnames = existing_schema.field_names

        # Collection for unseen fieldnames, allowing for duplicates to be created.
        unseen_existing = [*existing_fieldnames]

        # Get extra fieldnames
        extra_fieldnames: list[str] = []
        for fn in actual_fieldnames:
            if fn not in unseen_existing:
                extra_fieldnames.append(fn)
            if fn in unseen_existing:
                unseen_existing.remove(fn)

        # Construct list of extra Fields with type of string
        extra_fields = [
            frictionless.Field.from_descriptor({"name": fieldname, "type": "string"}) for fieldname in extra_fieldnames
        ]

        if full_schema:
            # Append the extra fields onto the official schema
            for field in extra_fields:
                existing_schema.add_field(field)

            # Return
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

        # Template File is the name and filetype as extension from metadata
        md = cls.metadata()
        template_file = directory / f"{md['name']}.{md['file_type'].lower()}"

        # Return
        return template_file

    @property
    def template_id(self) -> str:
        """Getter for the template id.

        Returns:
            str: template id from metadata
        """
        return self.metadata()["id"]

    @classmethod
    @functools.lru_cache
    def metadata(cls) -> dict[str, str]:
        """Retrieves and Caches the Template Metadata for this Template

        Returns:
            dict[str, Any]: Template Metadata for this Template
        """
        # Retrieve Metadata Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        metadata_file = directory / "metadata.json"

        # Read Metadata and validate
        md_dict = json.loads(metadata_file.read_text())
        md_class = models.metadata.TemplateMetadata.model_validate(md_dict, strict=False)

        # Return
        return md_class.model_dump()

    @final
    @classmethod
    @functools.lru_cache
    def schema(
        cls,
        discard_optional: bool = True,
    ) -> dict[str, Any]:
        """Retrieves and Caches the Frictionless Schema for this Template

        Args:
            discard_optional (bool): Flag to indicate whether to discard optional
                properties if None.

        Returns:
            dict[str, Any]: Frictionless Schema for this Template
        """
        # Retrieve Schema Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        schema_file = directory / "schema.json"

        # Read Schema and validate
        s_dict = json.loads(schema_file.read_text())
        s_class = models.schema.Schema.model_validate(s_dict, strict=True)

        # Dump pydantic class to return dict
        return s_class.model_dump(exclude_none=discard_optional)

    @final
    @classmethod
    def fields(cls) -> dict[str, models.schema.Field]:
        """Indexed dictionary of all fields' metadata.

        Returns:
            dict[str, types.schema.Field]: Dictionary of all fields
                with name as key..
        """
        # Get schema
        schema = models.schema.Schema.model_validate(cls.schema())

        # Return dictionary of fields
        return {f.name: f for f in schema.fields}

    @final
    def root_dir(self) -> pathlib.Path:
        """Returns the root directory for this Template.

        Returns:
            str: Path of the root directory for this Template
        """
        # Get file where caller is defined
        file_path = inspect.getfile(self.__class__)

        # Return the path
        return pathlib.Path(file_path).parent


# Registry for ABIS Mappers.
_registry: Final[dict[str, type[ABISMapper]]] = {}


def register_mapper(mapper: type[ABISMapper]) -> None:
    """Registers a concrete ABIS Mapper

    Args:
        mapper: Mapper class to be registered.
    """
    # Register the mapper with its template id
    template_id = mapper.metadata()["id"]
    _registry[template_id] = mapper


def get_mapper(template_id: str) -> Optional[type[ABISMapper]]:
    """Retrieves ABIS Mapper class for the specified template ID.

    Args:
        template_id: Template ID to retrieve the mapper for.

    Returns:
        ABIS mapper class associated with the specified template ID if found, otherwise `None`.
    """
    # Retrieve and return the mapper
    return _registry.get(template_id)


def registered_ids() -> Set[str]:
    """Retrieves a set of the registered ABIS Mappers' template IDs.

    Returns:
        Set of the template IDs there are registered ABIS Mappers for.
    """
    # Return the set of template IDs.
    # Do not return the _registry dict itself to reduce chance it is mutated outside this module.
    return _registry.keys()
