"""Provides ABIS Mapper for `survey_site_visit_data-v2.0.0` template."""

# Standard
import dataclasses

# Third-party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import types
from abis_mapping import utils

# Typing
from typing import Any, Iterator


# Constants / shortcuts
a = rdflib.RDF.type
DATA_ROLE_RESOURCE_PROVIDER = rdflib.URIRef("https://linked.data.gov.au/def/data-roles/resourceProvider")
CONCEPT_TARGET_TAXONOMIC_SCOPE = rdflib.URIRef(
    "https://linked.data.gov.au/def/nrm/7ea12fed-6b87-4c20-9ab4-600b32ce15ec",
)
CONCEPT_SAMPLING_EFFORT = utils.rdf.uri("concept/samplingEffort", utils.namespaces.EXAMPLE)


@dataclasses.dataclass
class Agent:
    """Contains data items to enable producing agent nodes"""

    row_value: str
    uri: rdflib.URIRef


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
        site_visit_id_map: dict[str, bool] = kwargs.get("site_visit_id_map", {})

        # Construct schema
        schema = self.extra_fields_schema(data=data, full_schema=True)

        # Construct resource
        resource_site_visit_data = frictionless.Resource(
            source=data,
            format="csv",
            schema=schema,
            encoding="utf-8",
        )

        # Base extra custom checks
        checks = [
            plugins.tabular.IsTabular(),
            plugins.empty.NotEmpty(),
            plugins.chronological.ChronologicalOrder(
                field_names=["siteVisitStart", "siteVisitEnd"],
            ),
            plugins.logical_or.LogicalOr(
                field_names=["siteVisitStart", "siteVisitEnd"],
            ),
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["samplingEffortValue", "samplingEffortUnit"],
            ),
        ]

        # Check to see if site visit id map was provided or was empty
        if site_visit_id_map:
            # Construct foreign key map
            fk_map = {"siteVisitID": set(site_visit_id_map)}

            # Add custom check for temporal flexibility with whitelists. Here deferring
            # the check on any ids found in the occurrence template, to when validaation
            # occurs on it in line with temporal flexibility rules.
            checks += [
                plugins.required.RequiredEnhanced(
                    field_names=["siteVisitStart"],
                    whitelists=fk_map,
                )
            ]

        # Validate the site visit resource
        report: frictionless.Report = resource_site_visit_data.validate(
            checklist=frictionless.Checklist(
                checks=checks,
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
                site_visit_id: str | None = row["siteVisitID"]

                # Check for siteVisitID, even though siteVisitID is a mandatory field, it can be missing here
                # because this method is called for cross-validation, regardless of if this template is valid.
                if not site_visit_id:
                    continue

                # Temporal flexibility is dependent upon a start_date being
                # present only.
                if not start_date:
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
        if start_date is not None:
            begin = rdflib.BNode()
            graph.add((temporal_coverage, rdflib.TIME.hasBeginning, begin))
            graph.add((begin, a, rdflib.TIME.Instant))
            graph.add((begin, start_date.rdf_in_xsd, start_date.to_rdf_literal()))
        if end_date is not None:
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
        # Extract keyword arguments
        chunk_size: int | None = kwargs.get("chunk_size")
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            chunk_size = None

        # Construct Schema
        schema = self.extra_fields_schema(
            data=data,
            full_schema=True,
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
        graph_has_data: bool = False

        # Check if Dataset IRI Supplied
        if not dataset_iri:
            # Create Dataset IRI
            dataset_iri = utils.rdf.uri(f"dataset/{self.DATASET_DEFAULT_NAME}", base_iri)

            # Add the default dataset
            self.add_default_dataset(
                uri=dataset_iri,
                base_iri=base_iri,
                graph=graph,
            )
            graph_has_data = True

        # Open the Resource to allow row streaming
        with resource.open() as r:
            # Loop through rows
            for i, row in enumerate(r.row_stream, start=1):
                # Map row
                self.apply_mapping_row(
                    row=row,
                    dataset=dataset_iri,
                    graph=graph,
                    base_iri=base_iri,
                )
                graph_has_data = True

                # yield chunk if required
                if chunk_size is not None and i % chunk_size == 0:
                    yield graph
                    # Initialise New Graph for next chunk
                    graph = utils.rdf.create_graph()
                    graph_has_data = False

            # yield final chunk, or whole graph if not chunking.
            if chunk_size is None or graph_has_data:
                yield graph

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: rdflib.Namespace | None,
    ) -> None:
        """Applies mapping for a row in the Survey Site Visit Data template.

        Args:
            row: Row to be processed in the dataset.
            dataset: Dataset IRI this row is a part of.
            graph: Graph to map row into.
            base_iri: Optional base IRI to use for mapping.
        """
        # variables starting with row_ are values from the row.
        # variables starting with uri_ are constructed URIs.

        row_site_visit_id: str | None = row["siteVisitID"]
        row_site_id: str | None = row["siteID"]
        # should always have these mandatory fields, skip if not
        if not row_site_visit_id:
            return
        if not row_site_id:
            return

        # Part 1: Construct URIs from Row

        # URIs for the Site Visit and the Site
        uri_site_visit_activity = utils.rdf.extend_uri_quoted(dataset, "visit", row_site_visit_id)
        uri_site = utils.rdf.extend_uri_quoted(dataset, "Site", row_site_id)

        # URI for the Survey
        row_survey_id: str | None = row["surveyID"]
        if row_survey_id:
            uri_survey = utils.rdf.uri(f"survey/SSD-Survey/{row_survey_id}")
        else:
            uri_survey = utils.rdf.uri("survey/SSD-Survey/1", base_iri)

        # URI for the Site Visit Plan
        uri_site_visit_plan = utils.rdf.extend_uri_quoted(dataset, "visit", "plan", row_site_visit_id)

        # URIs based on the siteIDSource
        row_site_id_source: str | None = row["siteIDSource"]
        if row_site_id_source:
            uri_site_id_datatype = utils.rdf.extend_uri_quoted(dataset, "datatype", "siteVisitID", row_site_id_source)
            uri_site_id_datatype_attribution = utils.rdf.extend_uri_quoted(
                dataset, "attribution", row_site_id_source, "resourceProvider"
            )
            uri_site_id_datatype_agent = utils.rdf.extend_uri_quoted(dataset, "agent", row_site_id_source)
        else:
            uri_site_id_datatype = None
            uri_site_id_datatype_attribution = None
            uri_site_id_datatype_agent = None

        # Create Agents for each visit Org
        row_visit_orgs: list[str] | None = row["visitOrgs"]
        visit_org_agents: list[Agent]
        if row_visit_orgs:
            visit_org_agents = [
                Agent(
                    row_value=visit_org,
                    uri=utils.rdf.extend_uri(dataset, "agent", visit_org),
                )
                for visit_org in row_visit_orgs
            ]
        else:
            visit_org_agents = []

        # Create Agents for each visit Observer
        row_visit_observers: list[str] | None = row["visitObservers"]
        visit_observer_agents: list[Agent]
        if row_visit_observers:
            visit_observer_agents = [
                Agent(
                    row_value=visit_observer,
                    uri=utils.rdf.extend_uri(dataset, "agent", visit_observer),
                )
                for visit_observer in row_visit_observers
            ]
        else:
            visit_observer_agents = []

        # Conditionally create Attribute and Value for targetTaxonomicScope
        row_target_taxonomic_scope: str | None = row["targetTaxonomicScope"]
        if row_target_taxonomic_scope:
            uri_target_taxonomic_scope_attribute = utils.rdf.extend_uri(
                dataset, "attribute", "targetTaxonomicScope", row_target_taxonomic_scope
            )
            uri_target_taxonomic_scope_value = utils.rdf.extend_uri(
                dataset, "value", "targetTaxonomicScope", row_target_taxonomic_scope
            )
            uri_target_taxonomic_scope_collection = utils.rdf.extend_uri(
                dataset, "collection", "targetTaxonomicScope", row_target_taxonomic_scope
            )
        else:
            uri_target_taxonomic_scope_attribute = None
            uri_target_taxonomic_scope_value = None
            uri_target_taxonomic_scope_collection = None

        # Conditionally create Attribute and Value for samplingEffort
        row_sampling_effort_value: str | None = row["samplingEffortValue"]
        row_sampling_effort_unit: str | None = row["samplingEffortUnit"]
        if row_sampling_effort_value and row_sampling_effort_unit:
            row_sampling_effort = f"{row_sampling_effort_value} {row_sampling_effort_unit}"
            uri_sampling_effort_attribute = utils.rdf.extend_uri(
                dataset, "attribute", "samplingEffort", row_sampling_effort
            )
            uri_sampling_effort_value = utils.rdf.extend_uri(dataset, "value", "samplingEffort", row_sampling_effort)
            uri_sampling_effort_collection = utils.rdf.extend_uri(
                dataset, "collection", "samplingEffort", row_sampling_effort
            )
        else:
            row_sampling_effort = None
            uri_sampling_effort_attribute = None
            uri_sampling_effort_value = None
            uri_sampling_effort_collection = None

        # Part 2: Construct mapping from row data and URIs

        # Add Site Visit Activity
        self.add_site_visit_activity(
            uri=uri_site_visit_activity,
            row_site_visit_id=row_site_visit_id,
            row_site_id=row_site_id,
            uri_survey=uri_survey,
            uri_site=uri_site,
            uri_site_visit_plan=uri_site_visit_plan,
            uri_site_id_datatype=uri_site_id_datatype,
            visit_org_agents=visit_org_agents,
            visit_observer_agents=visit_observer_agents,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add site id datatype, attribution and agent
        self.add_site_id_datatype(
            uri=uri_site_id_datatype,
            row_site_id_source=row_site_id_source,
            uri_site_id_datatype_attribution=uri_site_id_datatype_attribution,
            graph=graph,
        )
        self.add_site_id_datatype_attribution(
            uri=uri_site_id_datatype_attribution,
            uri_site_id_datatype_agent=uri_site_id_datatype_agent,
            graph=graph,
        )
        self.add_site_id_datatype_agent(
            uri=uri_site_id_datatype_agent,
            row_site_id_source=row_site_id_source,
            graph=graph,
        )

        # Add visitOrgs Agents
        for visit_org_agent in visit_org_agents:
            self.add_visit_org_agent(
                uri=visit_org_agent.uri,
                row_visit_org=visit_org_agent.row_value,
                graph=graph,
            )

        # Add visitObservers Agents
        for visit_observer_agent in visit_observer_agents:
            self.add_visit_observer_agent(
                uri=visit_observer_agent.uri,
                row_visit_observer=visit_observer_agent.row_value,
                graph=graph,
            )

        # Add site visit plan
        self.add_site_visit_plan(
            uri=uri_site_visit_plan,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add targetTaxonomicScope Attribute, Value and Collection
        self.add_target_taxonomic_scope_attribute(
            uri=uri_target_taxonomic_scope_attribute,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            uri_target_taxonomic_scope_value=uri_target_taxonomic_scope_value,
            dataset=dataset,
            graph=graph,
        )
        self.add_target_taxonomic_scope_value(
            uri=uri_target_taxonomic_scope_value,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            dataset=dataset,
            graph=graph,
        )
        self.add_target_taxonomic_scope_collection(
            uri=uri_target_taxonomic_scope_collection,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            uri_target_taxonomic_scope_attribute=uri_target_taxonomic_scope_attribute,
            uri_site_visit_activity=uri_site_visit_activity,
            dataset=dataset,
            graph=graph,
        )

        # Add samplingEffort Attribute, Value and Collection
        self.add_sampling_effort_attribute(
            uri=uri_sampling_effort_attribute,
            row_sampling_effort=row_sampling_effort,
            uri_sampling_effort_value=uri_sampling_effort_value,
            dataset=dataset,
            graph=graph,
        )
        self.add_sampling_effort_value(
            uri=uri_sampling_effort_value,
            row_sampling_effort_value=row_sampling_effort_value,
            row_sampling_effort_unit=row_sampling_effort_unit,
            dataset=dataset,
            graph=graph,
        )
        self.add_sampling_effort_collection(
            uri=uri_sampling_effort_collection,
            row_sampling_effort=row_sampling_effort,
            uri_sampling_effort_attribute=uri_sampling_effort_attribute,
            uri_site_visit_activity=uri_site_visit_activity,
            dataset=dataset,
            graph=graph,
        )

    def add_site_visit_activity(
        self,
        *,
        uri: rdflib.URIRef,
        row_site_visit_id: str,
        row_site_id: str,
        uri_survey: rdflib.URIRef,
        uri_site: rdflib.URIRef,
        uri_site_visit_plan: rdflib.URIRef,
        uri_site_id_datatype: rdflib.URIRef | None,
        visit_org_agents: list[Agent],
        visit_observer_agents: list[Agent],
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.SiteVisit))
        # Add dataset link
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # Add survey link
        graph.add((uri, rdflib.SDO.isPartOf, uri_survey))
        # Add site link
        graph.add((uri, utils.namespaces.TERN.hasSite, uri_site))
        if uri_site_id_datatype and row_site_id:
            graph.add((uri, utils.namespaces.TERN.hasSite, rdflib.Literal(row_site_id, datatype=uri_site_id_datatype)))

        # Add identifier
        graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(row_site_visit_id)))

        # Add temporal entity for start/end time
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.TemporalEntity))
        row_site_visit_start: types.temporal.Timestamp | None = row["siteVisitStart"]
        row_site_visit_end: types.temporal.Timestamp | None = row["siteVisitEnd"]
        if row_site_visit_start:
            start_instant = rdflib.BNode()
            graph.add((start_instant, a, rdflib.TIME.Instant))
            graph.add((start_instant, row_site_visit_start.rdf_in_xsd, row_site_visit_start.to_rdf_literal()))
            graph.add((temporal_entity, rdflib.TIME.hasBeginning, start_instant))
        if row_site_visit_end:
            end_instant = rdflib.BNode()
            graph.add((end_instant, a, rdflib.TIME.Instant))
            graph.add((end_instant, row_site_visit_end.rdf_in_xsd, row_site_visit_end.to_rdf_literal()))
            graph.add((temporal_entity, rdflib.TIME.hasEnd, end_instant))

        # Add link(s) to visitOrgs
        for visit_org_agent in visit_org_agents:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, visit_org_agent.uri))

        # Add link(s) to visitObservers
        for visit_observer_agent in visit_observer_agents:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, visit_observer_agent.uri))

        # Add condition
        row_condition: str | None = row["condition"]
        if row_condition:
            graph.add((uri, utils.namespaces.TERN.siteDescription, rdflib.Literal(row_condition)))

        # Add link to Site Visit Plan
        graph.add((uri, rdflib.PROV.hadPlan, uri_site_visit_plan))

    def add_site_id_datatype(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_site_id_source: str | None,
        uri_site_id_datatype_attribution: rdflib.URIRef | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site id datatype to the graph.

        Args:
            uri: Subject of the node.
            row_site_id_source: The siteIDSource value from the row.
            uri_site_id_datatype_attribution: The datatype attribution node.
            graph: Graph to be modified.
        """
        # Check subject was provided
        if uri is None:
            return
        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))
        # Add definition
        graph.add((uri, rdflib.SKOS.definition, rdflib.Literal("An identifier for the site")))
        # Add label
        if row_site_id_source:
            graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{row_site_id_source} Site ID")))
        # Add attribution link
        if uri_site_id_datatype_attribution:
            graph.add((uri, rdflib.PROV.qualifiedAttribution, uri_site_id_datatype_attribution))

    def add_site_id_datatype_attribution(
        self,
        *,
        uri: rdflib.URIRef | None,
        uri_site_id_datatype_agent: rdflib.URIRef | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site id datatype attribution to the graph.

        Args:
            uri: Suject of the node
            uri_site_id_datatype_agent: The datatype agent node.
            graph: The graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return
        # Add type
        graph.add((uri, a, rdflib.PROV.Attribution))
        # Add role
        graph.add((uri, rdflib.PROV.hadRole, DATA_ROLE_RESOURCE_PROVIDER))
        # Add agent link
        if uri_site_id_datatype_agent:
            graph.add((uri, rdflib.PROV.agent, uri_site_id_datatype_agent))

    def add_site_id_datatype_agent(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_site_id_source: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the site id datatype agent to the graph.

        Args:
            uri: Subject of the node.
            row_site_id_source: The siteIDSource value from the row.
            graph: Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return
        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))
        # Add name
        if row_site_id_source:
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(row_site_id_source)))

    def add_visit_org_agent(
        self,
        *,
        uri: rdflib.URIRef,
        row_visit_org: str,
        graph: rdflib.Graph,
    ) -> None:
        """Add a visit Org Agent node to the graph.

        Args:
            uri: The URI for this agent
            row_visit_org: One of the values from the visitOrgs field
            graph: The graph to be modified.
        """
        # Add subject types
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, a, rdflib.PROV.Organization))
        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row_visit_org)))

    def add_visit_observer_agent(
        self,
        *,
        uri: rdflib.URIRef,
        row_visit_observer: str,
        graph: rdflib.Graph,
    ) -> None:
        """Add a visit Observer Agent node to the graph.

        Args:
            uri: The URI for this agent
            row_visit_observer: One of the values from the visitObservers field
            graph: The graph to be modified.
        """
        # Add subject types
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, a, rdflib.PROV.Person))
        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row_visit_observer)))

    def add_site_visit_plan(
        self,
        *,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        # Add subject type
        graph.add((uri, a, rdflib.PROV.Plan))

        # Add description
        row_protocol_description: str | None = row["protocolDescription"]
        if row_protocol_description:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(row_protocol_description)))

        # Add used procedure
        row_protocol_name: str | None = row["protocolName"]
        if row_protocol_name:
            # Retrieve vocab for field
            vocab = self.fields()["protocolName"].get_vocab()
            # get or create term IRI
            term = vocab(graph=graph, source=dataset).get(row_protocol_name)
            # Add link to term
            graph.add((uri, rdflib.SOSA.usedProcedure, term))

    def add_target_taxonomic_scope_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_target_taxonomic_scope: str | None,
        uri_target_taxonomic_scope_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add the target taxonomic scope Attribute node.

        Args:
            uri: Subject of the node.
            row_target_taxonomic_scope: Raw data in the targetTaxonomicScope field.
            uri_target_taxonomic_scope_value: The target taxonomic scope Value node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject is provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add attribute concept
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_TARGET_TAXONOMIC_SCOPE))

        # Add values
        if row_target_taxonomic_scope:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row_target_taxonomic_scope)))
        if uri_target_taxonomic_scope_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, uri_target_taxonomic_scope_value))

    def add_target_taxonomic_scope_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_target_taxonomic_scope: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the target taxonomic scope Attribute Value node.

        Args:
            uri: Subject of the node.
            row_target_taxonomic_scope: Raw data in the targetTaxonomicScope field.
            dataset: Dataset raw data belongs.
            graph: Graph to be modified.
        """
        # check subject is provided
        if uri is None:
            return

        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if row_target_taxonomic_scope:
            # Retrieve vocab for field
            vocab = self.fields()["targetTaxonomicScope"].get_vocab()

            # Add value
            term = vocab(graph=graph, source=dataset).get(row_target_taxonomic_scope)
            graph.add((uri, rdflib.RDF.value, term))

    def add_target_taxonomic_scope_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_target_taxonomic_scope: str | None,
        uri_target_taxonomic_scope_attribute: rdflib.URIRef | None,
        uri_site_visit_activity: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add a target taxonomic scope Collection to the graph

        Args:
            uri: The uri for the Collection.
            row_target_taxonomic_scope: targetTaxonomicScope value from template.
            uri_target_taxonomic_scope_attribute: The uri for the attribute node.
            uri_site_visit_activity: The Site Visit node that should be a member of the collection.
            dataset: The uri for the dateset node.
            graph: The graph.
        """
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        if row_target_taxonomic_scope:
            graph.add(
                (
                    uri,
                    rdflib.SDO.identifier,
                    rdflib.Literal(f"Site Visit Collection - Target Taxonomic Scope - {row_target_taxonomic_scope}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # add link to the SiteVisit node
        graph.add((uri, rdflib.SDO.member, uri_site_visit_activity))
        # Add link to attribute
        if uri_target_taxonomic_scope_attribute is not None:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, uri_target_taxonomic_scope_attribute))

    def add_sampling_effort_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_sampling_effort: str | None,
        uri_sampling_effort_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds sampling effort Attribute node.

        Args:
            uri: Subject of the node.
            row_sampling_effort: Combination of samplingEffortValue and samplingEffortUnit fields
            uri_sampling_effort_value: URI of the Attribute Value node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check that subject is provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add concept
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_SAMPLING_EFFORT))

        # Add values
        if row_sampling_effort:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row_sampling_effort)))
        if uri_sampling_effort_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, uri_sampling_effort_value))

    def add_sampling_effort_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_sampling_effort_value: str | None,
        row_sampling_effort_unit: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds sampling effort Attribute Value node.

        Args:
            uri: Subject of the node.
            row_sampling_effort_value: Value from the samplingEffortValue field.
            row_sampling_effort_unit: Value from the samplingEffortUnit field.
            dataset (rdflib.URIRef): URI of the dataset this belongs to.
            graph (rdflib.Graph): Graph to be modified.
        """
        if uri is None:
            return

        # Add types
        graph.add((uri, a, utils.namespaces.TERN.Float))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add value
        if row_sampling_effort_value:
            graph.add((uri, rdflib.RDF.value, rdflib.Literal(row_sampling_effort_value, datatype=rdflib.XSD.float)))

        # Add Unit
        if row_sampling_effort_unit:
            # Retrieve vocab for field
            vocab = self.fields()["samplingEffortUnit"].get_vocab()
            # Add value
            term = vocab(graph=graph, source=dataset).get(row_sampling_effort_unit)
            graph.add((uri, utils.namespaces.TERN.unit, term))

    def add_sampling_effort_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_sampling_effort: str | None,
        uri_sampling_effort_attribute: rdflib.URIRef | None,
        uri_site_visit_activity: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add a sampling effort Collection to the graph

        Args:
            uri: The uri for the Collection.
            row_sampling_effort: Combined samplingEffort value from template.
            uri_sampling_effort_attribute: The uri for the attribute node.
            uri_site_visit_activity: The Site Visit node that should be a member of the collection.
            dataset: The uri for the dateset node.
            graph: The graph.
        """
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        if row_sampling_effort:
            graph.add(
                (
                    uri,
                    rdflib.SDO.identifier,
                    rdflib.Literal(f"Site Visit Collection - Sampling Effort - {row_sampling_effort}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # add link to the SiteVisit node
        graph.add((uri, rdflib.SDO.member, uri_site_visit_activity))
        # Add link to attribute
        if uri_sampling_effort_attribute is not None:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, uri_sampling_effort_attribute))


# Register Mapper
base.mapper.ABISMapper.register_mapper(SurveySiteVisitMapper)
