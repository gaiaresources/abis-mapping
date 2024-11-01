"""Provides ABIS mapper for `survey_metadata.csv` template v2"""

# Standard
import dataclasses

# Third-party
import frictionless
import frictionless.checks
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import types
from abis_mapping import utils

# Typing
from typing import Optional, Iterator, Any


# Constants / shortcuts
a = rdflib.RDF.type
PRINCIPAL_INVESTIGATOR = rdflib.URIRef(
    "http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/"
    "code/CI_RoleCode/principalInvestigator"
)
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
    agent: rdflib.URIRef


@dataclasses.dataclass
class AttributeValue:
    """Contains data items to enable producing attribute, value and collection nodes"""

    raw: str
    attribute: rdflib.URIRef
    value: rdflib.URIRef
    collection: rdflib.URIRef


class SurveyMetadataMapper(base.mapper.ABISMapper):
    """ABIS mapper for `survey_metadata.csv` v2"""

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Systematic Survey Metadata Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Metadata Dataset by Gaia Resources"

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
                    # Enforces non-empty and maximum row count.
                    frictionless.checks.table_dimensions(max_rows=1, min_rows=1),
                    # Extra Custom Checks
                    plugins.tabular.IsTabular(),
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

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies mapping for the `survey_metadata.csv` template.

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.
            **kwargs (Any): Additional keyword arguments.

        Yields:
            rdflib.Graph: ABIS conformant RDF sub-graph from raw data chunk.
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

        # Initialise Graph
        graph = utils.rdf.create_graph()

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

        # Open the Resource to allow row streaming
        with resource.open() as r:
            # Loop through rows
            for row in r.row_stream:
                # Map row
                self.apply_mapping_row(
                    row=row,
                    dataset=dataset_iri,
                    graph=graph,
                    base_iri=base_iri,
                )

            yield graph

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> None:
        """Applies mapping for a row in the `survey_metadata.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            base_iri (Optional[rdflib.Namespace]): Optional base IRI
                to use for mapping.
        """
        # Set the row number to start from the data, excluding header
        row_num = row.row_number - 1

        # Create BDR project IRI
        project = utils.rdf.uri(f"project/SSD-Survey-Project/{row_num}", base_iri)

        # Create TERN survey IRI
        survey = utils.rdf.uri(f"survey/SSD-Survey/{row_num}", base_iri)

        # Create survey method procedure IRI
        survey_method_procedure = utils.rdf.uri(f"survey/procedure/surveyMethod/{row_num}", base_iri)

        # Create survey plan IRI
        survey_plan = utils.rdf.uri(f"survey/SSD-survey/{row_num}/plan")

        # Conditionally create survey type attribute, value and collection IRIs
        row_survey_type: str | None = row["surveyType"]
        if row_survey_type:
            survey_type_attribute = utils.rdf.extend_uri(dataset, "attribute", "surveyType", row_survey_type)
            survey_type_value = utils.rdf.extend_uri(dataset, "value", "surveyType", row_survey_type)
            survey_type_collection = utils.rdf.extend_uri(dataset, "SurveyCollection", "surveyType", row_survey_type)
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
                        attribute=utils.rdf.extend_uri(dataset, "attribute", "targetHabitatScope", target_habitat),
                        value=utils.rdf.extend_uri(dataset, "value", "targetHabitatScope", target_habitat),
                        collection=utils.rdf.extend_uri(
                            dataset, "SurveyCollection", "targetHabitatScope", target_habitat
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
                        attribute=utils.rdf.extend_uri(dataset, "attribute", "targetTaxonomicScope", target_taxon),
                        value=utils.rdf.extend_uri(dataset, "value", "targetTaxonomicScope", target_taxon),
                        collection=utils.rdf.extend_uri(
                            dataset, "SurveyCollection", "targetTaxonomicScope", target_taxon
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
                        datatype=utils.rdf.uri(f"datatype/surveyID/{raw_org}", base_iri),
                        agent=utils.rdf.uri(f"agent/{raw_org}"),
                    )
                )

        # Add BDR project
        self.add_project(
            uri=project,
            survey=survey,
            dataset=dataset,
            graph=graph,
            row=row,
        )

        # Add BDR survey
        self.add_survey(
            uri=survey,
            survey_method=survey_method_procedure,
            survey_plan=survey_plan,
            survey_org_objects=survey_org_objects,
            row=row,
            graph=graph,
        )

        # Attach temporal coverage if present
        self.add_temporal_coverage(
            uri=survey,
            row=row,
            graph=graph,
        )

        # Add survey method urls
        self.add_survey_methodologies(
            uri=survey_method_procedure,
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
                agent=so_obj.agent,
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
            survey_type_attribute=survey_type_attribute,
            target_habitat_scope_attributes=(hbt.attribute for hbt in target_habitat_objects),
            target_taxa_attributes=(tx.attribute for tx in target_taxonomic_objects),
            row=row,
            graph=graph,
        )

        # Add survey type attribute node
        self.add_survey_type_attribute(
            uri=survey_type_attribute,
            survey_type_value=survey_type_value,
            row_survey_type=row_survey_type,
            dataset=dataset,
            graph=graph,
        )

        # Add survey type value node
        self.add_survey_type_value(
            uri=survey_type_value,
            row_survey_type=row_survey_type,
            dataset=dataset,
            graph=graph,
        )

        # Add survey type collection node
        self.add_survey_type_collection(
            uri=survey_type_collection,
            row_survey_type=row_survey_type,
            survey_type_attribute=survey_type_attribute,
            survey=survey,
            dataset=dataset,
            graph=graph,
        )

        # Iterate through target habitat objects
        for th_obj in target_habitat_objects:
            # Add target habitat scope attribute node
            self.add_target_habitat_attribute(
                uri=th_obj.attribute,
                dataset=dataset,
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
            )

            # Add target habitat scope collection
            self.add_target_habitat_collection(
                uri=th_obj.collection,
                raw_value=th_obj.raw,
                target_habitat_attribute=th_obj.attribute,
                survey=survey,
                dataset=dataset,
                graph=graph,
            )

        # Iterate through target taxonomic objects
        for tt_obj in target_taxonomic_objects:
            # Add target taxonomic scope attribute node
            self.add_target_taxonomic_attribute(
                uri=tt_obj.attribute,
                dataset=dataset,
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
            )

            # Add target taxonomic scope collection node
            self.add_target_taxonomic_scope_collection(
                uri=tt_obj.collection,
                raw_value=tt_obj.raw,
                target_taxon_attribute=tt_obj.attribute,
                survey=survey,
                dataset=dataset,
                graph=graph,
            )

        # Add extra columns JSON
        self.add_extra_fields_json(
            subject_uri=survey,
            row=row,
            graph=graph,
        )

    def add_project(
        self,
        uri: rdflib.URIRef,
        survey: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        row: frictionless.Row,
    ) -> None:
        """Adds the BDR project to the graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            survey (rdflib.URIRef): BDR survey uri.
            dataset (rdflib.URIRef): Dataset uri.
            graph (rdflib.Graph): Graph to add to.
            row (frictionless.Row): Row to be processed in dataset.
        """
        # Extract relevant values from row
        project_id = row["surveyID"]
        project_name = row["surveyName"]

        # Add type and attach to dataset
        graph.add((uri, a, utils.namespaces.BDR.Project))
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add (required) project name, id (not required) and purpose (not required).
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(project_name)))
        if project_id:
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(project_id)))

        # Attach survey
        graph.add((uri, rdflib.SDO.hasPart, survey))

    def add_survey(
        self,
        uri: rdflib.URIRef,
        survey_method: rdflib.URIRef,
        survey_plan: rdflib.URIRef,
        survey_org_objects: list[SurveyIDDatatype],
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the tern:Survey to the graph.

        Args:
            uri (rdflib.URIRef): URI of the survey.
            survey_method (rdflib.URIRef): URI of node associated with
                survey method data.
            survey_plan (rdflib.URIRef): URI of survey plan
            survey_org_objects (list[SurveyIDDatatype]): Data objects
                describing the survey organisations
            row (frictionless.Row): Data row provided in the data csv
            graph (rdflib.Graph): The graph to be modified.
        """
        # Add type and dataset
        graph.add((uri, a, utils.namespaces.TERN.Survey))

        # Add survey method procedure node
        graph.add((uri, rdflib.PROV.hadPlan, survey_method))

        # Add survey name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["surveyName"])))

        # Add survey ID
        if (survey_id := row["surveyID"]) is not None:
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
        geometry = types.spatial.Geometry(
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
        start_date: types.temporal.Timestamp = row["surveyStart"]
        end_date: types.temporal.Timestamp = row["surveyEnd"]
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

    def add_survey_methodologies(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the survey methodology URIs to the graph.

        Args:
            uri (rdflib.URIRef): Base URI the methodologies will be attached.
            row (frictionless.Row): Row containing CSV data row contents.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract relevant values from row
        survey_method_urls = row["surveyMethodURL"]
        survey_method_description = row["surveyMethodDescription"]
        survey_method_refs = row["surveyMethodCitation"]

        # If no relevant data provided then no change to graph
        if not (survey_method_urls or survey_method_description or survey_method_refs):
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Plan))

        # Attach survey methodologies
        if survey_method_urls:
            for survey_method_url in survey_method_urls:
                # Add literal containing the method URL
                graph.add(
                    (
                        uri,
                        rdflib.SDO.url,
                        rdflib.Literal(survey_method_url, datatype=rdflib.XSD.anyURI),
                    )
                )

        if survey_method_description:
            # Add literal containing the description
            graph.add(
                (
                    uri,
                    rdflib.SDO.description,
                    rdflib.Literal(survey_method_description),
                )
            )

        if survey_method_refs:
            for survey_method_ref in survey_method_refs:
                # Add bibliographic reference
                graph.add(
                    (
                        uri,
                        rdflib.SDO.citation,
                        rdflib.Literal(survey_method_ref),
                    )
                )

    def add_survey_id_source_datatypes(
        self,
        uri: rdflib.URIRef,
        agent: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the source datatype nodes to graph.

        Args:
            uri (rdflib.URIRef): The reference uri.
            agent (rdflib.URIRef): Agent uri.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add label
        graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal("surveyID source")))

        # Add attribution
        attribution = rdflib.BNode()
        graph.add((attribution, a, rdflib.PROV.Attribution))
        graph.add((attribution, rdflib.PROV.agent, agent))
        graph.add((attribution, rdflib.PROV.hadRole, PRINCIPAL_INVESTIGATOR))
        graph.add((uri, rdflib.PROV.qualifiedAttribution, attribution))

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
        survey_type_attribute: rdflib.URIRef | None,
        target_habitat_scope_attributes: Iterator[rdflib.URIRef],
        target_taxa_attributes: Iterator[rdflib.URIRef],
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds plan to graph.

        Args:
            uri: Plan reference.
            survey_type_attribute: SurveyType attribute for the node
            target_habitat_scope_attribute: targetHabitatScope attribute for the node.
            target_taxa_attribute: target taxa attribute for the node.
            row: Raw data row.
            graph: Graph to be modified.
        """
        # Add type
        graph.add((uri, a, rdflib.PROV.Plan))

        # Add attributes
        if survey_type_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, survey_type_attribute))

        for hbt_attr in target_habitat_scope_attributes:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, hbt_attr))

        for tx_attr in target_taxa_attributes:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, tx_attr))

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
        graph: rdflib.Graph,
    ) -> None:
        """Adds survey type attribute node.

        Args:
            uri: Attribute node for survey type
            survey_type_value: Value node for Survey type
            row_survey_type: Raw value from the template for surveyType
            dataset: Dataset the data belongs.
            graph: Graph to be modified.
        """
        # Non default field, return if not present
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

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
    ) -> None:
        """Adds the survey type value node to graph.

        Args:
            uri: Survey type value iri.
            row_survey_type: Raw value from the template for surveyType
            dataset: Dataset raw data belongs.
            graph: Graph to be modified.
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
            vocab = self.fields()["surveyType"].get_vocab()

            # Add value
            term = vocab(graph=graph, source=dataset).get(row_survey_type)
            graph.add((uri, rdflib.RDF.value, term))

    def add_survey_type_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        row_survey_type: str | None,
        survey_type_attribute: rdflib.URIRef | None,
        survey: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add a survey type Collection to the graph

        Args:
            uri: The uri for the Collection.
            row_survey_type: surveyType value from template.
            survey_type_attribute: The uri for the attribute node.
            survey: The uri for the Survey node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
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
                    rdflib.SDO.identifier,
                    rdflib.Literal(f"Survey Collection - Survey Type - {row_survey_type}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # Add link to attribute
        if survey_type_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, survey_type_attribute))
        # add link to the Survey node
        graph.add((uri, rdflib.SDO.member, survey))

    def add_target_habitat_attribute(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        target_habitat_value: rdflib.URIRef,
        raw_value: str,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the target habitat scope attribute node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            target_habitat_value (rdflib.URIRef): Corresponding value.
            raw_value (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

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
    ) -> None:
        """Add the target habitat scope value node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            raw_value (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(raw_value)))

        # Retrieve vocab for field
        vocab = self.fields()["targetHabitatScope"].get_vocab()

        # Add value
        term = vocab(graph=graph, source=dataset).get(raw_value)
        graph.add((uri, rdflib.RDF.value, term))

    def add_target_habitat_collection(
        self,
        *,
        uri: rdflib.URIRef,
        raw_value: str,
        target_habitat_attribute: rdflib.URIRef,
        survey: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add a target habitat Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_value: targetTaxonomicScope value from template.
            target_habitat_attribute: The uri for the attribute node.
            survey: The uri for the Survey node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
            graph: The graph.
        """
        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        graph.add(
            (
                uri,
                rdflib.SDO.identifier,
                rdflib.Literal(f"Survey Collection - Target Habitat Scope - {raw_value}"),
            )
        )
        # Add link to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # Add link to attribute
        graph.add((uri, utils.namespaces.TERN.hasAttribute, target_habitat_attribute))
        # add link to the Survey node
        graph.add((uri, rdflib.SDO.member, survey))

    def add_target_taxonomic_attribute(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        target_taxon_value: rdflib.URIRef,
        raw_value: str,
        graph: rdflib.Graph,
    ) -> None:
        """Add the target taxonomic scope node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            target_taxon_value (rdflib.URIRef): Corresponding
                value node.
            raw_value (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

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
    ) -> None:
        """Adds the target toxonomic scope value node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            raw_value (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add types
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(raw_value)))

        # Retrieve vocab for field
        vocab = self.fields()["targetTaxonomicScope"].get_vocab()

        # Add value
        term = vocab(graph=graph, source=dataset).get(raw_value)
        graph.add((uri, rdflib.RDF.value, term))

    def add_target_taxonomic_scope_collection(
        self,
        *,
        uri: rdflib.URIRef,
        raw_value: str,
        target_taxon_attribute: rdflib.URIRef,
        survey: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Add a target taxonomic scope Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_value: targetTaxonomicScope value from template.
            target_taxon_attribute: The uri for the attribute node.
            survey: The uri for the Survey node that wil be a member of the Collection.
            dataset: The uri for the dateset node.
            graph: The graph.
        """
        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        # Add identifier
        graph.add(
            (
                uri,
                rdflib.SDO.identifier,
                rdflib.Literal(f"Survey Collection - Target Taxonomic Scope - {raw_value}"),
            )
        )
        # Add link to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        # Add link to attribute
        graph.add((uri, utils.namespaces.TERN.hasAttribute, target_taxon_attribute))
        # add link to the Survey node
        graph.add((uri, rdflib.SDO.member, survey))


# Register Mapper
base.mapper.ABISMapper.register_mapper(SurveyMetadataMapper)
