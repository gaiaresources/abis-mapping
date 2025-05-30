"""Provides ABIS Mapper for `survey_site_data-v3.0.0.csv` template."""

# Standard
import dataclasses
import datetime
import decimal

# Third-party
import rdflib
import frictionless
import frictionless.checks
import shapely
import shapely.geometry

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import models
from abis_mapping import utils
from abis_mapping import vocabs

# Typing
from typing import Any, Literal


# Constants and shortcuts
a = rdflib.RDF.type
HABITAT = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99")
CONCEPT_DATA_GENERALIZATIONS = rdflib.URIRef(
    "http://linked.data.gov.au/def/tern-cv/77f30c7d-4642-45a4-ab91-1400bf2bc652"
)
DATA_ROLE_RESOURCE_PROVIDER = rdflib.URIRef("https://linked.data.gov.au/def/data-roles/resourceProvider")


# Dataclasses used in mapping
@dataclasses.dataclass
class AttributeValue:
    """Contains data items to enable producing attribute, value and collection nodes"""

    raw: str
    attribute: rdflib.URIRef
    value: rdflib.URIRef
    collection: rdflib.URIRef


@dataclasses.dataclass
class Agent:
    """Contains data items to enable producing agent nodes"""

    raw: str
    uri: rdflib.URIRef


class SurveySiteMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `survey_site_data.csv` v3"""

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
            site_id_map (dict[models.identifier.SiteIdentifier, bool]): Site ids present in the occurrence template.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Extract keyword arguments
        site_id_map: dict[models.identifier.SiteIdentifier, bool] = kwargs.get("site_id_map", {})
        if site_id_map is None:
            raise ValueError("If provided, site_id_map must not be None")

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

        # Extract SiteIdentifiers present in this template.
        site_identifiers = self.extract_site_identifiers(data)

        # Validate
        report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra custom checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    # Valid of the ID-related fields
                    plugins.site_id_or_iri_validation.SiteIdentifierCheck(),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["siteID", "siteIDSource"],
                    ),
                    plugins.unique_together.UniqueTogether(
                        fields=["siteID", "siteIDSource"],
                        slugified_fields=["siteIDSource"],
                        null_handling="skip",
                        error_message_template=(
                            "siteID and siteIDSource must be unique for each Row. "
                            '[{values}] have already been used in the row at position "{first_seen_row_number}"'
                        ),
                    ),
                    # Other fields' validation
                    plugins.sites_geometry.SitesGeometry(
                        occurrence_site_identifiers=site_id_map,
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["relatedSiteID", "relatedSiteIDSource"],
                    ),
                    # Check that related site and relationship are provided together,
                    # also check that relatedSiteID+Source matches a site in the template.
                    plugins.related_site_validation.RelatedSiteValidation(
                        site_identifiers=site_identifiers,
                    ),
                ],
            )
        )

        # Return validation report
        return report

    def extract_site_identifiers(
        self,
        data: base.types.ReadableType,
    ) -> dict[models.identifier.SiteIdentifier, Literal[True]]:
        """Constructs a key mapped 'set' of all SiteIdentifier in the template.

        Args:
            data: Raw data to be mapped
        """
        # Construct schema
        schema = self.regular_fields_schema()

        # Construct resource
        resource = frictionless.Resource(source=data, format="csv", schema=schema, encoding="utf-8")

        with resource.open() as r:
            # Create empty dictionary to hold mapping values
            result: dict[models.identifier.SiteIdentifier, Literal[True]] = {}
            for row in r.row_stream:
                # Extract value
                site_identifier = models.identifier.SiteIdentifier.from_row(row)

                if site_identifier:
                    result[site_identifier] = True

            return result

    def extract_geometry_defaults(
        self,
        data: base.types.ReadableType,
    ) -> dict[models.identifier.SiteIdentifier, str]:
        """Constructs a dictionary mapping site id to default WKT.

        The resulting string WKT returned can then be used as the missing
        geometry for other related templates i.e. the site occurrences

        Args:
            data (base.types.ReadableType): Raw data to be mapped.

        Returns:
            Mapping with SiteIdentifier as the keys; values are the
            appropriate point WKT serialized string. If none then
            there is no siteID key created. Values include the geodetic
            datum uri.
        """
        # Construct schema
        schema = self.regular_fields_schema()

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
            result: dict[models.identifier.SiteIdentifier, str] = {}
            for row in r.row_stream:
                # Extract values
                site_identifier = models.identifier.SiteIdentifier.from_row(row)

                # Check there is an identifier, even though it is mandatory field, it can be missing here
                # because this method is called for cross-validation, regardless of if this template is valid.
                if not site_identifier:
                    continue

                footprint_wkt: shapely.geometry.base.BaseGeometry | None = row["footprintWKT"]
                longitude: decimal.Decimal | None = row["decimalLongitude"]
                latitude: decimal.Decimal | None = row["decimalLatitude"]
                datum: str | None = row["geodeticDatum"]

                # if no valid datum for row then don't add to map.
                if datum is None:
                    continue

                try:
                    # Default to using the footprint wkt + geodetic datum
                    if footprint_wkt is not None:
                        # Create string and add to map for site id
                        result[site_identifier] = str(
                            models.spatial.Geometry(
                                raw=footprint_wkt.centroid,
                                datum=datum,
                            ).to_rdf_literal()
                        )
                        continue

                    # If not footprint then we revert to using supplied longitude & latitude
                    if longitude is not None and latitude is not None:
                        # Create string and add to map for site id
                        result[site_identifier] = str(
                            models.spatial.Geometry(
                                raw=shapely.Point([float(longitude), float(latitude)]),
                                datum=datum,
                            ).to_rdf_literal()
                        )
                except models.spatial.GeometryError:
                    continue

            return result

    def apply_mapping_row(
        self,
        *,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        extra_schema: frictionless.Schema,
        base_iri: rdflib.Namespace,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
        **kwargs: Any,
    ) -> None:
        """Applies mapping for a row in the `survey_site_data.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            extra_schema (frictionless.Schema): Schema of extra fields.
            base_iri (rdflib.Namespace): Optional base IRI to use for mapping.
            submission_iri: Optional submission IRI
            submitted_on_date: The date the data was submitted.
        """
        # TERN.Site subject IRI - Note this needs to match the iri construction of the
        # survey site visit and occurrence template mapping, ensuring they will resolve properly.
        # If existingBDRSiteIRI is specified, just use that as-is for the IRI.
        site_id: str | None = row["siteID"]
        site_id_src: str | None = row["siteIDSource"]
        existing_site_iri: str | None = row["existingBDRSiteIRI"]
        if existing_site_iri:
            site = rdflib.URIRef(existing_site_iri)
        elif site_id and site_id_src:
            site = utils.iri_patterns.site_iri(site_id_src, site_id)
        else:
            raise ValueError("Invalid row missing SiteID and existingBDRSiteIRI")

        # When siteID+siteIDSource are provided,
        # the site gets a schema:identifier with this datatype.
        if site_id and site_id_src:
            site_id_datatype = utils.iri_patterns.datatype_iri("siteID", site_id_src)
            site_id_agent = utils.iri_patterns.agent_iri("org", site_id_src)
            site_id_attribution = utils.iri_patterns.attribution_iri("resourceProvider", site_id_src)
        else:
            site_id_datatype = None
            site_id_agent = None
            site_id_attribution = None

        # Conditionally create related site URI
        related_site_id: str | None = row["relatedSiteID"]
        related_site_id_source: str | None = row["relatedSiteIDSource"]
        related_site_iri: str | None = row["relatedSiteIRI"]
        related_site: rdflib.URIRef | None
        if related_site_iri:
            related_site = rdflib.URIRef(related_site_iri)
        elif related_site_id and related_site_id_source:
            related_site = utils.iri_patterns.site_iri(related_site_id_source, related_site_id)
        else:
            related_site = None

        # Conditionally create uris dependent on dataGeneralizations
        data_generalizations: str | None = row["dataGeneralizations"]
        if data_generalizations:
            data_generalizations_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "dataGeneralizations", data_generalizations
            )
            data_generalizations_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "dataGeneralizations", data_generalizations
            )
            data_generalizations_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Site", "dataGeneralizations", data_generalizations
            )
        else:
            data_generalizations_attribute = None
            data_generalizations_value = None
            data_generalizations_collection = None

        # Create habitat attribute and value objects
        habitat_objects: list[AttributeValue] = []
        if habitats := row["habitat"]:
            for habitat in habitats:
                habitat_objects.append(
                    AttributeValue(
                        raw=habitat,
                        attribute=utils.iri_patterns.attribute_iri(base_iri, "habitat", habitat),
                        value=utils.iri_patterns.attribute_value_iri(base_iri, "habitat", habitat),
                        collection=utils.iri_patterns.attribute_collection_iri(base_iri, "Site", "habitat", habitat),
                    )
                )

        # Add site
        self.add_site(
            uri=site,
            dataset=dataset,
            submission_iri=submission_iri,
            site_id_datatype=site_id_datatype,
            related_site=related_site,
            row=row,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add site id datatype
        self.add_site_id_datatype(
            uri=site_id_datatype,
            attribution=site_id_attribution,
            row=row,
            graph=graph,
        )

        # Add site id attribution
        self.add_site_id_attribution(
            uri=site_id_attribution,
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
                submission_iri=submission_iri,
            )

            # Add habitat value
            self.add_habitat_value(
                uri=habitat_object.value,
                dataset=dataset,
                raw=habitat_object.raw,
                graph=graph,
                submitted_on_date=submitted_on_date,
            )

            # Add habitat attribute Collection
            self.add_habitat_collection(
                uri=habitat_object.collection,
                raw_habitat_value=habitat_object.raw,
                attribute=habitat_object.attribute,
                site=site,
                dataset=dataset,
                graph=graph,
                submission_iri=submission_iri,
            )

        # Add data generalizations attribute
        self.add_data_generalizations_attribute(
            uri=data_generalizations_attribute,
            value=data_generalizations_value,
            dataset=dataset,
            row=row,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add data generalizations value
        self.add_data_generalizations_value(
            uri=data_generalizations_value,
            row=row,
            graph=graph,
        )

        # Add data generalizations attribute Collection
        self.add_data_generalizations_collection(
            uri=data_generalizations_collection,
            raw_data_generalizations_value=data_generalizations,
            attribute=data_generalizations_attribute,
            site=site,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
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
            extra_schema=extra_schema,
        )

    def add_site(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        submission_iri: rdflib.URIRef | None,
        site_id_datatype: rdflib.URIRef | None,
        related_site: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds site to the graph.

        Args:
            uri: URI to use for this node.
            dataset: Dataset to which data belongs.
            submission_iri: IRI of the Submission being mapped.
            site_id_datatype: Datatype to use for
                the site id literal.
            related_site: Either the internal site uri that
                this site relates to or a URI for an external site.
            row: Row to retrieve data from.
            graph: Graph to be modified.
            submitted_on_date: The date the data was submitted.
        """
        # Extract relevant values
        existing_site_iri: str | None = row["existingBDRSiteIRI"]
        site_name = row["siteName"]
        site_type = row["siteType"]
        site_description = row["siteDescription"]
        locality = row["locality"]

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Site))

        # Add link to submission only when the Site is not an existing Site.
        if not existing_site_iri:
            if submission_iri:
                graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add siteID schema:identifier property, when siteID+siteIDSource are provided.
        site_id: str | None = row["siteID"]
        if site_id and site_id_datatype is not None:
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(site_id, datatype=site_id_datatype)))

        # Add related site if provided
        if related_site is not None and (relationship_to_related_site := row["relationshipToRelatedSite"]):
            # Retrieve vocab for field
            relationship_to_related_site_vocab = self.fields()["relationshipToRelatedSite"].get_vocab()
            # Retrieve term
            relationship_to_related_site_term = relationship_to_related_site_vocab().get(relationship_to_related_site)
            graph.add((uri, relationship_to_related_site_term, related_site))

        # Add site tern featuretype
        graph.add((uri, utils.namespaces.TERN.featureType, vocabs.site_type.SITE.iri))

        if site_type:
            # Retrieve vocab for field
            site_type_vocab = self.fields()["siteType"].get_flexible_vocab()

            # Retrieve term or create on the fly
            site_type_term = site_type_vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(
                site_type
            )

            # Add to site type graph
            graph.add((uri, rdflib.SDO.additionalType, site_type_term))

        # Add site name if available
        if site_name:
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(site_name)))

        # Add site description if available
        if site_description:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(site_description)))

        # Add locality as location description
        if locality:
            graph.add((uri, utils.namespaces.TERN.locationDescription, rdflib.Literal(locality)))

    def add_site_id_datatype(
        self,
        uri: rdflib.URIRef | None,
        attribution: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site id datatype to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            attribution (rdflib.URIRef | None): Attribution that the datatype corresponds to.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{row['siteIDSource']} Site ID")))

        # Add definition
        graph.add((uri, rdflib.SKOS.definition, rdflib.Literal("An identifier for the site")))

        # Add attribution
        if attribution is not None:
            graph.add((uri, rdflib.PROV.qualifiedAttribution, attribution))

    def add_site_id_attribution(
        self,
        uri: rdflib.URIRef | None,
        agent: rdflib.URIRef | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site id attribution to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            agent (rdflib.URIRef | None): Agent that the attribution corresponds to.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # Add attribution
        graph.add((uri, a, rdflib.PROV.Attribution))

        # Add agent
        if agent is not None:
            graph.add((uri, rdflib.PROV.agent, agent))

        # Add hadRole
        graph.add((uri, rdflib.PROV.hadRole, DATA_ROLE_RESOURCE_PROVIDER))

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
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add tern values
        graph.add((uri, utils.namespaces.TERN.attribute, HABITAT))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(raw)))
        graph.add((uri, utils.namespaces.TERN.hasValue, value))

    def add_habitat_value(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        raw: str,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Add a habitat value node to graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            dataset (rdflib.URIRef): Dataset data belongs.
            raw (str): Raw data provided.
            graph (rdflib.Graph): Graph to be modified.
            submitted_on_date: The date the data was submitted.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        # Add label
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(raw)))

        # Retrieve vocab for field
        vocab = self.fields()["habitat"].get_flexible_vocab()

        # Add flexible vocab term
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(raw)
        graph.add((uri, rdflib.RDF.value, term))

    def add_habitat_collection(
        self,
        uri: rdflib.URIRef,
        raw_habitat_value: str,
        attribute: rdflib.URIRef,
        site: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a habitat attribute Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_habitat_value: Habitat value from template.
            attribute: The uri for the attribute node.
            site: The uri for the site node.
            dataset: The uri for the dateset node.
            graph: The graph.
            submission_iri: Optional submission IRI
        """
        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add identifier
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(f"Site Collection - Habitat - {raw_habitat_value}")))
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to this site
        graph.add((uri, rdflib.SDO.hasPart, site))
        # Add link to attribute
        graph.add((uri, utils.namespaces.TERN.hasAttribute, attribute))

    def add_data_generalizations_attribute(
        self,
        uri: rdflib.URIRef | None,
        value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add tern values
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_DATA_GENERALIZATIONS))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["dataGeneralizations"])))
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

    def add_data_generalizations_collection(
        self,
        uri: rdflib.URIRef | None,
        raw_data_generalizations_value: str | None,
        attribute: rdflib.URIRef | None,
        site: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a Data Generalizations attribute Collection to the graph

        Args:
            uri: The uri for the Collection.
            raw_data_generalizations_value: DataGeneralizations value from template.
            attribute: The uri for the attribute node.
            site: The uri for the site node.
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
        if raw_data_generalizations_value:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Site Collection - Data Generalizations - {raw_data_generalizations_value}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to this site
        graph.add((uri, rdflib.SDO.hasPart, site))
        # Add link to attribute
        if attribute is not None:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, attribute))

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
        geometry = models.spatial.Geometry(
            raw=footprint_wkt,
            datum=geodetic_datum,
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))
        graph.add((uri, rdflib.SDO.spatial, geometry_node))

        # Add coordinate uncertainty if available
        coordinate_uncertainty = row["coordinateUncertaintyInMeters"]
        if coordinate_uncertainty:
            spatial_accuracy = rdflib.Literal(coordinate_uncertainty, datatype=rdflib.XSD.double)
            graph.add((geometry_node, utils.namespaces.GEO.hasMetricSpatialAccuracy, spatial_accuracy))
        else:
            spatial_accuracy = None

        # Add original geometry supplied as statement
        self.add_geometry_supplied_as(
            subj=uri,
            pred=rdflib.SDO.spatial,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
            spatial_accuracy=spatial_accuracy,
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
        geometry = models.spatial.Geometry(
            raw=models.spatial.LatLong(decimal_latitude, decimal_longitude),
            datum=geodetic_datum,
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))
        graph.add((uri, rdflib.SDO.spatial, geometry_node))

        # Add coordinate uncertainty if available
        coordinate_uncertainty = row["coordinateUncertaintyInMeters"]
        if coordinate_uncertainty:
            spatial_accuracy = rdflib.Literal(coordinate_uncertainty, datatype=rdflib.XSD.double)
            graph.add((geometry_node, utils.namespaces.GEO.hasMetricSpatialAccuracy, spatial_accuracy))
        else:
            spatial_accuracy = None

        # Add original geometry supplied as statement
        self.add_geometry_supplied_as(
            subj=uri,
            pred=rdflib.SDO.spatial,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
            spatial_accuracy=spatial_accuracy,
        )


# Register Mapper
base.mapper.register_mapper(SurveySiteMapper)
