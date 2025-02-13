"""Provides ABIS Mapper for `survey_site_visit_data-v3.0.0` template."""

# Standard
import dataclasses

# Third-party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import models
from abis_mapping import utils

# Typing
from typing import Any


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
    """ABIS mapper for the v3 survey site visit data csv template."""

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
            survey_id_set (Set[str]): Set of surveyIDs from the metadata template.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
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
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["siteID", "siteIDSource"],
            ),
            plugins.site_id_or_iri_validation.SiteIdentifierCheck(),
            plugins.chronological.ChronologicalOrder(
                field_names=["siteVisitStart", "siteVisitEnd"],
            ),
            plugins.mutual_inclusion.MutuallyInclusive(
                field_names=["samplingEffortValue", "samplingEffortUnit"],
            ),
        ]

        if "survey_id_set" in kwargs:
            checks.append(
                plugins.survey_id_validation.SurveyIDValidation(
                    valid_survey_ids=kwargs["survey_id_set"],
                )
            )

        # Validate the site visit resource
        report: frictionless.Report = resource_site_visit_data.validate(
            checklist=frictionless.Checklist(
                checks=checks,
            ),
        )

        # Return validation report
        return report

    def extract_site_visit_id_to_site_id_map(
        self,
        data: base.types.ReadableType,
    ) -> dict[str, models.identifier.SiteIdentifier | None]:
        """Constructs a dictionary mapping site visit id to SiteIdentifier.

        Args:
            data: Raw data to be mapped.

        Returns:
            Map with site visit id for keys and SiteIdentifier for values,
            or None for value if there is no identifier.
        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct resource
        resource = frictionless.Resource(source=data, format="csv", schema=schema, encoding="utf-8")

        # Declare result reference
        result: dict[str, models.identifier.SiteIdentifier | None] = {}

        # Context manager for row streaming
        with resource.open() as r:
            for row in r.row_stream:
                # Check that the cells have values and add to map
                site_visit_id: str | None = row["siteVisitID"]
                site_identifier = models.identifier.SiteIdentifier.from_row(row)
                # Put siteVisitID in the map, even when site_identifier is None,
                # So the other templates have access to all the provided siteVisitIDs.
                # This lets other templates differentiate between 'a siteVisitID not in this template',
                # and 'a siteVisitID in this template but with no Site identifier'.
                if site_visit_id:
                    result[site_visit_id] = site_identifier

        # Return
        return result

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
                # Extract values from row.
                start_date: models.temporal.Timestamp | None = row["siteVisitStart"]
                end_date: models.temporal.Timestamp | None = row["siteVisitEnd"]
                site_visit_id: str | None = row["siteVisitID"]

                # Check for siteVisitID, even though siteVisitID is a mandatory field, it can be missing here
                # because this method is called for cross-validation, regardless of if this template is valid.
                if not site_visit_id:
                    continue

                # Temporal flexibility is dependent upon a start_date being present only.
                # Again, even though siteVisitStart is a mandatory field, it can be None here
                # because this method is called for cross-validation, regardless of if this template is valid.
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
        *,
        graph: rdflib.Graph,
        start_date: models.temporal.Timestamp,
        end_date: models.temporal.Timestamp | None,
    ) -> None:
        """Creates and adds to graph, temporal coverage blank node.

        Args:
            start_date: start date.
            end_date: Optional end date.
            graph: Graph to add to.
        """
        # Create temporal coverage node
        temporal_coverage = rdflib.BNode()
        graph.add((temporal_coverage, a, rdflib.TIME.TemporalEntity))
        begin = rdflib.BNode()
        graph.add((temporal_coverage, rdflib.TIME.hasBeginning, begin))
        graph.add((begin, a, rdflib.TIME.Instant))
        graph.add((begin, start_date.rdf_in_xsd, start_date.to_rdf_literal()))
        if end_date is not None:
            end = rdflib.BNode()
            graph.add((temporal_coverage, rdflib.TIME.hasEnd, end))
            graph.add((end, a, rdflib.TIME.Instant))
            graph.add((end, end_date.rdf_in_xsd, end_date.to_rdf_literal()))

    def apply_mapping_row(
        self,
        *,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        extra_schema: frictionless.Schema,
        base_iri: rdflib.Namespace,
        submission_iri: rdflib.URIRef | None,
        **kwargs: Any,
    ) -> None:
        """Applies mapping for a row in the Survey Site Visit Data template.

        Args:
            row: Row to be processed in the dataset.
            dataset: Dataset IRI this row is a part of.
            graph: Graph to map row into.
            extra_schema: Schema of extra fields.
            base_iri: Base IRI to use for mapping.
            submission_iri: Submission IRI to use for mapping.
        """
        # variables starting with row_ are values from the row.
        # variables starting with uri_ are constructed URIs.

        row_site_visit_id: str | None = row["siteVisitID"]
        # should always have these mandatory fields, skip if not
        if not row_site_visit_id:
            return

        # Part 1: Construct URIs from Row

        # Create TERN.SiteVisit subject IRI - Note this needs to match the iri construction of the
        # survey occurrence template mapping, ensuring they will resolve properly.
        uri_site_visit_activity = utils.iri_patterns.site_visit_iri(base_iri, row_site_visit_id)

        # TERN.Site subject IRI - Note this needs to match the iri construction of the
        # survey site and occurrence template mapping, ensuring they will resolve properly.
        # If existingBDRSiteIRI is specified, just use that as-is for the IRI.
        row_site_id: str | None = row["siteID"]
        row_site_id_source: str | None = row["siteIDSource"]
        row_existing_site_iri: str | None = row["existingBDRSiteIRI"]
        if row_existing_site_iri:
            uri_site = rdflib.URIRef(row_existing_site_iri)
        elif row_site_id and row_site_id_source:
            uri_site = utils.iri_patterns.site_iri(row_site_id_source, row_site_id)
        else:
            raise ValueError("Invalid row missing SiteID and existingBDRSiteIRI")

        # Create TERN survey IRI from surveyID field
        row_survey_id: str = row["surveyID"]
        uri_survey = utils.iri_patterns.survey_iri(base_iri, row_survey_id)

        # URI for the Site Visit Plan
        uri_site_visit_plan = utils.iri_patterns.plan_iri(base_iri, "visit", row_site_visit_id)

        # When siteID+siteIDSource are provided,
        # the site gets a schema:identifier with this datatype.
        if row_site_id and row_site_id_source:
            uri_site_id_datatype = utils.iri_patterns.datatype_iri("siteID", row_site_id_source)
            uri_site_id_datatype_attribution = utils.iri_patterns.attribution_iri(
                "resourceProvider", row_site_id_source
            )
            uri_site_id_datatype_agent = utils.iri_patterns.agent_iri("org", row_site_id_source)
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
                    uri=utils.iri_patterns.agent_iri("org", visit_org),
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
                    uri=utils.iri_patterns.agent_iri("person", visit_observer),
                )
                for visit_observer in row_visit_observers
            ]
        else:
            visit_observer_agents = []

        # Conditionally create Attribute and Value for targetTaxonomicScope
        row_target_taxonomic_scope: str | None = row["targetTaxonomicScope"]
        if row_target_taxonomic_scope:
            uri_target_taxonomic_scope_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "targetTaxonomicScope", row_target_taxonomic_scope
            )
            uri_target_taxonomic_scope_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "targetTaxonomicScope", row_target_taxonomic_scope
            )
            uri_target_taxonomic_scope_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "SiteVisit", "targetTaxonomicScope", row_target_taxonomic_scope
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
            uri_sampling_effort_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "samplingEffort", row_sampling_effort
            )
            uri_sampling_effort_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "samplingEffort", row_sampling_effort
            )
            uri_sampling_effort_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "SiteVisit", "samplingEffort", row_sampling_effort
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
            uri_survey=uri_survey,
            uri_site=uri_site,
            uri_site_visit_plan=uri_site_visit_plan,
            visit_org_agents=visit_org_agents,
            visit_observer_agents=visit_observer_agents,
            row=row,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add survey
        self.add_survey(uri=uri_survey, dataset=dataset, graph=graph, submission_iri=submission_iri)

        # Add site
        self.add_site(
            uri=uri_site,
            uri_site_id_datatype=uri_site_id_datatype,
            submission_iri=submission_iri,
            row_site_id=row_site_id,
            row_existing_site_iri=row_existing_site_iri,
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
            base_iri=base_iri,
        )

        # Add targetTaxonomicScope Attribute, Value and Collection
        self.add_target_taxonomic_scope_attribute(
            uri=uri_target_taxonomic_scope_attribute,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            uri_target_taxonomic_scope_value=uri_target_taxonomic_scope_value,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )
        self.add_target_taxonomic_scope_value(
            uri=uri_target_taxonomic_scope_value,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            dataset=dataset,
            graph=graph,
            base_iri=base_iri,
        )
        self.add_target_taxonomic_scope_collection(
            uri=uri_target_taxonomic_scope_collection,
            row_target_taxonomic_scope=row_target_taxonomic_scope,
            uri_target_taxonomic_scope_attribute=uri_target_taxonomic_scope_attribute,
            uri_site_visit_activity=uri_site_visit_activity,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add samplingEffort Attribute, Value and Collection
        self.add_sampling_effort_attribute(
            uri=uri_sampling_effort_attribute,
            row_sampling_effort=row_sampling_effort,
            uri_sampling_effort_value=uri_sampling_effort_value,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )
        self.add_sampling_effort_value(
            uri=uri_sampling_effort_value,
            row_sampling_effort_value=row_sampling_effort_value,
            row_sampling_effort_unit=row_sampling_effort_unit,
            dataset=dataset,
            graph=graph,
            base_iri=base_iri,
        )
        self.add_sampling_effort_collection(
            uri=uri_sampling_effort_collection,
            row_sampling_effort=row_sampling_effort,
            uri_sampling_effort_attribute=uri_sampling_effort_attribute,
            uri_site_visit_activity=uri_site_visit_activity,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add extra fields
        self.add_extra_fields_json(
            subject_uri=uri_site_visit_activity,
            row=row,
            graph=graph,
            extra_schema=extra_schema,
        )

    def add_site_visit_activity(
        self,
        *,
        uri: rdflib.URIRef,
        row_site_visit_id: str,
        uri_survey: rdflib.URIRef,
        uri_site: rdflib.URIRef,
        uri_site_visit_plan: rdflib.URIRef,
        visit_org_agents: list[Agent],
        visit_observer_agents: list[Agent],
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.SiteVisit))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset link
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add survey link
        graph.add((uri, rdflib.SDO.isPartOf, uri_survey))
        # Add site link
        graph.add((uri, utils.namespaces.TERN.hasSite, uri_site))

        # Add identifier
        graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(row_site_visit_id)))

        # Add temporal entity for start/end time
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.TemporalEntity))
        row_site_visit_start: models.temporal.Timestamp = row["siteVisitStart"]
        row_site_visit_end: models.temporal.Timestamp | None = row["siteVisitEnd"]
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

    def add_survey(
        self, uri: rdflib.URIRef, dataset: rdflib.URIRef, graph: rdflib.Graph, submission_iri: rdflib.URIRef | None
    ) -> None:
        """Adds the basics of the Survey node to the graph.

        The other properties for the node come from the survey metadata.

        Args:
            uri: The URI for the Survey node
            dataset: The dataset URI
            graph: The graph to update
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Survey))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset link
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

    def add_site(
        self,
        *,
        uri: rdflib.URIRef,
        uri_site_id_datatype: rdflib.URIRef | None,
        submission_iri: rdflib.URIRef | None,
        row_site_id: str | None,
        row_existing_site_iri: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site to the graph.

        Args:
            uri: Subject of the node.
            uri_site_id_datatype: Datatype of the site
                id source.
            submission_iri: IRI of the submission being mapped.
            row_site_id: siteID field from the template.
            row_existing_site_iri: existingBDRSiteIRI field from the template.
            graph: Graph to be modified.
        """
        # Add class
        graph.add((uri, a, utils.namespaces.TERN.Site))

        # Add link to submission only when the Site is not an existing Site.
        if not row_existing_site_iri:
            if submission_iri:
                graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add siteID schema:identifier property, when siteID+siteIDSource are provided.
        if row_site_id and uri_site_id_datatype is not None:
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(row_site_id, datatype=uri_site_id_datatype)))

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
        base_iri: rdflib.Namespace,
    ) -> None:
        """Add a site visit prov:Plan node to the graph.

        Args:
            uri: The URI for the site visit plan
            row: Raw row from the template.
            dataset: Dataset raw data belongs to.
            graph: The graph to be modified.
            base_iri: Namespace used to construct IRIs
        """
        # Add subject type
        graph.add((uri, a, rdflib.PROV.Plan))

        # add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add description
        row_protocol_description: str | None = row["protocolDescription"]
        if row_protocol_description:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(row_protocol_description)))

        # Add used procedure
        row_protocol_name: str | None = row["protocolName"]
        if row_protocol_name:
            # Retrieve vocab for field
            vocab = self.fields()["protocolName"].get_flexible_vocab()
            # get or create term IRI
            term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(row_protocol_name)
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
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

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
        base_iri: rdflib.Namespace,
    ) -> None:
        """Adds the target taxonomic scope Attribute Value node.

        Args:
            uri: Subject of the node.
            row_target_taxonomic_scope: Raw data in the targetTaxonomicScope field.
            dataset: Dataset raw data belongs.
            graph: Graph to be modified.
            base_iri: Namespace used to construct IRIs
        """
        # check subject is provided
        if uri is None:
            return

        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if row_target_taxonomic_scope:
            # Retrieve vocab for field
            vocab = self.fields()["targetTaxonomicScope"].get_flexible_vocab()

            # Add value
            term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(row_target_taxonomic_scope)
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
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add identifier
        if row_target_taxonomic_scope:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Site Visit Collection - Target Taxonomic Scope - {row_target_taxonomic_scope}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
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
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

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
        base_iri: rdflib.Namespace,
    ) -> None:
        """Adds sampling effort Attribute Value node.

        Args:
            uri: Subject of the node.
            row_sampling_effort_value: Value from the samplingEffortValue field.
            row_sampling_effort_unit: Value from the samplingEffortUnit field.
            dataset (rdflib.URIRef): URI of the dataset this belongs to.
            graph (rdflib.Graph): Graph to be modified.
            base_iri (rdflib.Namespace): Namespace used to construct IRIs
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
            vocab = self.fields()["samplingEffortUnit"].get_flexible_vocab()
            # Add value
            term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(row_sampling_effort_unit)
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
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add identifier
        if row_sampling_effort:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Site Visit Collection - Sampling Effort - {row_sampling_effort}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the SiteVisit node
        graph.add((uri, rdflib.SDO.member, uri_site_visit_activity))
        # Add link to attribute
        if uri_sampling_effort_attribute is not None:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, uri_sampling_effort_attribute))


# Register Mapper
base.mapper.register_mapper(SurveySiteVisitMapper)
