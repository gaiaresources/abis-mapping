"""Provides Mapper Base Class for the Package"""

# Standard
import abc
import csv
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
from typing import Any, Iterator, Optional, final


# Constants
a = rdflib.RDF.type


class ABISMapper(abc.ABC):
    """ABIS Mapper Base Class"""

    # ABIS Mapper Registry
    registry: dict[str, type["ABISMapper"]] = {}

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Dataset by Gaia Resources"
    DATASET_DEFAULT_ORGANIZATION = "Gaia Resources"

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

    @abc.abstractmethod
    def apply_mapping(
        self,
        data: base_types.ReadableType,
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
        base_iri: rdflib.Namespace | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Default Example Dataset to the Graph

        Args:
            uri (rdflib.URIRef): IRI of the dataset.
            base_iri (rdflib.Namespace | None): Namespace to use for
                created iris.
            graph (rdflib.Graph): Graph to add to.
        """
        # Add Default Dataset to Graph
        graph.add((uri, a, utils.namespaces.TERN.Dataset))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(self.DATASET_DEFAULT_NAME)))
        graph.add((uri, rdflib.SDO.description, rdflib.Literal(self.DATASET_DEFAULT_DESCRIPTION)))
        graph.add((uri, rdflib.SDO.dateCreated, models.temporal.Date.today().to_rdf_literal()))
        graph.add((uri, rdflib.SDO.dateIssued, models.temporal.Date.today().to_rdf_literal()))

        # Add default dataset datatype
        default_dataset_datatype = utils.rdf.uri(f"datatype/datasetID/{self.DATASET_DEFAULT_ORGANIZATION}")
        self._add_default_dataset_datatype(default_dataset_datatype, base_iri, graph)

    def _add_default_dataset_datatype(
        self,
        uri: rdflib.URIRef,
        base_iri: rdflib.Namespace | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds default example dataset datatype to the graph.

        This should only be called when adding the default dataset.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            base_iri (rdflib.Namespace | None): Namespace to use for
                created iris.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add default dataset datatype to graph
        graph.add((uri, a, rdflib.RDFS.Datatype))
        graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{self.DATASET_DEFAULT_ORGANIZATION} datasetID")))
        graph.add((uri, rdflib.SKOS.definition, rdflib.Literal("An identifier for the dataset")))

        # Add default dataset datatype attribution
        default_dataset_attribution = utils.rdf.uri(f"provider/{self.DATASET_DEFAULT_ORGANIZATION}", base_iri)
        graph.add((uri, rdflib.PROV.wasAttributedTo, default_dataset_attribution))

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
    def generate_blank_template(cls) -> None:
        """Generates a blank csv for the template.

        It is based on the schema field names and writes it to a file within
        the template mapper's root dir. NOTE: full schema validation is not applied,
        and metadata validation is.
        """
        # Retrieve Schema Filepath
        directory = pathlib.Path(inspect.getfile(cls)).parent
        schema_file = directory / "schema.json"

        # Get raw schema
        fields: list[dict] = json.loads(schema_file.read_text())["fields"]
        out_path = directory / f"{cls.metadata()['name']}.{cls.metadata()['file_type'].lower()}"
        with out_path.open("w") as f:
            csv_writer = csv.DictWriter(f, [field["name"] for field in fields])
            csv_writer.writeheader()

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
        template_id = mapper.metadata()["id"]
        cls.registry[template_id] = mapper

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
