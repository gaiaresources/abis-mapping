"""Provides ABIS Mapper for `survey_site_data-v2.0.0.csv` template."""

# Standard
import dataclasses
import decimal
import urllib.parse

# Third-party
import rdflib
import frictionless
import shapely
import shapely.geometry

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import settings
from abis_mapping import types
from abis_mapping import utils
from abis_mapping import vocabs

# Typing
from typing import Any, Optional, Iterator


# Constants and shortcuts
a = rdflib.RDF.type
HABITAT_DESCRIPTION = rdflib.URIRef("https://linked.data.gov.au/def/nrm/aa4c96f6-9ea8-4bd3-8800-0bfddcd8a37c")
CONCEPT_DATA_GENERALIZATIONS = utils.rdf.uri("concept/data-generalizations", utils.namespaces.EXAMPLE)
CONCEPT_VEGETATION_CONDITION = rdflib.URIRef(
    "http://linked.data.gov.au/def/ausplots-cv/ff69c254-e549-45e8-a320-e28ead5092c8"
)  # noqa: E501
DEFAULT_SURVEY = utils.rdf.uri("survey/SSD-Survey/1", utils.namespaces.CREATEME)  # TODO: Cross reference
UNSPECIFIED_CONDITION_METHOD = utils.rdf.uri("bdr-cv/methods/conditionMethod/Unspecified", utils.namespaces.CREATEME)


# Dataclasses used in mapping
@dataclasses.dataclass
class AttributeValue:
    """Contains data items to enable producing attribute and value nodes"""

    raw: str
    attribute: rdflib.URIRef
    value: rdflib.URIRef


@dataclasses.dataclass
class Agent:
    """Contains data items to enable producing agent nodes"""

    raw: str
    uri: rdflib.URIRef


class SurveySiteMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `survey_site_data.csv` v2"""

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Systematic Survey Site Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Site Dataset by Gaia Resources"

    def apply_validation(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `survey_site_data.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.
            **kwargs (Any): Additional keyword arguments.

        Keyword Args:
            site_id_map (dict[str, bool]): Site ids present in the occurrence template.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Extract keyword arguments
        site_id_map: dict[str, bool] = kwargs.get("site_id_map", {})

        # Construct schema
        schema = self.extra_fields_schema(
            data=data,
            full_schema=True,
        )

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
                    plugins.sites_geometry.SitesGeometry(
                        occurrence_site_ids=set(site_id_map),
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["relatedSiteID", "relationshipToRelatedSite"],
                    ),
                ],
            )
        )

        # Return validation report
        return report

    def extract_geometry_defaults(
        self,
        data: base.types.ReadableType,
    ) -> dict[str, str]:
        """Constructs a dictionary mapping site id to default WKT.

        The resulting string WKT returned can then be used as the missing
        geometry for other related templates i.e. the site occurrences

        Args:
            data (base.types.ReadableType): Raw data to be mapped.

        Returns:
            dict[str, str]: Keys are the site id; values are the
                appropriate point WKT serialized string. If none then
                there is no siteID key created. Values include the geodetic
                datum uri.
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

        # Context manager for row streaming
        with resource.open() as r:
            # Create empty dictionary to hold mapping values
            result = {}
            for row in r.row_stream:
                # Extract values
                site_id: str = row["siteID"]
                footprint_wkt: shapely.geometry.base.BaseGeometry = row["footprintWKT"]
                longitude: decimal.Decimal = row["decimalLongitude"]
                latitude: decimal.Decimal = row["decimalLatitude"]
                datum: str = row["geodeticDatum"]

                # if no valid datum for row then don't add to map.
                if datum is None:
                    continue

                try:
                    # Default to using the footprint wkt + geodetic datum
                    if footprint_wkt is not None:
                        # Create string and add to map for site id
                        result[site_id] = str(
                            types.spatial.Geometry(
                                raw=footprint_wkt.centroid,
                                datum=datum,
                            ).to_rdf_literal()
                        )
                        continue

                    # If not footprint then we revert to using supplied longitude & latitude
                    if longitude is not None and latitude is not None:
                        # Create string and add to map for site id
                        result[site_id] = str(
                            types.spatial.Geometry(
                                raw=shapely.Point([longitude, latitude]),
                                datum=datum,
                            ).to_rdf_literal()
                        )
                except types.spatial.GeometryError:
                    continue

            return result

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping for the `survey_site_data.csv` Template.

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.

        Keyword Args:
            chunk_size (Optional[int]): How many rows of the original data to
                ingest before yielding a graph. `None` will ingest all rows.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
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
        base_iri: Optional[rdflib.Namespace],
    ) -> None:
        """Applies mapping for a row in the `survey_site_data.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            base_iri (Optional[rdflib.Namespace]): Optional base IRI
                to use for mapping.
        """
        # Set the row number to start from the data, excluding header
        row_num = row.row_number - 1

        site_visit = utils.rdf.uri(f"visit/site/{row_num}", base_iri)
        site_id = urllib.parse.quote(row["siteID"], safe="")
        site = dataset + f"/Site/{site_id}"
        condition_site_observation = utils.rdf.uri(f"observation/site/condition/{row_num}", base_iri)
        condition_value = utils.rdf.uri(f"value/condition/{row_num}")

        # Conditionally create uris dependent on siteIDSource
        if site_id_src := row["siteIDSource"]:
            site_id_datatype = utils.rdf.uri(f"datatype/siteID/{site_id_src}", base_iri)
            site_id_agent = utils.rdf.uri(f"agent/{site_id_src}", base_iri)
        else:
            site_id_datatype = None
            site_id_agent = None

        # Conditionally create uris dependent on dataGeneralizations
        if row["dataGeneralizations"]:
            data_generalizations_attribute = utils.rdf.uri(f"attribute/dataGeneralizations/site/{row_num}", base_iri)
            data_generalizations_value = utils.rdf.uri(f"value/dataGeneralizations/site/{row_num}", base_iri)
        else:
            data_generalizations_attribute = None
            data_generalizations_value = None

        # Create habitat attribute and value objects
        habitat_objects: list[AttributeValue] = []
        if habitats := row["habitat"]:
            for i, habitat in enumerate(habitats, start=1):
                habitat_objects.append(
                    AttributeValue(
                        raw=habitat,
                        attribute=utils.rdf.uri(f"attribute/habitat/site/{row_num}/{i}", base_iri),
                        value=utils.rdf.uri(f"value/habitat/site/{row_num}/{i}", base_iri),
                    )
                )

        # Create organization agent objects
        org_agent_objects: list[Agent] = []
        if organization_agents := row["visitOrgs"]:
            for organizations_agent in organization_agents:
                org_agent_objects.append(
                    Agent(
                        raw=organizations_agent,
                        uri=utils.rdf.uri(f"agent/{organizations_agent}", base_iri),
                    )
                )

        # Create observer agent objects
        observer_agent_objects: list[Agent] = []
        if observer_agents := row["visitObservers"]:
            for observer_agent in observer_agents:
                observer_agent_objects.append(
                    Agent(
                        raw=observer_agent,
                        uri=utils.rdf.uri(f"agent/{observer_agent}", base_iri),
                    )
                )

        # Add site
        self.add_site(
            uri=site,
            dataset=dataset,
            site_visit=site_visit,
            site_id_datatype=site_id_datatype,
            habitat_attributes=[h.attribute for h in habitat_objects],
            data_generalizations_attribute=data_generalizations_attribute,
            row=row,
            graph=graph,
        )

        # Add site id datatype
        self.add_site_id_datatype(
            uri=site_id_datatype,
            agent=site_id_agent,
            graph=graph,
        )

        # Add site id agent
        self.add_site_id_agent(
            uri=site_id_agent,
            row=row,
            graph=graph,
        )

        # Iterate through habitat objects
        for habitat_object in habitat_objects:
            # Add habitat attribute
            self.add_habitat_attribute(
                uri=habitat_object.attribute,
                value=habitat_object.value,
                dataset=dataset,
                raw=habitat_object.raw,
                graph=graph,
            )

            # Add habitat value
            self.add_habitat_value(
                uri=habitat_object.value,
                dataset=dataset,
                raw=habitat_object.raw,
                graph=graph,
            )

        # Add data generalizations attribute
        self.add_data_generalizations_attribute(
            uri=data_generalizations_attribute,
            value=data_generalizations_value,
            dataset=dataset,
            row=row,
            graph=graph,
        )

        # Add data generalizations value
        self.add_data_generalizations_value(
            uri=data_generalizations_value,
            row=row,
            graph=graph,
        )

        # Add site visit
        self.add_site_visit(
            uri=site_visit,
            dataset=dataset,
            agents=[agent.uri for agent in org_agent_objects + observer_agent_objects],
            row=row,
            graph=graph,
        )

        # Add organization agents
        for org_agent in org_agent_objects:
            self.add_organization_agent(
                uri=org_agent.uri,
                raw=org_agent.raw,
                graph=graph,
            )

        # Add observer agents
        for obs_agent in observer_agent_objects:
            self.add_observer_agent(
                uri=obs_agent.uri,
                raw=obs_agent.raw,
                graph=graph,
            )

        # Add site condition
        self.add_site_condition(
            uri=condition_site_observation,
            dataset=dataset,
            site=site,
            value=condition_value,
            row=row,
            graph=graph,
        )

        # TODO: Add condition value
        self.add_condition_value(
            uri=condition_value,
            row=row,
            graph=graph,
        )

        # Add geometry
        self.add_footprint_geometry(
            uri=site,
            row=row,
            graph=graph,
        )

        self.add_point_geometry(
            uri=site,
            row=row,
            graph=graph,
        )

        # Add extra fields
        self.add_extra_fields_json(
            subject_uri=site,
            row=row,
            graph=graph,
        )

    def add_site(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        site_visit: rdflib.URIRef,
        site_id_datatype: rdflib.URIRef | None,
        habitat_attributes: list[rdflib.URIRef],
        data_generalizations_attribute: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site to the graph.

        Args:
           uri (rdflib.URIRef): URI to use for this node.
           dataset (rdflib.URIRef): Dataset to which data belongs.
           site_visit (rdflib.URIRef): Site visit the site corresponds to.
           site_id_datatype (rdflib.URIRef | None): Datatype to use for
                the site id literal.
           habitat_attributes (list[rdflib.URIRef]): List of habitat attribute
                iris.
           data_generalizations_attribute (rdflib.URIRef | None): Data generalization
                the site corresponds.
           row (frictionless.Row): Row to retrieve data from.
           graph (rdflib.Graph): Graph to be modified.
        """
        # Extract relevant values
        site_id = row["siteID"]
        site_name = row["siteName"]
        site_type = row["siteType"]
        site_description = row["siteDescription"]
        coordinate_uncertainty = row["coordinateUncertaintyInMeters"]

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Site))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add habitat attributes
        for habitat_attribute in habitat_attributes:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, habitat_attribute))

        # Link to site visit
        graph.add((uri, utils.namespaces.TERN.hasSiteVisit, site_visit))

        # Add siteID
        dt = site_id_datatype if site_id_datatype is not None else rdflib.XSD.string
        graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(site_id, datatype=dt)))

        # Add related site if available
        if (relationship_to_related_site := row["relationshipToRelatedSite"]) and (
            related_site := row["relatedSiteID"]
        ):
            # Retrieve vocab for field
            relationship_to_related_site_vocab = self.fields()["relationshipToRelatedSite"].get_vocab()

            # Retrieve term
            relationship_to_related_site_term = relationship_to_related_site_vocab(graph=graph).get(
                relationship_to_related_site
            )

            # Assign triple based on related site string
            if (related_site_literal := utils.rdf.uri_or_string_literal(related_site)).datatype == rdflib.XSD.string:
                graph.add((uri, relationship_to_related_site_term, related_site_literal))
            else:
                graph.add((uri, relationship_to_related_site_term, rdflib.URIRef(related_site)))

        # Add site tern featuretype
        graph.add((uri, utils.namespaces.TERN.featureType, vocabs.site_type.SITE.iri))

        # Retrieve vocab for field
        site_type_vocab = self.fields()["siteType"].get_vocab()

        # Retrieve term or create on the fly
        site_type_term = site_type_vocab(graph=graph, source=dataset).get(site_type)

        # Add to site type graph
        graph.add((uri, rdflib.DCTERMS.type, site_type_term))

        # Add site name if available
        if site_name:
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(site_name)))

        # Add site description if available
        if site_description:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(site_description)))

        # Add coordinate uncertainty if available
        if coordinate_uncertainty:
            accuracy = rdflib.Literal(coordinate_uncertainty, datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Add data generalizations attribute if available
        if data_generalizations_attribute is not None:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, data_generalizations_attribute))

    def add_site_id_datatype(
        self,
        uri: rdflib.URIRef | None,
        agent: rdflib.URIRef | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site id datatype to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            agent (rdflib.URIRef | None): Agent that the datatype
                corresponds.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal("siteID source")))

        # Add attribution
        if agent is not None:
            graph.add((uri, rdflib.PROV.wasAttributedTo, agent))

    def add_site_id_agent(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the site id agent to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["siteIDSource"])))

    def add_habitat_attribute(
        self,
        uri: rdflib.URIRef,
        value: rdflib.URIRef,
        dataset: rdflib.URIRef,
        raw: str,
        graph: rdflib.Graph,
    ) -> None:
        """Adds a habitat attribute to the graph.

        Args:
            uri (rdflib.URIRef): Subjcet of the node.
            value (rdflib.URIRef): Corresponding value reference.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            raw (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add tern values
        graph.add((uri, utils.namespaces.TERN.attribute, HABITAT_DESCRIPTION))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(raw)))
        graph.add((uri, utils.namespaces.TERN.hasValue, value))

    def add_habitat_value(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        raw: str,
        graph: rdflib.Graph,
    ) -> None:
        """Add a habitat value node to graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset data belongs.
            raw (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("Site habitat")))

        # Retrieve vocab for field
        vocab = self.fields()["habitat"].get_vocab()

        # Add flexible vocab term
        term = vocab(graph=graph, source=dataset).get(raw)
        graph.add((uri, rdflib.RDF.value, term))

    def add_data_generalizations_attribute(
        self,
        uri: rdflib.URIRef | None,
        value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Add the data generalizations attribute node to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            value (rdflib.URIRef | None): Corresponding value.
            dataset (rdflib.URIRef): Corresponding dataset data belongs.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Attribute))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add tern values
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_DATA_GENERALIZATIONS))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, row["dataGeneralizations"]))
        if value is not None:
            graph.add((uri, utils.namespaces.TERN.hasValue, value))

    def add_data_generalizations_value(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Add data generalizations value node to graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.:
        """
        # Check subject provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add raw value
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["dataGeneralizations"])))

    def add_site_visit(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        agents: list[rdflib.URIRef],
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site visit to the graph.

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset to which data belongs.
            agents (list[rdflib.URIRef]): Agents involved in the site visit.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.SiteVisit))

        # Add to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # TODO: Cross reference
        # Add survey
        graph.add((uri, rdflib.SDO.isPartOf, DEFAULT_SURVEY))

        # Add site visit id
        if site_visit_id := row["siteVisitID"]:
            graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(site_visit_id)))

        # Add temporal information
        site_visit_start: types.temporal.Timestamp = row["siteVisitStart"]
        start_instant = rdflib.BNode()
        graph.add((start_instant, a, rdflib.TIME.Instant))
        graph.add((start_instant, site_visit_start.rdf_in_xsd, site_visit_start.to_rdf_literal()))

        temporal_entity = rdflib.BNode()
        graph.add((temporal_entity, a, rdflib.TIME.TemporalEntity))
        graph.add((temporal_entity, rdflib.TIME.hasBeginning, start_instant))

        site_visit_end: types.temporal.Timestamp | None = row["siteVisitEnd"]
        if site_visit_end is not None:
            end_instant = rdflib.BNode()
            graph.add((end_instant, a, rdflib.TIME.Instant))
            graph.add((end_instant, site_visit_end.rdf_in_xsd, site_visit_end.to_rdf_literal()))
            graph.add((temporal_entity, rdflib.TIME.hasEnd, end_instant))

        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))

        # Add agents
        for agent in agents:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, agent))

    def add_organization_agent(
        self,
        uri: rdflib.URIRef,
        raw: str,
        graph: rdflib.Graph,
    ) -> None:
        """Adds organization agent node to the graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            raw (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, a, rdflib.PROV.Organization))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(raw)))

    def add_observer_agent(
        self,
        uri: rdflib.URIRef,
        raw: str,
        graph: rdflib.Graph,
    ) -> None:
        """Adds observer agent node to the graph

        Args:
            uri (rdflib.URIRef): Subject of the node.
            raw (str): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, a, rdflib.PROV.Person))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(raw)))

    def add_site_condition(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        site: rdflib.URIRef,
        value: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site condition node to the graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset raw data belongs.
            site (rdflib.URIRef): Site that condition references.
            value (rdflib.URIRef): Corresponding value node reference.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check to see if a condition was supplied
        if not (condition := row["condition"]):
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Observation))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add comment
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("site-condition")))

        # Add feature of interest
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, site))

        # Add result
        graph.add((uri, rdflib.SOSA.hasResult, value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(condition)))

        # Add observed property
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_VEGETATION_CONDITION))

        # Add temporal information
        site_visit_start: types.temporal.Timestamp = row["siteVisitStart"]
        start_instant = rdflib.BNode()
        graph.add((start_instant, a, rdflib.TIME.Instant))
        graph.add((start_instant, site_visit_start.rdf_in_xsd, site_visit_start.to_rdf_literal()))
        graph.add((uri, rdflib.SOSA.phenomenonTime, start_instant))

        graph.add((uri, utils.namespaces.TERN.resultDateTime, site_visit_start.to_rdf_literal()))

        # Add method
        graph.add((uri, rdflib.SOSA.usedProcedure, UNSPECIFIED_CONDITION_METHOD))

    def add_condition_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds condition value node to graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check to ensure value for condition provided.
        if not (condition := row["condition"]):
            return

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add value
        graph.add((uri, rdflib.RDF.value, condition))

    def add_footprint_geometry(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds footprint geometry details to the graph.

        Args:
            uri (rdflib.URIRef): URI to attach.
            row (frictionless.Row): Row to retrieve data from.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract values
        geodetic_datum = row["geodeticDatum"]
        footprint_wkt = row["footprintWKT"]

        if footprint_wkt is None or geodetic_datum is None:
            return

        # Construct geometry
        geometry = types.spatial.Geometry(
            raw=footprint_wkt,
            datum=geodetic_datum,
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))

        # Add original geometry supplied as statement
        self.add_geometry_supplied_as(
            subj=uri,
            pred=utils.namespaces.GEO.hasGeometry,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
        )

    def add_point_geometry(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site point geometry details to the graph.

        Args:
            uri (rdflib.URIRef): URI to attach.
            row (frictionless.Row): Row to retrieve data from.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract values
        decimal_latitude = row["decimalLatitude"]
        decimal_longitude = row["decimalLongitude"]
        geodetic_datum = row["geodeticDatum"]

        if decimal_latitude is None or decimal_longitude is None or geodetic_datum is None:
            return

        # Construct geometry
        geometry = types.spatial.Geometry(
            raw=types.spatial.LatLong(decimal_latitude, decimal_longitude),
            datum=geodetic_datum,
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))

        # Add original geometry supplied as statement
        self.add_geometry_supplied_as(
            subj=uri,
            pred=utils.namespaces.GEO.hasGeometry,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
        )


# Register Mapper
if settings.SETTINGS.MAJOR_VERSION >= 5:
    # SSD v2 is still in development, keep hidden until v5 release candidates are created
    base.mapper.ABISMapper.register_mapper(SurveySiteMapper)
