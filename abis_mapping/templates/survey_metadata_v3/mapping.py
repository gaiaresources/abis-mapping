"""Provides ABIS mapper for `survey_metadata.csv` template v3"""

# Standard
import dataclasses

# Third-party
import frictionless
import frictionless.checks
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import models
from abis_mapping import utils

# Typing
from typing import Any, Literal

# Constants / shortcuts
a = rdflib.RDF.type
PRINCIPAL_INVESTIGATOR = rdflib.URIRef("https://linked.data.gov.au/def/data-roles/principalInvestigator")
CONCEPT_SURVEY_TYPE = utils.rdf.uri("concept/surveyType", utils.namespaces.EXAMPLE)
CONCEPT_TARGET_HABITAT_SCOPE = rdflib.URIRef("https://linked.data.gov.au/def/nrm/ae2c88be-63d5-44d3-95ac-54b14c4a4b28")
CONCEPT_TARGET_TAXONOMIC_SCOPE = rdflib.URIRef(
    "https://linked.data.gov.au/def/nrm/7ea12fed-6b87-4c20-9ab4-600b32ce15ec",
)


# Dataclass used in mapping
@dataclasses.dataclass
class SurveyIDDatatype:
    """Contains data items for a survey organisation"""

    name: str
    datatype: rdflib.URIRef
    attribution: rdflib.URIRef
    agent: rdflib.URIRef


@dataclasses.dataclass
class AttributeValue:
    """Contains data items to enable producing attribute, value and collection nodes"""

    raw: str
    attribute: rdflib.URIRef
    value: rdflib.URIRef
    collection: rdflib.URIRef


class SurveyMetadataMapper(base.mapper.ABISMapper):
    """ABIS mapper for `survey_metadata.csv` v3"""

    def apply_validation(self, data: base.types.ReadableType, **kwargs: Any) -> frictionless.Report:
        """Applies Frictionless validation for the 'survey_metadata.csv' template

        Args:
            data (base.types.ReadableType): Raw data to be validated
            **kwargs (Any): Additional keyword arguments.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
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

        # Validate
        report: frictionless.Report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra Custom Checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    plugins.chronological.ChronologicalOrder(
                        field_names=[
                            "surveyStart",
                            "surveyEnd",
                        ]
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=[
                            "spatialCoverageWKT",
                            "geodeticDatum",
                        ]
                    ),
                ],
            ),
        )

        # Return validation report
        return report

    def extract_survey_id_set(
            self,
            data: base.types.ReadableType,
    ) -> dict[str, Literal[True]]:
        """Extract surveyID values from the template

        Args:
            data (base.types.ReadableType): Raw data.

        Returns:
            The set of surveyID values, as a dict.
        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct resource
        resource = frictionless.Resource(
            source=data,
            format="csv",
            schema=schema,
            encoding="utf-8",
        )

        survey_ids: dict[str, Literal[True]] = {}

        # Iterate over rows to extract values
        with resource.open() as r:
            for row in r.row_stream:
                survey_id: str | None = row["surveyID"]
                if survey_id:
                    survey_ids[survey_id] = True

        return survey_ids

    def apply_mapping_row(
            self,
            *,
            row: frictionless.Row,
            dataset: rdflib.URIRef,
            graph: rdflib.Graph,
            extra_schema: frictionless.Schema,
            base_iri: rdflib.Namespace,
            submission_iri: rdflib.URIRef | None,
            project_iri: rdflib.URIRef | None,
            **kwargs: Any,
    ) -> None:
        """Applies mapping for a row in the `survey_metadata.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            extra_schema (frictionless.Schema): Schema of extra fields.
            base_iri (rdflib.Namespace): Base IRI to use for mapping.
            submission_iri: The Submission IRI to use for mapping.
            project_iri: The abis:Project IRI if there is one.
        """
        # Set the row number to start from the data, excluding header
        row_num = row.row_number - 1

        if submission_iri is None:
            # Legacy: When using the metadata form v1, Create BDR project IRI
            project_iri = utils.rdf.uri(f"project/SSD-Survey-Project/{row_num}", base_iri)
        else:
            # When using metadata form v2, Use project_iri as-is, Can be None when no Project in Form.
            pass

        # Create TERN survey IRI from surveyID field
        survey_id: str = row["surveyID"]
        survey = utils.iri_patterns.survey_iri(base_iri, survey_id)

        # Create survey plan IRI
        survey_plan = utils.iri_patterns.plan_iri(
            base_iri,
            "survey",
            survey_id,
        )

        # Conditionally create survey type attribute, value and collection IRIs
        row_survey_type: str | None = row["surveyType"]
        if row_survey_type:
            survey_type_attribute = utils.iri_patterns.attribute_iri(base_iri, "surveyType", row_survey_type)
            survey_type_value = utils.iri_patterns.attribute_value_iri(base_iri, "surveyType", row_survey_type)
            survey_type_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Survey", "surveyType", row_survey_type
            )
        else:
            survey_type_attribute = None
            survey_type_value = None
            survey_type_collection = None

        # Create target habitat scope attribute and value objects
        target_habitat_objects: list[AttributeValue] = []
        if target_habitats := row["targetHabitatScope"]:
            for target_habitat in target_habitats:
                target_habitat_objects.append(
                    AttributeValue(
                        raw=target_habitat,
                        attribute=utils.iri_patterns.attribute_iri(base_iri, "targetHabitatScope", target_habitat),
                        value=utils.iri_patterns.attribute_value_iri(base_iri, "targetHabitatScope", target_habitat),
                        collection=utils.iri_patterns.attribute_collection_iri(
                            base_iri, "Survey", "targetHabitatScope", target_habitat
                        ),
                    ),
                )

        # Create target taxonomic scope attribute and value IRIs (list input)
        target_taxonomic_objects: list[AttributeValue] = []
        if target_taxa := row["targetTaxonomicScope"]:
            for target_taxon in target_taxa:
                target_taxonomic_objects.append(
                    AttributeValue(
                        raw=target_taxon,
                        attribute=utils.iri_patterns.attribute_iri(base_iri, "targetTaxonomicScope", target_taxon),
                        value=utils.iri_patterns.attribute_value_iri(base_iri, "targetTaxonomicScope", target_taxon),
                        collection=utils.iri_patterns.attribute_collection_iri(
                            base_iri, "Survey", "targetTaxonomicScope", target_taxon
                        ),
                    )
                )

        # Create survey orgs iris
        survey_org_objects: list[SurveyIDDatatype] = []
        if survey_orgs := row["surveyOrgs"]:
            for raw_org in survey_orgs:
                survey_org_objects.append(
                    SurveyIDDatatype(
                        name=raw_org,
                        datatype=utils.iri_patterns.datatype_iri("surveyID", raw_org),
                        attribution=utils.iri_patterns.attribution_iri(base_iri, "principalInvestigator", raw_org),
                        agent=utils.iri_patterns.agent_iri("org", raw_org),
                    )
                )

        # Add BDR project
        self.add_project(
            uri=project_iri,
            survey=survey,
            dataset=dataset,
            submission_iri=submission_iri,
            graph=graph,
            row=row,
        )

        # Add BDR survey
        self.add_survey(
            uri=survey,
            survey_plan=survey_plan,
            survey_org_objects=survey_org_objects,
            submission_iri=submission_iri,
            row=row,
            graph=graph,
        )

        # Attach temporal coverage if present
        self.add_temporal_coverage(
            uri=survey,
            row=row,
            graph=graph,
        )

        # Add spatial coverage values
        self.add_spatial_coverage(
            uri=survey,
            row=row,
            graph=graph,
        )

        for so_obj in survey_org_objects:
            # Add survey ID source datatype nodes
            self.add_survey_id_source_datatypes(
                uri=so_obj.datatype,
                attribution=so_obj.attribution,
                graph=graph,
            )

            # Add attribution
            self.add_attribution(
                uri=so_obj.attribution,
                agent=so_obj.agent,
                role=PRINCIPAL_INVESTIGATOR,
                graph=graph,
            )

            # Add agent
            self.add_agent(
                uri=so_obj.agent,
                name=so_obj.name,
                graph=graph,
            )

        # Add plan
        self.add_plan(
            uri=survey_plan,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add survey type attribute node
        self.add_survey_type_attribute(
            uri=survey_type_attribute,
            survey_type_value=survey_type_value,
            row_survey_type=row_survey_type,
            dataset=dataset,
            submission_iri=submission_iri,
            graph=graph,
        )

        # Add survey type value node
        self.add_survey_type_value(
            uri=survey_type_value,
            row_survey_type=row_survey_type,
            dataset=dataset,
            graph=graph,
            base_iri=base_iri,
        )

        # Add survey type collection node
        self.add_survey_type_collection(
            uri=survey_type_collection,
            row_survey_type=row_survey_type,
            survey_type_attribute=survey_type_attribute,
            survey_plan=survey_plan,
            dataset=dataset,
            submission_iri=submission_iri,
            graph=graph,
        )

        # Iterate through target habitat objects
        for th_obj in target_habitat_objects:
            # Add target habitat scope attribute node
            self.add_target_habitat_attribute(
                uri=th_obj.attribute,
                dataset=dataset,
                submission_iri=submission_iri,
                target_habitat_value=th_obj.value,
                raw_value=th_obj.raw,
                graph=graph,
            )

            # Add target habitat scope value node
            self.add_target_habitat_value(
                uri=th_obj.value,
                dataset=dataset,
                raw_value=th_obj.raw,
                graph=graph,
                base_iri=base_iri,
            )

            # Add target habitat scope collection
            self.add_target_habitat_collection(
                uri=th_obj.collection,
                raw_value=th_obj.raw,
                target_habitat_attribute=th_obj.attribute,
                survey_plan=survey_plan,
                dataset=dataset,
                submission_iri=submission_iri,
                graph=graph,
            )

        # Iterate through target taxonomic objects
        for tt_obj in target_taxonomic_objects:
            # Add target taxonomic scope attribute node
            self.add_target_taxonomic_attribute(
                uri=tt_obj.attribute,
                dataset=dataset,
                submission_iri=submission_iri,
                target_taxon_value=tt_obj.value,
                raw_value=tt_obj.raw,
                graph=graph,
            )

            # Add target taxonomic scope value node
            self.add_target_taxonomic_value(
                uri=tt_obj.value,
                dataset=dataset,
                raw_value=tt_obj.raw,
                graph=graph,
                base_iri=base_iri,
            )

            # Add target taxonomic scope collection node
            self.add_target_taxonomic_scope_collection(
                uri=tt_obj.collection,
                raw_value=tt_obj.raw,
                target_taxon_attribute=tt_obj.attribute,
                survey_plan=survey_plan,
                dataset=dataset,
                submission_iri=submission_iri,
                graph=graph,
            )

        # Add extra columns JSON
        self.add_extra_fields_json(
            subject_uri=survey,
            row=row,
            graph=graph,
            extra_schema=extra_schema,
        )

    def add_project(
            self,
            uri: rdflib.URIRef | None,
            survey: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            graph: rdflib.Graph,
            row: frictionless.Row,
    ) -> None:
        """Adds the ABIS project to the graph

        Args:
            uri: URI to use for this node, None if the node should not be created.
            survey: BDR survey uri.
            dataset: Dataset uri.
            submission_iri: The Submission IRI to use for mapping.
            graph: Graph to add to.
            row: Row to be processed in dataset.
        """
        # Check if Project should be created
        if uri is None:
            return

        # Add type and attach to Survey
        graph.add((uri, a, utils.namespaces.ABIS.Project))
        graph.add((uri, rdflib.SDO.hasPart, survey))

        # Legacy: If using the metadata form v1, Also map these properties.
        # When using the v2 metadata form, these properties are added by the form's mapping.
        if submission_iri is None:
            # Extract relevant values from row
            project_id: str = row["surveyID"]
            project_name: str = row["surveyName"]
            # Attach to dataset
            graph.add((uri, rdflib.SDO.isPartOf, dataset))
            # Add project name and identifier
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(project_name)))
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(project_id)))

    def add_survey(
            self,
            uri: rdflib.URIRef,
            survey_plan: rdflib.URIRef,
            survey_org_objects: list[SurveyIDDatatype],
            submission_iri: rdflib.URIRef | None,
            row: frictionless.Row,
            graph: rdflib.Graph,
    ) -> None:
        """Adds the tern:Survey to the graph.

        Args:
            uri (rdflib.URIRef): URI of the survey.
            survey_plan (rdflib.URIRef): URI of survey plan
            survey_org_objects (list[SurveyIDDatatype]): Data objects
                describing the survey organisations
            submission_iri: The Submission IRI to use for mapping.
            row (frictionless.Row): Data row provided in the data csv
            graph (rdflib.Graph): The graph to be modified.
        """
        # Add type and dataset
        graph.add((uri, a, utils.namespaces.TERN.Survey))

        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add survey name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["surveyName"])))

        # Add survey ID
        survey_id: str = row["surveyID"]
        # Add survey id literals per organisation
        for survey_org in survey_org_objects:
            id_literal = rdflib.Literal(lexical_or_value=survey_id, datatype=survey_org.datatype)
            graph.add((uri, rdflib.SDO.identifier, id_literal))

        # Add survey id as type string if no organisation provided
        if len(survey_org_objects) == 0:
            id_literal = rdflib.Literal(survey_id)
            graph.add((uri, rdflib.SDO.identifier, id_literal))

        # Add taxonomic coverage
        if taxonomic_coverage := row["targetTaxonomicScope"]:
            for taxa in taxonomic_coverage:
                graph.add((uri, utils.namespaces.BDR.target, rdflib.Literal(taxa)))

        # Add purpose
        if purpose := row["surveyPurpose"]:
            graph.add((uri, utils.namespaces.BDR.purpose, rdflib.Literal(purpose)))

        # Add plan
        graph.add((uri, rdflib.PROV.hadPlan, survey_plan))

        # Add keywords
        if keywords := row["keywords"]:
            for keyword in keywords:
                graph.add((uri, rdflib.SDO.keywords, rdflib.Literal(keyword)))

    def add_spatial_coverage(
            self,
            uri: rdflib.URIRef,
            row: frictionless.Row,
            graph: rdflib.Graph,
    ) -> None:
        """Adds the spatial coverage fields to the graph.

        Args:
            uri (rdflib.URIRef): Base URI the spatial information will be attached
            row (frictionless.Row): Data row provided in the data csv
            graph (rdflib.Graph): Graph to be modified
        """
        # Extract relevant values
        datum = row["geodeticDatum"]
        sc_geometry = row["spatialCoverageWKT"]

        if not (datum and sc_geometry):
            return

        # Construct geometry
        geometry = models.spatial.Geometry(
            raw=sc_geometry,
            datum=datum,
        )

        # Add spatial coverage
        geometry_node = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))

        self.add_geometry_supplied_as(
            subj=uri,
            pred=utils.namespaces.GEO.hasGeometry,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
        )

    def add_temporal_coverage(
            self,
            uri: rdflib.URIRef,
            row: frictionless.Row,
            graph: rdflib.Graph,
    ) -> None:
        """Adds the temporal coverage fields to the graph.

        Args:
            uri (rdflib.URIRef): Base URI the temporal information will be attached
            row (frictionless.Row): Data row provided in the data csv
            graph (rdflib.Graph): Graph to be modified
        """
        # Determine if any dates are present in the row
        start_date: models.temporal.Timestamp = row["surveyStart"]
        end_date: models.temporal.Timestamp = row["surveyEnd"]
        if not start_date and not end_date:
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

        # Attach to survey node
        graph.add((uri, rdflib.TIME.hasTime, temporal_coverage))

    def add_survey_id_source_datatypes(
            self,
            uri: rdflib.URIRef,
            attribution: rdflib.URIRef,
            graph: rdflib.Graph,
    ) -> None:
        """Adds the source datatype nodes to graph.

        Args:
            uri (rdflib.URIRef): The reference uri.
            attribution (rdflib.URIRef): Attribution uri.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal("surveyID source")))
        # Add attribution
        graph.add((uri, rdflib.PROV.qualifiedAttribution, attribution))

    def add_attribution(
            self,
            uri: rdflib.URIRef,
            agent: rdflib.URIRef,
            role: rdflib.URIRef,
            graph: rdflib.Graph,
    ) -> None:
        """Add the prov:Attribution nodes to the graph."""
        # Add attribution
        graph.add((uri, a, rdflib.PROV.Attribution))
        graph.add((uri, rdflib.PROV.agent, agent))
        graph.add((uri, rdflib.PROV.hadRole, role))

    def add_agent(
            self,
            uri: rdflib.URIRef,
            name: str,
            graph: rdflib.Graph,
    ) -> None:
        """Adds agent to graph.

        Args:
            uri (rdflib.URIRef): Agent reference
            name (str): Original name supplied
            graph (rdflib.Graph): Graph to be modified
        """
        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, utils.rdf.uri_or_string_literal(name)))

    def add_plan(
            self,
            uri: rdflib.URIRef,
            row: frictionless.Row,
            dataset: rdflib.URIRef,
            graph: rdflib.Graph,
    ) -> None:
        """Adds plan to graph.

        Args:
            uri: Plan reference.
            row: Raw data row.
            dataset: URI for the dataset node.
            graph: Graph to be modified.
        """

        if not (
                row["targetTaxonomicScope"]
                or row["targetHabitatScope"]
                or row["surveyType"]
                or row["surveyMethodCitation"]
                or row["surveyMethodDescription"]
                or row["surveyMethodURL"]
        ):
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Plan))

        # add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add citation(s)
        if citations := row["surveyMethodCitation"]:
            for citation in citations:
                graph.add((uri, rdflib.SDO.citation, rdflib.Literal(citation)))

        # Add description
        if description := row["surveyMethodDescription"]:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(description)))

        # Add method url(s)
        if method_urls := row["surveyMethodURL"]:
            for method_url in method_urls:
                graph.add((uri, rdflib.SDO.url, rdflib.Literal(method_url, datatype=rdflib.XSD.anyURI)))

    def add_survey_type_attribute(
            self,
            uri: rdflib.URIRef | None,
            survey_type_value: rdflib.URIRef | None,
            row_survey_type: str | None,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            graph: rdflib.Graph,
    ) -> None:
        """Adds survey type attribute node.

        Args:
            uri: Attribute node for survey type
            survey_type_value: Value node for Survey type
            row_survey_type: Raw value from the template for surveyType
            dataset: Dataset the data belongs.
            submission_iri: The Submission IRI to use for mapping.
            graph: Graph to be modified.
        """
        # Non default field, return if not present
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add attribute
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_SURVEY_TYPE))

        # Add value
        if row_survey_type:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row_survey_type)))
        if survey_type_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, survey_type_value))

    def add_survey_type_value(
            self,
            uri: rdflib.URIRef | None,
            row_survey_type: str | None,
            dataset: rdflib.URIRef,
            graph: rdflib.Graph,
            base_iri: rdflib.Namespace,
    ) -> None:
        """Adds the survey type value node to graph.

        Args:
            uri: Survey type value iri.
            row_survey_type: Raw value from the template for surveyType
            dataset: Dataset raw data belongs.
            graph: Graph to be modified.
            base_iri: Namespace used to construct IRIs
        """
        # Return no value IRI
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if row_survey_type:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(row_survey_type)))

            # Retrieve vocab for field
            vocab = self.fields()["surveyType"].get_flexible_vocab()

            # Add value
            term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(row_survey_type)
            graph.add((uri, rdflib.RDF.value, term))

    def add_survey_type_collection(
            self,
            *,
            uri: rdflib.URIRef | None,
            row_survey_type: str | None,
            survey_type_attribute: rdflib.URIRef | None,
            survey_plan: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            graph: rdflib.Graph,
    ) -> None:
        """Add a survey type Collection to the graph

        Args:
            uri: The uri for the Collection.
            row_survey_type: surveyType value from template.
            survey_type_attribute: The uri for the attribute node.
            survey_plan: The uri for the Survey Plan node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
            submission_iri: The Submission IRI to use for mapping.
            graph: The graph.
        """
        # Check if collection node should be created
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        if row_survey_type:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Survey Collection - Survey Type - {row_survey_type}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        # Add link to attribute
        if survey_type_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, survey_type_attribute))
        # add link to the Survey Plan node
        graph.add((uri, rdflib.SDO.member, survey_plan))

    def add_target_habitat_attribute(
            self,
            uri: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            target_habitat_value: rdflib.URIRef,
            raw_value: str,
            graph: rdflib.Graph,
    ) -> None:
        """Adds the target habitat scope attribute node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            submission_iri: The Submission IRI to use for mapping.
            target_habitat_value (rdflib.URIRef): Corresponding value.
            raw_value (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add attribute concept
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_TARGET_HABITAT_SCOPE))

        # Add value
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(raw_value)))
        graph.add((uri, utils.namespaces.TERN.hasValue, target_habitat_value))

    def add_target_habitat_value(
            self,
            uri: rdflib.URIRef,
            dataset: rdflib.URIRef,
            raw_value: str,
            graph: rdflib.Graph,
            base_iri: rdflib.Namespace,
    ) -> None:
        """Add the target habitat scope value node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            raw_value (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
            base_iri (rdflib.Namespace): Namespace used to construct IRIs
        """
        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(raw_value)))

        # Retrieve vocab for field
        vocab = self.fields()["targetHabitatScope"].get_flexible_vocab()

        # Add value
        term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(raw_value)
        graph.add((uri, rdflib.RDF.value, term))

    def add_target_habitat_collection(
            self,
            *,
            uri: rdflib.URIRef,
            raw_value: str,
            target_habitat_attribute: rdflib.URIRef,
            survey_plan: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            graph: rdflib.Graph,
    ) -> None:
        """Add a target habitat Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_value: targetTaxonomicScope value from template.
            target_habitat_attribute: The uri for the attribute node.
            survey_plan: The uri for the Survey Plan node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
            submission_iri: The Submission IRI to use for mapping.
            graph: The graph.
        """
        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        graph.add(
            (
                uri,
                rdflib.SDO.name,
                rdflib.Literal(f"Survey Collection - Target Habitat Scope - {raw_value}"),
            )
        )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        # Add link to attribute
        graph.add((uri, utils.namespaces.TERN.hasAttribute, target_habitat_attribute))
        # add link to the Survey Plan node
        graph.add((uri, rdflib.SDO.member, survey_plan))

    def add_target_taxonomic_attribute(
            self,
            uri: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            target_taxon_value: rdflib.URIRef,
            raw_value: str,
            graph: rdflib.Graph,
    ) -> None:
        """Add the target taxonomic scope node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            submission_iri: The Submission IRI to use for mapping.
            target_taxon_value (rdflib.URIRef): Corresponding
                value node.
            raw_value (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add attribute concept
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_TARGET_TAXONOMIC_SCOPE))

        # Add values
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(raw_value)))
        graph.add((uri, utils.namespaces.TERN.hasValue, target_taxon_value))

    def add_target_taxonomic_value(
            self,
            uri: rdflib.URIRef,
            dataset: rdflib.URIRef,
            raw_value: str,
            graph: rdflib.Graph,
            base_iri: rdflib.Namespace,
    ) -> None:
        """Adds the target toxonomic scope value node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            raw_value (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
            base_iri (rdflib.Namespace): Namespace used to construct IRIs
        """
        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(raw_value)))

        # Retrieve vocab for field
        vocab = self.fields()["targetTaxonomicScope"].get_flexible_vocab()

        # Add value
        term = vocab(graph=graph, source=dataset, base_iri=base_iri).get(raw_value)
        graph.add((uri, rdflib.RDF.value, term))

    def add_target_taxonomic_scope_collection(
            self,
            *,
            uri: rdflib.URIRef,
            raw_value: str,
            target_taxon_attribute: rdflib.URIRef,
            survey_plan: rdflib.URIRef,
            dataset: rdflib.URIRef,
            submission_iri: rdflib.URIRef | None,
            graph: rdflib.Graph,
    ) -> None:
        """Add a target taxonomic scope Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_value: targetTaxonomicScope value from template.
            target_taxon_attribute: The uri for the attribute node.
            survey_plan: The uri for the Survey Plan node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
            submission_iri: The Submission IRI to use for mapping.
            graph: The graph.
        """
        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        graph.add(
            (
                uri,
                rdflib.SDO.name,
                rdflib.Literal(f"Survey Collection - Target Taxonomic Scope - {raw_value}"),
            )
        )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to submission
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        # Add link to attribute
        graph.add((uri, utils.namespaces.TERN.hasAttribute, target_taxon_attribute))
        # add link to the Survey Plan node
        graph.add((uri, rdflib.SDO.member, survey_plan))


# Register Mapper
base.mapper.register_mapper(SurveyMetadataMapper)
