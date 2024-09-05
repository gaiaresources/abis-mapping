"""Provides ABIS Mapper for `survey_site_visit_data-v2.0.0` template."""

# Third-party
import frictionless
import rdflib

# Local
from abis_mapping import base

# Typing
from typing import Any, Iterator


class SurveySiteVisitMapper(base.mapper.ABISMapper):
    """ABIS mapper for the v2 survey site data csv template."""

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Systematic Survey Site Visit Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Site Visit Dataset by Gaia Resources"

    def apply_validation(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the csv Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.
            **kwargs (Any): Additional keyword arguments.

        Keyword Args:
            site_visit_id_map (dict[str, bool]): Site visit ids present in the occurrence template.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # TODO: Implement
        raise NotImplementedError

        # Extract keyword arguments
        # TODO: Uncomment
        # site_visit_id_map: dict[str, bool] = kwargs.get("site_visit_id_map", {})

        # Construct schema
        schema = self.extra_fields_schema(data=data, full_schema=True)

        # Construct resource
        resource = frictionless.Resource(
            source=data,
            format="csv",
            schema=schema,
            encoding="utf-8",
        )

        # Validate
        report = resource.validate()

        # Return validation report
        return report

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: rdflib.URIRef | None = None,
        base_iri: rdflib.Namespace | None = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping from Raw Data to ABIS conformant RDF.

        Args:
            data (ReadableType): Readable raw data.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.
            **kwargs (Any): Additional keyword arguments.

        Keyword Args:
            chunk_size (Optional[int]): How many rows of the original data to
                ingest before yielding a graph. `None` will ingest all rows.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """
        # TODO: Implement
        raise NotImplementedError
