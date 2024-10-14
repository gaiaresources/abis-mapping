"""Provides ABIS Mapper for `survey_site_visit_data-v2.0.0` template."""

# Third-party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import settings
from abis_mapping import types

# Typing
from typing import Any, Iterator


# Constants / shortcuts
a = rdflib.RDF.type


class SurveySiteVisitMapper(base.mapper.ABISMapper):
    """ABIS mapper for the v2 survey site visit data csv template."""

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
        report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra custom checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    plugins.logical_or.LogicalOr(
                        field_names=["siteVisitStart", "siteVisitEnd"],
                    ),
                    plugins.chronological.ChronologicalOrder(
                        field_names=["siteVisitStart", "siteVisitEnd"],
                    ),
                ],
            ),
        )

        # Return validation report
        return report

    def extract_temporal_defaults(
        self,
        data: base.types.ReadableType,
    ) -> dict[str, str]:
        """Constructs a dictionary mapping site visit id to default temporal entity.

        The default temporal entity value will contain serialized RDF as turtle.

        Args:
            data (base.types.ReadableType): Raw data to be mapped.

        Returns:
            dict[str, str]: Keys are the site visit id, values are the serialized
                RDF (turtle) containing the default temporal entity.
        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct resource
        resource = frictionless.Resource(source=data, format="csv", schema=schema, encoding="utf-8")

        # Create empty dictionary to hold map
        result: dict[str, str] = {}

        # Context manager for row streaming
        with resource.open() as r:
            for row in r.row_stream:
                # Extract values and
                # Determine if any dates are present in the row
                start_date: types.temporal.Timestamp = row["siteVisitStart"]
                end_date: types.temporal.Timestamp = row["siteVisitEnd"]
                site_visit_id: str = row["siteVisitID"]
                if not start_date and not end_date:
                    continue

                # Create new graph
                graph = rdflib.Graph()

                self.add_temporal_coverage_bnode(
                    graph=graph,
                    start_date=start_date,
                    end_date=end_date,
                )

                # Add serialize rdf as turtle to result map
                result[site_visit_id] = graph.serialize(format="turtle")

        return result

    def add_temporal_coverage_bnode(
        self,
        graph: rdflib.Graph,
        start_date: types.temporal.Timestamp | None = None,
        end_date: types.temporal.Timestamp | None = None,
    ) -> None:
        """Creates and adds to graph, temporal coverage blank node.

        Args:
            start_date (types.temporal.Timestamp | None): Optional start date.
            end_date (types.temporal.Timestamp | None): Optional end date. At least
                one of either start_date or end_date (or both) must be supplied.
            graph (rdflib.Graph): Graph to add to.
        """
        # Ensure date was supplied
        if start_date is None and end_date is None:
            return
        # Create temporal coverage node
        temporal_coverage = rdflib.BNode()
        graph.add((temporal_coverage, a, rdflib.TIME.TemporalEntity))
        if start_date:
            begin = rdflib.BNode()
            graph.add((temporal_coverage, rdflib.TIME.hasBeginning, begin))
            graph.add((begin, a, rdflib.TIME.Instant))
            graph.add((begin, start_date.rdf_in_xsd, start_date.to_rdf_literal()))
        if end_date:
            end = rdflib.BNode()
            graph.add((temporal_coverage, rdflib.TIME.hasEnd, end))
            graph.add((end, a, rdflib.TIME.Instant))
            graph.add((end, end_date.rdf_in_xsd, end_date.to_rdf_literal()))

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


# Register Mapper
if settings.SETTINGS.MAJOR_VERSION >= 5:
    # SSD v2 is still in development, keep hidden until v5 release candidates are created
    base.mapper.ABISMapper.register_mapper(SurveySiteVisitMapper)
