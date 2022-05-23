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
CONCEPT_ID_UNCERTAINTY = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/54e40f12-8c13-495a-9f8d-838d78faa5a7")
CONCEPT_ID_REMARKS = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a86abc-43c7-4a30-ac73-fc8d62538140")
CONCEPT_PROCEDURE_ID = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2eef4e87-beb3-449a-9251-f59f5c07d653")
CONCEPT_PROCEDURE_SAMPLING = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/7930424c-f2e1-41fa-9128-61524b67dbd5")
CONCEPT_SCIENTIFIC_NAME = utils.rdf.uri("concept/scientificName")  # TODO -> Need real URI
CONCEPT_DATA_GENERALIZATIONS = utils.rdf.uri("concept/data-generalizations")  # TODO -> Need real URI
CONCEPT_KINGDOM = utils.rdf.uri("concept/kingdom")  # TODO -> Need real URI
CONCEPT_TAXON_RANK = utils.rdf.uri("concept/taxonRank")  # TODO -> Need real URI

# Controlled Vocabularies
VOCAB_GEODETIC_DATUM = {
    # AGD84
    "AGD84": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4203"),
    "EPSG:4203": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4203"),
    # GDA2020
    "GDA2020": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/7844"),
    "EPSG:7844": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/7844"),
    # GDA94
    "GDA94": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4283"),
    "EPSG:4283": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/9.9.1/4283"),
    # WGS84
    "WGS84": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4326"),
    "EPSG:4326": rdflib.URIRef("http://www.opengis.net/def/crs/EPSG/0/4326"),
}
VOCAB_SAMPLING_PROTOCOL = {
    None: utils.rdf.uri("sampling-protocol/default"),  # Default  # TODO -> Need real URI
    "human observation": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157"),
    "by hand": utils.rdf.uri("sampling-protocol/by-hand"),  # TODO -> Need real URI,
}
VOCAB_KINGDOM_OCCURRENCE = {
    "Plantae": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/b311c0d3-4a1a-4932-a39c-f5cdc1afa611"),
    "Animalia": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"),
    "Fungi": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"),
}
VOCAB_KINGDOM_SPECIMEN = {
    "Plantae": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2e122e23-881c-43fa-a921-a8745f016ceb"),
    "Animalia": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"),
    "Fungi": rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"),  # TODO -> ?
}
VOCAB_KINGDOM = {
    "Plantae": utils.rdf.uri("kingdom/plantae"),  # TODO -> Need real URI,
    "Animalia": utils.rdf.uri("kingdom/animalia"),  # TODO -> Need real URI,
    "Fungi": utils.rdf.uri("kingdom/fungi"),  # TODO -> Need real URI,
}
VOCAB_TAXON_RANK = {
    None: utils.rdf.uri("taxonRank/default"),  # Default  # TODO -> Need real URI
    "kingdom": utils.rdf.uri("taxonRank/kingdom"),  # TODO -> Need real URI
    "phylum": utils.rdf.uri("taxonRank/phylum"),  # TODO -> Need real URI
    "class": utils.rdf.uri("taxonRank/class"),  # TODO -> Need real URI
    "order": utils.rdf.uri("taxonRank/order"),  # TODO -> Need real URI
    "family": utils.rdf.uri("taxonRank/family"),  # TODO -> Need real URI
    "genus": utils.rdf.uri("taxonRank/genus"),  # TODO -> Need real URI
    "species": utils.rdf.uri("taxonRank/species"),  # TODO -> Need real URI
}


class DWCMVPMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `dwc_mvp.csv`"""

    # Template ID and Instructions File
    template_id = "dwc_mvp.csv"
    instructions_file = "instructions.pdf"

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
        report: frictionless.Report = resource.validate(
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
        data_generalizations_attribute = utils.rdf.uri(f"attribute/dataGeneralizations/{row_number}", base_iri)
        data_generalizations_value = utils.rdf.uri(f"value/dataGeneralizations/{row_number}", base_iri)
        kingdom_attribute = utils.rdf.uri(f"attribute/kingdom/{row_number}", base_iri)
        kingdom_value = utils.rdf.uri(f"value/kingdom/{row_number}", base_iri)
        taxon_rank_attribute = utils.rdf.uri(f"attribute/taxonRank/{row_number}", base_iri)
        taxon_rank_value = utils.rdf.uri(f"value/taxonRank/{row_number}", base_iri)

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
            row=row,
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
            generalizations=data_generalizations_attribute,
            graph=graph,
        )

        # Add Sample Specimen
        self.add_sample_specimen(
            uri=sample_specimen,
            row=row,
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
            generalizations=data_generalizations_attribute,
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
            qualifier=id_qualifier_attribute,
            remarks=id_remarks_attribute,
            kingdom=kingdom_attribute,
            taxon_rank=taxon_rank_attribute,
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

        # Add Data Generalizations Attribute
        self.add_data_generalizations_attribute(
            uri=data_generalizations_attribute,
            row=row,
            dataset=dataset,
            data_generalizations_value=data_generalizations_value,
            graph=graph,
        )

        # Add Data Generalizations Value
        self.add_data_generalizations_value(
            uri=data_generalizations_value,
            row=row,
            graph=graph,
        )

        # Add Kingdom Attribute
        self.add_kingdom_attribute(
            uri=kingdom_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            kingdom_value=kingdom_value,
        )

        # Add Kingdom Value
        self.add_kingdom_value(
            uri=kingdom_value,
            row=row,
            graph=graph,
        )

        # Add Taxon Rank Attribute
        self.add_taxon_rank_attribute(
            uri=taxon_rank_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            taxon_rank_value=taxon_rank_value,
        )

        # Add Taxon Rank Value
        self.add_taxon_rank_value(
            uri=taxon_rank_value,
            row=row,
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
        # Check for identifiedBy
        if not row["identifiedBy"]:
            return

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
        # Check for recordedBy
        if not row["recordedBy"]:
            return

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
        qualifier: rdflib.URIRef,
        remarks: rdflib.URIRef,
        kingdom: rdflib.URIRef,
        taxon_rank: rdflib.URIRef,
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
            qualifier (rdflib.URIRef): Identification Qualifier attribute
                associated with this node
            remarks (rdflib.URIRef): Identification Remarks attribute
                associated with this node
            kingdom (rdflib.URIRef): Kingdom attribute associated with this
                node
            taxon_rank (rdflib.URIRef): Taxon Rank attribute associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Get Timestamps
        event_date = row["eventDate"]
        date_identified = row["dateIdentified"] or row["eventDate"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("scientificName-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_specimen))
        graph.add((uri, rdflib.SOSA.hasResult, scientific_name))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["scientificName"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), rdflib.Literal(event_date)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(date_identified)))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_ID))

        # Check for identifiedBy
        if row["identifiedBy"]:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Comment
            comment = "Date unknown, template eventDate used as proxy"

            # Add Temporal Qualifier
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(comment)))

        # Check for identificationQualifier
        if row["identificationQualifier"]:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, qualifier))

        # Check for identificationRemarks
        if row["identificationRemarks"]:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, remarks))

        # Add Kingdom
        graph.add((uri, utils.namespaces.TERN.hasAttribute, kingdom))

        # Check for taxonRank
        if row["taxonRank"]:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, taxon_rank))

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
        # Check for verbatimIdentification
        if not row["verbatimIdentification"]:
            return

        # Get Timestamps
        event_date = row["eventDate"]
        date_identified = row["dateIdentified"] or row["eventDate"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("verbatimID-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_specimen))
        graph.add((uri, rdflib.SOSA.hasResult, verbatim_id))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["verbatimIdentification"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), rdflib.Literal(event_date)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(date_identified)))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_ID))

        # Check for identifiedBy
        if row["identifiedBy"]:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Comment
            comment = "Date unknown, template eventDate used as proxy"

            # Add Temporal Qualifier
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(comment)))

    def add_sampling_field(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        provider: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        generalizations: rdflib.URIRef,
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
            generalizations (rdflib.URIRef): Data Generalizations associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(
            latitude=row["decimalLatitude"],
            longitude=row["decimalLongitude"],
            datum=VOCAB_GEODETIC_DATUM[row["geodeticDatum"]],
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("field-sampling")))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, feature_of_interest))
        graph.add((uri, rdflib.SOSA.hasResult, sample_field))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, rdflib.Literal(row["eventDate"])))
        graph.add((uri, rdflib.SOSA.usedProcedure, VOCAB_SAMPLING_PROTOCOL[row["samplingProtocol"]]))

        # Check for recordedBy
        if row["recordedBy"]:
            # Add Associated Provider
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))

        # Check for locality
        if row["locality"]:
            # Add Location Description
            graph.add((uri, utils.namespaces.TERN.locationDescription, rdflib.Literal(row["locality"])))

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Check for dataGeneralizations
        if row["dataGeneralizations"]:
            # Add Data Generalizations Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, generalizations))

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
        # Check identificationQualifier
        if not row["identificationQualifier"]:
            return

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
        # Check identificationQualifier
        if not row["identificationQualifier"]:
            return

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
        # Check identificationRemarks
        if not row["identificationRemarks"]:
            return

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
        # Check identificationRemarks
        if not row["identificationRemarks"]:
            return

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
        generalizations: rdflib.URIRef,
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
            generalizations (rdflib.URIRef): Data Generalizations associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(
            latitude=row["decimalLatitude"],
            longitude=row["decimalLongitude"],
            datum=VOCAB_GEODETIC_DATUM[row["geodeticDatum"]],
        )

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
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Spatial Qualifier
        spatial_comment = "Location unknown, location of field sampling used as proxy"
        spatial_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, spatial_qualifier))
        graph.add((spatial_qualifier, a, rdflib.RDF.Statement))
        graph.add((spatial_qualifier, rdflib.RDF.value, utils.namespaces.GEO.hasGeometry))
        graph.add((spatial_qualifier, rdflib.RDFS.comment, rdflib.Literal(spatial_comment)))

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Check for dataGeneralizations
        if row["dataGeneralizations"]:
            # Add Data Generalizations Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, generalizations))

    def add_text_verbatim_id(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Text Verbatim ID to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check for verbatimIdentification
        if not row["verbatimIdentification"]:
            return

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["verbatimIdentification"])))

    def add_sample_field(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sampling_field: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sample Field to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
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
        graph.add((uri, utils.namespaces.TERN.featureType, VOCAB_KINGDOM_OCCURRENCE[row["kingdom"]]))

    def add_sample_specimen(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
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
        graph.add((uri, utils.namespaces.TERN.featureType, VOCAB_KINGDOM_SPECIMEN[row["kingdom"]]))

    def add_data_generalizations_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        data_generalizations_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Data Generalizations Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            data_generalizations_value (rdflib.URIRef): Data Generalizations
                Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["dataGeneralizations"]:
            return

        # Data Generalizations Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_DATA_GENERALIZATIONS))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["dataGeneralizations"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, data_generalizations_value))

    def add_data_generalizations_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Data Generalizations Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["dataGeneralizations"]:
            return

        # Data Generalizations Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["dataGeneralizations"])))

    def add_kingdom_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        kingdom_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Kingdom Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            kingdom_value (rdflib.URIRef): Kingdom Value associated with this
                node
            graph (rdflib.Graph): Graph to add to
        """
        # Kingdom Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_KINGDOM))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["kingdom"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, kingdom_value))

    def add_kingdom_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Kingdom Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Kingdom Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"kingdom = {row['kingdom']}")))
        graph.add((uri, rdflib.RDF.value, VOCAB_KINGDOM[row["kingdom"]]))

    def add_taxon_rank_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        taxon_rank_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Taxon Rank Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            taxon_rank_value (rdflib.URIRef): Taxon Rank Value associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["taxonRank"]:
            return

        # Taxon Rank Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_TAXON_RANK))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["taxonRank"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, taxon_rank_value))

    def add_taxon_rank_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Taxon Rank Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["taxonRank"]:
            return

        # Taxon Rank Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"taxon rank = {row['taxonRank']}")))
        graph.add((uri, rdflib.RDF.value, VOCAB_TAXON_RANK[row["taxonRank"]]))


# Register Mapper
base.mapper.ABISMapper.register_mapper(DWCMVPMapper)
