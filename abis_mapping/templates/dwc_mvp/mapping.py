"""Provides ABIS Mapper for `dwc_mvp.csv` Template"""


# Standard
import datetime

# Third-Party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import utils

# Typing
from typing import Optional


# Default Dataset Metadata
DATASET_DEFAULT_NAME = "Example DWC MVP Dataset"
DATASET_DEFAULT_DESCRIPTION = "Example DWC MVP Dataset by Gaia Resources"

# Constants and Shortcuts
# These constants are specific to this template, and as such are defined here
# rather than in a common `utils` module.
a = rdflib.RDF.type
CONCEPT_AUSTRALIA = rdflib.URIRef("https://sws.geonames.org/2077456/")
CONCEPT_TAXON = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/70646576-6dc7-4bc5-a9d8-c4c366850df0")
CONCEPT_SITE = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5bf7ae21-a454-440b-bdd7-f2fe982d8de4")
CONCEPT_HUMAN_OBSERVATION = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157")
CONCEPT_ID_UNCERTAINTY = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/54e40f12-8c13-495a-9f8d-838d78faa5a7")
CONCEPT_ID_REMARKS = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a86abc-43c7-4a30-ac73-fc8d62538140")
CONCEPT_PLANT_OCCURRENCE = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b311c0d3-4a1a-4932-a39c-f5cdc1afa611")
CONCEPT_PLANT_INDIVIDUAL = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/60d7edf8-98c6-43e9-841c-e176c334d270")
CONCEPT_PROCEDURE_ID = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2eef4e87-beb3-449a-9251-f59f5c07d653")
CONCEPT_PROCEDURE_SAMPLING = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/7930424c-f2e1-41fa-9128-61524b67dbd5")
CONCEPT_SCIENTIFIC_NAME = utils.rdf.uri("concept/scientificName")  # TODO -> Need real URI


class DWCMVPMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `dwc_mvp.csv`"""

    # Template ID and Instructions File
    template_id = "dwc_mvp.csv"
    instructions_file = "README.md"

    def apply_validation(
        self,
        data: base.types.ReadableType,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `dwc_mvp.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct Resource (Table with Schema)
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=self.schema(),
            onerror="ignore",  # Ignore errors, they will be handled in the report
        )

        # Validate
        report: frictionless.Report = frictionless.validate_resource(
            source=resource,
            checks=[
                # Extra Custom Checks
                utils.checks.NotTabular(),
                utils.checks.NotEmpty(),
                utils.checks.ValidCoordinates(
                    latitude_name="decimalLatitude",
                    longitude_name="decimalLongitude",
                ),
            ]
        )

        # Return Validation Report
        return report

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> rdflib.Graph:
        """Applies Mapping for the `dwc_mvp.csv` Template

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.

        Returns:
            rdflib.Graph: ABIS Conformant RDF Graph.
        """
        # Construct Resource (Table with Schema)
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=self.schema(),
            onerror="raise",  # Raise errors, it should already be valid here
        )

        # Initialise Graph
        graph = utils.rdf.create_graph()

        # Check if Dataset IRI Supplied
        if not dataset_iri:
            # Create Default Dataset if not Supplied
            dataset_iri = utils.rdf.uri(f"dataset/{DATASET_DEFAULT_NAME}", base_iri)
            graph.add((dataset_iri, a, utils.namespaces.TERN.RDFDataset))
            graph.add((dataset_iri, rdflib.DCTERMS.title, rdflib.Literal(DATASET_DEFAULT_NAME)))
            graph.add((dataset_iri, rdflib.DCTERMS.description, rdflib.Literal(DATASET_DEFAULT_DESCRIPTION)))
            graph.add((dataset_iri, rdflib.DCTERMS.issued, rdflib.Literal(datetime.date.today())))

        # Create Terminal FOI (Australia)
        australia = utils.rdf.uri("location/Australia", base_iri)
        geometry = rdflib.BNode()
        graph.add((australia, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((australia, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.sfWithin, CONCEPT_AUSTRALIA))
        graph.add((australia, rdflib.VOID.inDataset, dataset_iri))
        graph.add((australia, utils.namespaces.TERN.featureType, CONCEPT_SITE))

        # Loop through Rows
        for row_number, row in enumerate(resource):
            # Map Row
            self.apply_mapping_row(row, row_number, dataset_iri, australia, graph, base_iri)

        # Return
        return graph

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        row_number: int,
        dataset: rdflib.URIRef,
        terminal_foi: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> rdflib.Graph:
        """Applies Mapping for a Row in the `dwc_mvp.csv` Template

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            row_number (int): Row number to be processed.
            dataset (rdflib.URIRef): Dataset uri this row is apart of.
            terminal_foi (rdflib.URIRef): Terminal feature of interest.
            graph (rdflib.Graph): Graph to map row into.
            base_iri (Optional[rdflib.Namespace]): Optional base IRI namespace
                to use for mapping.

        Returns:
            rdflib.Graph: Graph with row mapped into it.
        """
        # Create URIs
        provider_identified = utils.rdf.uri(f"provider/{row['identifiedBy']}", base_iri)
        provider_recorded = utils.rdf.uri(f"provider/{row['recordedBy']}", base_iri)
        sample_field = utils.rdf.uri(f"sample/field/{row_number}", base_iri)
        sampling_field = utils.rdf.uri(f"sampling/field/{row_number}", base_iri)
        sample_specimen = utils.rdf.uri(f"sample/specimen/{row_number}", base_iri)
        sampling_specimen = utils.rdf.uri(f"sampling/specimen/{row_number}", base_iri)
        text_scientific_name = utils.rdf.uri(f"scientificName/{row_number}", base_iri)
        text_verbatim_id = utils.rdf.uri(f"verbatimID/{row_number}", base_iri)
        observation_scientific_name = utils.rdf.uri(f"observation/scientificName/{row_number}", base_iri)
        observation_verbatim_id = utils.rdf.uri(f"observation/verbatimID/{row_number}", base_iri)
        id_qualifier_attribute = utils.rdf.uri(f"attribute/identificationQualifier/{row_number}", base_iri)
        id_qualifier_value = utils.rdf.uri(f"value/identificationQualifier/{row_number}", base_iri)
        id_remarks_attribute = utils.rdf.uri(f"attribute/identificationRemarks/{row_number}", base_iri)
        id_remarks_value = utils.rdf.uri(f"value/identificationRemarks/{row_number}", base_iri)

        # Add Provider Identified By
        self.add_provider_identified(
            uri=provider_identified,
            row=row,
            graph=graph,
        )

        # Add Provider Recorded By
        self.add_provider_recorded(
            uri=provider_recorded,
            row=row,
            graph=graph,
        )

        # Add Sample Field
        self.add_sample_field(
            uri=sample_field,
            dataset=dataset,
            feature_of_interest=terminal_foi,
            sampling_field=sampling_field,
            graph=graph,
        )

        # Add Sampling Field
        self.add_sampling_field(
            uri=sampling_field,
            row=row,
            provider=provider_recorded,
            feature_of_interest=terminal_foi,
            sample_field=sample_field,
            graph=graph,
        )

        # Add Sample Specimen
        self.add_sample_specimen(
            uri=sample_specimen,
            dataset=dataset,
            sampling_specimen=sampling_specimen,
            sample_field=sample_field,
            graph=graph,
        )

        # Add Sampling Specimen
        self.add_sampling_specimen(
            uri=sampling_specimen,
            row=row,
            sample_field=sample_field,
            sample_specimen=sample_specimen,
            graph=graph,
        )

        # Add Text for Scientific Name
        self.add_text_scientific_name(
            uri=text_scientific_name,
            dataset=dataset,
            row=row,
            graph=graph,
        )

        # Add Identification Qualifier Attribute
        self.add_id_qualifier_attribute(
            uri=id_qualifier_attribute,
            row=row,
            dataset=dataset,
            id_qualifier_value=id_qualifier_value,
            graph=graph,
        )

        # Add Identification Qualifier Value
        self.add_id_qualifier_value(
            uri=id_qualifier_value,
            row=row,
            graph=graph,
        )

        # Add Identification Remarks Attribute
        self.add_id_remarks_attribute(
            uri=id_remarks_attribute,
            row=row,
            dataset=dataset,
            id_remarks_value=id_remarks_value,
            graph=graph,
        )

        # Add Identification Remarks Value
        self.add_id_remarks_value(
            uri=id_remarks_value,
            row=row,
            graph=graph,
        )

        # Add Text for Verbatim ID
        self.add_text_verbatim_id(
            uri=text_verbatim_id,
            row=row,
            qualifier=id_qualifier_attribute,
            remarks=id_remarks_attribute,
            graph=graph,
        )

        # Add Observation for Scientific Name
        self.add_observation_scientific_name(
            uri=observation_scientific_name,
            row=row,
            dataset=dataset,
            provider=provider_identified,
            sample_specimen=sample_specimen,
            scientific_name=text_scientific_name,
            graph=graph,
        )

        # Add Observation for Verbatim ID
        self.add_observation_verbatim_id(
            uri=observation_verbatim_id,
            row=row,
            dataset=dataset,
            provider=provider_identified,
            sample_specimen=sample_specimen,
            verbatim_id=text_verbatim_id,
            graph=graph,
        )

        # Return
        return graph

    def add_provider_identified(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identified By Provider to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.FOAF.name, rdflib.Literal(row["identifiedBy"])))

    def add_provider_recorded(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Recorded By Provider to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.FOAF.name, rdflib.Literal(row["recordedBy"])))

    def add_observation_scientific_name(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        scientific_name: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Observation Scientific Name to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider (rdflib.URIRef): Provider associated with this node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            scientific_name (rdflib.URIRef): Scientific Name associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Get Timestamp
        timestamp = row["dateIdentified"] or row["eventDate"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("scientificName-observation")))
        graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_specimen))
        graph.add((uri, rdflib.SOSA.hasResult, scientific_name))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["scientificName"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(timestamp), rdflib.Literal(timestamp)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(timestamp)))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_ID))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Add Temporal Qualifier
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDF.value, rdflib.SOSA.phenomenonTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal("Date inferred from the eventDate")))

    def add_observation_verbatim_id(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        verbatim_id: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Observation Verbatim ID to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider (rdflib.URIRef): Provider associated with this node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            verbatim_id (rdflib.URIRef): Verbatim ID associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Get Timestamp
        timestamp = row["dateIdentified"] or row["eventDate"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("verbatimID-observation")))
        graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_specimen))
        graph.add((uri, rdflib.SOSA.hasResult, verbatim_id))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["verbatimIdentification"])))
        graph.add((uri, rdflib.SOSA.observedProperty, rdflib.URIRef(CONCEPT_TAXON)))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(timestamp), rdflib.Literal(timestamp)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(timestamp)))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_ID))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Add Temporal Qualifier
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDF.value, rdflib.SOSA.phenomenonTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal("Date inferred from the eventDate")))

    def add_sampling_field(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        provider: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sampling Field to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            provider (rdflib.URIRef): Provider associated with this node
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node.
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            graph (rdflib.Graph): Graph to add to
        """
        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(row["decimalLatitude"], row["decimalLongitude"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("field-sampling")))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, feature_of_interest))
        graph.add((uri, rdflib.SOSA.hasResult, sample_field))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(row["eventDate"])))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_HUMAN_OBSERVATION))

    def add_id_qualifier_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        id_qualifier_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Qualifier Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            row_number (int): Row number for this row
            dataset (rdflib.URIRef): Dataset this belongs to
            id_qualifier_value (rdflib.URIRef): Identification Qualifier Value
                associated with this node.
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if row.get("identificationQualifier"):
            # Identification Qualifier Attribute
            graph.add((uri, a, utils.namespaces.TERN.Attribute))
            graph.add((uri, rdflib.VOID.inDataset, dataset))
            graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_ID_UNCERTAINTY))
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["identificationQualifier"])))
            graph.add((uri, utils.namespaces.TERN.hasValue, id_qualifier_value))

    def add_id_qualifier_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Qualifier Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if row.get("identificationQualifier"):
            # Identification Qualifier Value
            graph.add((uri, a, utils.namespaces.TERN.Text))
            graph.add((uri, a, utils.namespaces.TERN.Value))
            graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["identificationQualifier"])))

    def add_id_remarks_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        id_remarks_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Remarks Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            id_remarks_value (rdflib.URIRef): Identification Remarks Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if row.get("identificationRemarks"):
            # Identification Remarks Attribute
            graph.add((uri, a, utils.namespaces.TERN.Attribute))
            graph.add((uri, rdflib.VOID.inDataset, dataset))
            graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_ID_REMARKS))
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["identificationRemarks"])))
            graph.add((uri, utils.namespaces.TERN.hasValue, id_remarks_value))

    def add_id_remarks_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Remarks Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if row.get("identificationRemarks"):
            # Identification Remarks Value
            graph.add((uri, a, utils.namespaces.TERN.Text))
            graph.add((uri, a, utils.namespaces.TERN.Value))
            graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["identificationRemarks"])))

    def add_text_scientific_name(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Text Scientific Name to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset this belongs to
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("scientificName")))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["scientificName"])))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_SCIENTIFIC_NAME))

    def add_sampling_specimen(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        sample_field: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sampling Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(row["decimalLatitude"], row["decimalLongitude"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sampling")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, sample_specimen))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_SAMPLING))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(row["eventDate"])))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))

        # Add Temporal Qualifier
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal("Date inferred from the eventDate")))

        # Add Spatial Qualifier
        spatial_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, spatial_qualifier))
        graph.add((spatial_qualifier, a, rdflib.RDF.Statement))
        graph.add((spatial_qualifier, rdflib.RDF.value, utils.namespaces.GEO.hasGeometry))
        graph.add((spatial_qualifier, rdflib.RDFS.comment, rdflib.Literal("Location inferred from the field sampling")))

    def add_text_verbatim_id(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        qualifier: rdflib.URIRef,
        remarks: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Text Verbatim ID to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            qualifier (rdflib.URIRef): Identification Qualifier attribute
                associated with this node
            remarks (rdflib.URIRef): Identification Remarks attribute
                associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["verbatimIdentification"])))

        # Check for Qualifier and Remarks
        if row.get("identificationQualifier"):
            graph.add((uri, utils.namespaces.TERN.hasAttribute, qualifier))
        if row.get("identificationRemarks"):
            graph.add((uri, utils.namespaces.TERN.hasAttribute, remarks))

    def add_sample_field(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sampling_field: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sample Field to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset this belongs to
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node.
            sampling_field (rdflib.URIRef): Sampling Field associated with this
                node
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("field-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_field))
        graph.add((uri, rdflib.SOSA.isSampleOf, feature_of_interest))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_PLANT_OCCURRENCE))

    def add_sample_specimen(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        sampling_specimen: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sample Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            sampling_specimen (rdflib.URIRef): Sampling Specimen associated
                with this node
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_specimen))
        graph.add((uri, rdflib.SOSA.isSampleOf, sample_field))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_PLANT_INDIVIDUAL))


# Register Mapper
base.mapper.ABISMapper.register_mapper(DWCMVPMapper)
