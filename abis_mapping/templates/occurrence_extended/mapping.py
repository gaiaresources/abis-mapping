"""Provides ABIS Mapper for `occurrence_extended.csv` Template"""


# Standard
import datetime

# Third-Party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import utils
from abis_mapping import plugins
from abis_mapping import vocabs

# Typing
from typing import Iterator, Optional


# Default Dataset Metadata
DATASET_DEFAULT_NAME = "Example Occurrence Extended Dataset"
DATASET_DEFAULT_DESCRIPTION = "Example Occurrence Extended Dataset by Gaia Resources"
DATASET_DEFAULT_PROVIDER = "Example Provider Gaia Resources"
DATASET_DEFAULT_PROVIDER_URL = "https://www.gaiaresources.com.au/"

# Constants and Shortcuts
# These constants are specific to this template, and as such are defined here
# rather than in a common `utils` module.
a = rdflib.RDF.type
CONCEPT_AUSTRALIA = rdflib.URIRef("https://sws.geonames.org/2077456/")
CONCEPT_TAXON = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/70646576-6dc7-4bc5-a9d8-c4c366850df0")
CONCEPT_SITE = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5bf7ae21-a454-440b-bdd7-f2fe982d8de4")
CONCEPT_ID_UNCERTAINTY = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/54e40f12-8c13-495a-9f8d-838d78faa5a7")
CONCEPT_ID_REMARKS = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/45a86abc-43c7-4a30-ac73-fc8d62538140")
CONCEPT_PROCEDURE_SAMPLING = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/7930424c-f2e1-41fa-9128-61524b67dbd5")
CONCEPT_SCIENTIFIC_NAME = utils.rdf.uri("concept/scientificName", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_DATA_GENERALIZATIONS = utils.rdf.uri("concept/data-generalizations", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
CONCEPT_KINGDOM = utils.rdf.uri("concept/kingdom", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_TAXON_RANK = utils.rdf.uri("concept/taxonRank", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_INDIVIDUAL_COUNT = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/74c71500-0bae-43c9-8db0-bd6940899af1")
CONCEPT_ORGANISM_REMARKS = utils.rdf.uri("concept/organismRemarks", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_HABITAT = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99")
CONCEPT_BASIS_OF_RECORD = utils.rdf.uri("concept/basisOfRecord", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_OCCURRENCE_STATUS = utils.rdf.uri("concept/occurrenceStatus", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_PREPARATIONS = utils.rdf.uri("concept/preparations", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_ESTABLISHMENT_MEANS = utils.rdf.uri("concept/establishmentMeans", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
CONCEPT_LIFE_STAGE = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/abb0ee19-b2e8-42f3-8a25-d1f39ca3ebc3")
CONCEPT_SEX = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/05cbf534-c233-4aa8-a08c-00b28976ed36")
CONCEPT_REPRODUCTIVE_CONDITION = utils.rdf.uri("concept/reproductiveCondition", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
CONCEPT_ACCEPTED_NAME_USAGE = utils.rdf.uri("concept/acceptedNameUsage", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
CONCEPT_NAME_CHECK_METHOD = utils.rdf.uri("methods/name-check-method", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
CONCEPT_SEQUENCE = utils.rdf.uri("concept/sequence", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_CONSERVATION_STATUS = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/1466cc29-350d-4a23-858b-3da653fd24a6")  # noqa: E501
CONCEPT_CONSERVATION_JURISDICTION = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/755b1456-b76f-4d54-8690-10e41e25c5a7")  # noqa: E501

# Roles
ROLE_ORIGINATOR = rdflib.URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/originator")  # noqa: E501
ROLE_RIGHTS_HOLDER = rdflib.URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/rightsHolder")  # noqa: E501
ROLE_RESOURCE_PROVIDER = rdflib.URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/resourceProvider")  # noqa: E501
ROLE_CUSTODIAN = rdflib.URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/custodian")  # noqa: E501
ROLE_STAKEHOLDER = rdflib.URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/stakeholder")  # noqa: E501


class OccurrenceExtendedMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `occurrence_extended.csv`"""

    # Template ID and Instructions File
    template_id = "occurrence_extended.csv"
    instructions_file = "instructions.pdf"

    def apply_validation(
        self,
        data: base.types.ReadableType,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `occurrence_extended.csv` Template

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
                plugins.tabular.IsTabular(),
                plugins.empty.NotEmpty(),
                plugins.coordinates.ValidCoordinates(
                    latitude_name="decimalLatitude",
                    longitude_name="decimalLongitude",
                ),
                plugins.mutual_inclusion.MutuallyInclusive(
                    field_names=["threatStatus", "conservationJurisdiction"],
                )
            ]
        )

        # Return Validation Report
        return report

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        chunk_size: Optional[int] = None,
        dataset_iri: Optional[rdflib.URIRef] = None,
        provider_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping for the `occurrence_extended.csv` Template

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            provider_iri (Optional[rdflib.URIRef]): Optional provider IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """
        # Construct Resource (Table with Schema)
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=self.schema(),
            onerror="raise",  # Raise errors, it should already be valid here
        )

        # Infer Statistics and Count Number of Rows
        resource.infer(stats=True)
        rows = resource.stats["rows"]

        # Initialise Graph
        graph = utils.rdf.create_graph()

        # Check if Dataset IRI Supplied
        if not dataset_iri:
            # Create Dataset IRI
            dataset_iri = utils.rdf.uri(f"dataset/{DATASET_DEFAULT_NAME}", base_iri)

            # Add Example Default Dataset if not Supplied
            self.add_default_dataset(
                uri=dataset_iri,
                graph=graph,
            )

        # Check if Dataset Provider IRI Supplied
        if not provider_iri:
            # Create Dataset Provider IRI
            provider_iri = utils.rdf.uri(f"provider/{DATASET_DEFAULT_PROVIDER}", base_iri)

            # Add Example Default Dataset Provider if not Supplied
            self.add_default_provider(
                uri=provider_iri,
                graph=graph,
            )

        # Create Terminal Feature of Interest IRI
        terminal_foi = utils.rdf.uri("location/Australia", base_iri)

        # Add Terminal Feature of Interest (Australia)
        self.add_terminal_feature_of_interest(
            uri=terminal_foi,
            dataset=dataset_iri,
            graph=graph,
        )

        # Loop through Rows
        for row in resource:
            # Map Row
            self.apply_mapping_row(
                row=row,
                dataset=dataset_iri,
                provider=provider_iri,
                terminal_foi=terminal_foi,
                graph=graph,
                base_iri=base_iri,
            )

            # Check Whether to Yield a Chunk
            if utils.chunking.should_chunk(row, rows, chunk_size):
                # Yield Chunk
                yield graph

                # Initialise New Graph
                graph = utils.rdf.create_graph()

        # Return
        return graph

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider: rdflib.URIRef,
        terminal_foi: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> rdflib.Graph:
        """Applies Mapping for a Row in the `occurrence_extended.csv` Template

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset uri this row is apart of.
            provider (rdflib.URIRef): Dataset Provider uri for this row.
            terminal_foi (rdflib.URIRef): Terminal feature of interest.
            graph (rdflib.Graph): Graph to map row into.
            base_iri (Optional[rdflib.Namespace]): Optional base IRI namespace
                to use for mapping.

        Returns:
            rdflib.Graph: Graph with row mapped into it.
        """
        # Create URIs
        provider_owner_institution = utils.rdf.uri(f"provider/{row['ownerInstitutionCode']}", base_iri)
        provider_institution = utils.rdf.uri(f"provider/{row['institutionCode']}", base_iri)
        provider_identified = utils.rdf.uri(f"provider/{row['identifiedBy']}", base_iri)
        provider_recorded = utils.rdf.uri(f"provider/{row['recordedBy']}", base_iri)
        sample_field = utils.rdf.uri(f"sample/field/{row.row_number}", base_iri)
        sampling_field = utils.rdf.uri(f"sampling/field/{row.row_number}", base_iri)
        sample_specimen = utils.rdf.uri(f"sample/specimen/{row.row_number}", base_iri)
        sampling_specimen = utils.rdf.uri(f"sampling/specimen/{row.row_number}", base_iri)
        text_scientific_name = utils.rdf.uri(f"scientificName/{row.row_number}", base_iri)
        text_verbatim_id = utils.rdf.uri(f"verbatimID/{row.row_number}", base_iri)
        observation_scientific_name = utils.rdf.uri(f"observation/scientificName/{row.row_number}", base_iri)
        observation_verbatim_id = utils.rdf.uri(f"observation/verbatimID/{row.row_number}", base_iri)
        id_qualifier_attribute = utils.rdf.uri(f"attribute/identificationQualifier/{row.row_number}", base_iri)
        id_qualifier_value = utils.rdf.uri(f"value/identificationQualifier/{row.row_number}", base_iri)
        id_remarks_attribute = utils.rdf.uri(f"attribute/identificationRemarks/{row.row_number}", base_iri)
        id_remarks_value = utils.rdf.uri(f"value/identificationRemarks/{row.row_number}", base_iri)
        data_generalizations_attribute = utils.rdf.uri(f"attribute/dataGeneralizations/{row.row_number}", base_iri)
        data_generalizations_value = utils.rdf.uri(f"value/dataGeneralizations/{row.row_number}", base_iri)
        kingdom_attribute = utils.rdf.uri(f"attribute/kingdom/{row.row_number}", base_iri)
        kingdom_value = utils.rdf.uri(f"value/kingdom/{row.row_number}", base_iri)
        taxon_rank_attribute = utils.rdf.uri(f"attribute/taxonRank/{row.row_number}", base_iri)
        taxon_rank_value = utils.rdf.uri(f"value/taxonRank/{row.row_number}", base_iri)
        individual_count_observation = utils.rdf.uri(f"observation/individualCount/{row.row_number}", base_iri)
        individual_count_value = utils.rdf.uri(f"value/individualCount/{row.row_number}", base_iri)
        organism_remarks_observation = utils.rdf.uri(f"observation/organismRemarks/{row.row_number}", base_iri)
        organism_remarks_value = utils.rdf.uri(f"value/organismRemarks/{row.row_number}", base_iri)
        habitat_attribute = utils.rdf.uri(f"attribute/habitat/{row.row_number}", base_iri)
        habitat_value = utils.rdf.uri(f"value/habitat/{row.row_number}", base_iri)
        basis_attribute = utils.rdf.uri(f"attribute/basisOfRecord/{row.row_number}", base_iri)
        basis_value = utils.rdf.uri(f"value/basisOfRecord/{row.row_number}", base_iri)
        occurrence_status_observation = utils.rdf.uri(f"observation/occurrenceStatus/{row.row_number}", base_iri)
        occurrence_status_value = utils.rdf.uri(f"value/occurrenceStatus/{row.row_number}", base_iri)
        preparations_attribute = utils.rdf.uri(f"attribute/preparations/{row.row_number}", base_iri)
        preparations_value = utils.rdf.uri(f"value/preparations/{row.row_number}", base_iri)
        establishment_means_observation = utils.rdf.uri(f"observation/establishmentMeans/{row.row_number}", base_iri)
        establishment_means_value = utils.rdf.uri(f"value/establishmentMeans/{row.row_number}", base_iri)
        life_stage_observation = utils.rdf.uri(f"observation/lifeStage/{row.row_number}", base_iri)
        life_stage_value = utils.rdf.uri(f"value/lifeStage/{row.row_number}", base_iri)
        sex_observation = utils.rdf.uri(f"observation/sex/{row.row_number}", base_iri)
        sex_value = utils.rdf.uri(f"value/sex/{row.row_number}", base_iri)
        reproductive_condition_observation = utils.rdf.uri(f"observation/reproductiveCondition/{row.row_number}", base_iri)  # noqa: E501
        reproductive_condition_value = utils.rdf.uri(f"value/reproductiveCondition/{row.row_number}", base_iri)
        accepted_name_usage_observation = utils.rdf.uri(f"observation/acceptedNameUsage/{row.row_number}", base_iri)  # noqa: E501
        accepted_name_usage_value = utils.rdf.uri(f"value/acceptedNameUsage/{row.row_number}", base_iri)
        sampling_sequencing = utils.rdf.uri(f"sampling/sequencing/{row.row_number}", base_iri)
        sample_sequence = utils.rdf.uri(f"sample/sequence/{row.row_number}", base_iri)
        threat_status_observation = utils.rdf.uri(f"observation/threatStatus/{row.row_number}", base_iri)
        threat_status_value = utils.rdf.uri(f"value/threatStatus/{row.row_number}", base_iri)
        conservation_jurisdiction_attribute = utils.rdf.uri(f"attribute/conservationJurisdiction/{row.row_number}", base_iri)  # noqa: E501
        conservation_jurisdiction_value = utils.rdf.uri(f"value/conservationJurisdiction/{row.row_number}", base_iri)
        provider_determined_by = utils.rdf.uri(f"provider/{row['threatStatusDeterminedBy']}", base_iri)

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
            recorded_by=provider_recorded,
            owner_institution_code=provider_owner_institution,
            institution_code=provider_institution,
            graph=graph,
        )

        # Add Sampling Field
        self.add_sampling_field(
            uri=sampling_field,
            row=row,
            dataset=dataset,
            dataset_provider=provider,
            provider=provider_recorded,
            feature_of_interest=terminal_foi,
            sample_field=sample_field,
            generalizations=data_generalizations_attribute,
            habitat=habitat_attribute,
            basis=basis_attribute,
            graph=graph,
        )

        # Add Sample Specimen
        self.add_sample_specimen(
            uri=sample_specimen,
            row=row,
            dataset=dataset,
            sampling_specimen=sampling_specimen,
            sample_field=sample_field,
            preparations=preparations_attribute,
            owner_institution_code=provider_owner_institution,
            institution_code=provider_institution,
            graph=graph,
        )

        # Add Sampling Specimen
        self.add_sampling_specimen(
            uri=sampling_specimen,
            row=row,
            dataset=dataset,
            sample_field=sample_field,
            sample_specimen=sample_specimen,
            generalizations=data_generalizations_attribute,
            basis=basis_attribute,
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
            dataset=dataset,
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
            sample_field=sample_field,
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
            sample_field=sample_field,
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
            dataset=dataset,
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
            dataset=dataset,
            graph=graph,
        )

        # Add Individual Count Observation
        self.add_individual_count_observation(
            uri=individual_count_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            individual_count_value=individual_count_value,
        )

        # Add Individual Count Value
        self.add_individual_count_value(
            uri=individual_count_value,
            row=row,
            graph=graph,
        )

        # Add Organism Remarks Observation
        self.add_organism_remarks_observation(
            uri=organism_remarks_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            organism_remarks_value=organism_remarks_value,
        )

        # Add Organism Remarks Value
        self.add_organism_remarks_value(
            uri=organism_remarks_value,
            row=row,
            graph=graph,
        )

        # Add Habitat Attribute
        self.add_habitat_attribute(
            uri=habitat_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            habitat_value=habitat_value,
        )

        # Add Habitat Value
        self.add_habitat_value(
            uri=habitat_value,
            row=row,
            graph=graph,
        )

        # Add Basis of Record Attribute
        self.add_basis_attribute(
            uri=basis_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            basis_value=basis_value,
        )

        # Add Basis of Record Value
        self.add_basis_value(
            uri=basis_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Owner Institution Provider
        self.add_owner_institution_provider(
            uri=provider_owner_institution,
            row=row,
            graph=graph,
        )

        # Add Institution Provider
        self.add_institution_provider(
            uri=provider_institution,
            row=row,
            graph=graph,
        )

        # Add Occurrence Status Observation
        self.add_occurrence_status_observation(
            uri=occurrence_status_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            occurrence_status_value=occurrence_status_value,
        )

        # Add Occurrence Status Value
        self.add_occurrence_status_value(
            uri=occurrence_status_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Preparations Attribute
        self.add_preparations_attribute(
            uri=preparations_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            preparations_value=preparations_value,
        )

        # Add Preparations Value
        self.add_preparations_value(
            uri=preparations_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Establishment Means Observation
        self.add_establishment_means_observation(
            uri=establishment_means_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            establishment_means_value=establishment_means_value,
        )

        # Add Establishment Means Value
        self.add_establishment_means_value(
            uri=establishment_means_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Life Stage Observation
        self.add_life_stage_observation(
            uri=life_stage_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            sample_specimen=sample_specimen,
            life_stage_value=life_stage_value,
        )

        # Add Life Stage Value
        self.add_life_stage_value(
            uri=life_stage_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Sex Observation
        self.add_sex_observation(
            uri=sex_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            sample_specimen=sample_specimen,
            sex_value=sex_value,
        )

        # Add Sex Value
        self.add_sex_value(
            uri=sex_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Reproductive Condition Observation
        self.add_reproductive_condition_observation(
            uri=reproductive_condition_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            sample_field=sample_field,
            sample_specimen=sample_specimen,
            reproductive_condition_value=reproductive_condition_value,
        )

        # Add Reproductive Condition Value
        self.add_reproductive_condition_value(
            uri=reproductive_condition_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Accepted Name Usage Observation
        self.add_accepted_name_usage_observation(
            uri=accepted_name_usage_observation,
            row=row,
            graph=graph,
            dataset=dataset,
            scientific_name=text_scientific_name,
            accepted_name_usage_value=accepted_name_usage_value,
        )

        # Add Accepted Name Usage Value
        self.add_accepted_name_usage_value(
            uri=accepted_name_usage_value,
            row=row,
            graph=graph,
        )

        # Add Sampling Sequencing
        self.add_sampling_sequencing(
            uri=sampling_sequencing,
            row=row,
            dataset=dataset,
            feature_of_interest=sample_specimen,
            sample_sequence=sample_sequence,
            graph=graph,
        )

        # Add Sample Sequence
        self.add_sample_sequence(
            uri=sample_sequence,
            row=row,
            dataset=dataset,
            feature_of_interest=sample_specimen,
            sampling_sequencing=sampling_sequencing,
            graph=graph,
        )

        # Add Provider Threat Status Determined By
        self.add_provider_determined_by(
            uri=provider_determined_by,
            row=row,
            graph=graph,
        )

        # Add Threat Status Observation
        self.add_threat_status_observation(
            uri=threat_status_observation,
            row=row,
            dataset=dataset,
            accepted_name_usage=accepted_name_usage_value,
            scientific_name=text_scientific_name,
            threat_status_value=threat_status_value,
            jurisdiction_attribute=conservation_jurisdiction_attribute,
            determined_by=provider_determined_by,
            graph=graph,
        )

        # Add Threat Status Value
        self.add_threat_status_value(
            uri=threat_status_value,
            row=row,
            dataset=dataset,
            graph=graph,
        )

        # Add Conservation Jurisdiction Attribute
        self.add_conservation_jurisdiction_attribute(
            uri=conservation_jurisdiction_attribute,
            row=row,
            graph=graph,
            dataset=dataset,
            conservation_jurisdiction_value=conservation_jurisdiction_value,
        )

        # Add Conservation Jurisdiction Value
        self.add_conservation_jurisdiction_value(
            uri=conservation_jurisdiction_value,
            row=row,
            graph=graph,
        )

        # Return
        return graph

    def add_default_dataset(
        self,
        uri: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Default Example Dataset to the Graph

        Args:
            graph (rdflib.Graph): Graph to add to
        """
        # Add Default Dataset to Graph
        graph.add((uri, a, utils.namespaces.TERN.RDFDataset))
        graph.add((uri, rdflib.DCTERMS.title, rdflib.Literal(DATASET_DEFAULT_NAME)))
        graph.add((uri, rdflib.DCTERMS.description, rdflib.Literal(DATASET_DEFAULT_DESCRIPTION)))
        graph.add((uri, rdflib.DCTERMS.issued, utils.rdf.toTimestamp(datetime.date.today())))

    def add_default_provider(
        self,
        uri: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Default Example Dataset Provider to the Graph

        Args:
            graph (rdflib.Graph): Graph to add to
        """
        # Add Default Dataset Provider to Graph
        graph.add((uri, a, rdflib.SDO.Organization))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(DATASET_DEFAULT_PROVIDER)))
        graph.add((uri, rdflib.SDO.url, rdflib.Literal(DATASET_DEFAULT_PROVIDER_URL, datatype=rdflib.XSD.anyURI)))

    def add_terminal_feature_of_interest(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the Terminal Feature of Interest to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Add Terminal Feature of Interest to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_SITE))

        # Add Geometry
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.sfWithin, CONCEPT_AUSTRALIA))

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
        sample_field: rdflib.URIRef,
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
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
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

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else sample_field

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.identification_method.IDENTIFICATION_METHOD.get(
            graph=graph,
            value=row["identificationMethod"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("scientificName-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, scientific_name))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["scientificName"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(date_identified)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))

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
        sample_field: rdflib.URIRef,
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
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
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

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else sample_field

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.identification_method.IDENTIFICATION_METHOD.get(
            graph=graph,
            value=row["identificationMethod"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("verbatimID-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, verbatim_id))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["verbatimIdentification"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(date_identified)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))

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
        dataset: rdflib.URIRef,
        dataset_provider: rdflib.URIRef,
        provider: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        generalizations: rdflib.URIRef,
        habitat: rdflib.URIRef,
        basis: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sampling Field to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            dataset_provider (rdflib.URIRef): Dataset Provider this belongs to
            provider (rdflib.URIRef): Provider associated with this node
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node.
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            generalizations (rdflib.URIRef): Data Generalizations associated
                with this node
            habitat (rdflib.URIRef): Habitat associated with this node
            basis (rdflib.URIRef): Basis Of Record associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(
            latitude=row["decimalLatitude"],
            longitude=row["decimalLongitude"],
            datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(row["geodeticDatum"]),
        )

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.SAMPLING_PROTOCOL.get(
            graph=graph,
            value=row["samplingProtocol"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("field-sampling")))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, feature_of_interest))
        graph.add((uri, rdflib.SOSA.hasResult, sample_field))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(row["eventDate"])))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))

        # Check for recordID
        if row["recordID"]:
            # Add Identifier
            graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(row["recordID"])))

            # Add Identifier Provenance
            provenance = rdflib.BNode()
            graph.add((provenance, a, rdflib.RDF.Statement))
            graph.add((provenance, rdflib.RDF.subject, uri))
            graph.add((provenance, rdflib.RDF.predicate, rdflib.DCTERMS.identifier))
            graph.add((provenance, rdflib.RDF.object, rdflib.Literal(row["recordID"])))
            graph.add((provenance, rdflib.SKOS.prefLabel, rdflib.Literal("recordID source")))
            qualifier = rdflib.BNode()
            graph.add((provenance, rdflib.PROV.qualifiedAttribution, qualifier))
            graph.add((qualifier, rdflib.PROV.Agent, dataset_provider))
            graph.add((qualifier, utils.namespaces.ABISDM.hadRole, ROLE_RESOURCE_PROVIDER))

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

        # Check for habitat
        if row["habitat"]:
            # Add Habitat Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, habitat))

        # Check for basisOfRecord and if Row has no Specimen
        if not has_specimen(row) and row["basisOfRecord"]:
            # Add Basis Of Record Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, basis))

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
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Qualifier Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check identificationQualifier
        if not row["identificationQualifier"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.identification_qualifier.IDENTIFICATION_QUALIFIER.get(
            graph=graph,
            value=row["identificationQualifier"],
            source=dataset,
        )

        # Identification Qualifier Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("identificationQualifier")))
        graph.add((uri, rdflib.RDF.value, vocab))

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
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        generalizations: rdflib.URIRef,
        basis: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sampling Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            generalizations (rdflib.URIRef): Data Generalizations associated
                with this node
            basis (rdflib.URIRef): Basis Of Record associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check if Row has a Specimen
        if not has_specimen(row):
            return

        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(
            latitude=row["decimalLatitude"],
            longitude=row["decimalLongitude"],
            datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(row["geodeticDatum"]),
        )

        # Get Timestamp
        timestamp = row["preparedDate"] or row["eventDate"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sampling")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, sample_specimen))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_SAMPLING))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(timestamp)))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))

        # Add Spatial Qualifier
        spatial_comment = "Location unknown, location of field sampling used as proxy"
        spatial_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, spatial_qualifier))
        graph.add((spatial_qualifier, a, rdflib.RDF.Statement))
        graph.add((spatial_qualifier, rdflib.RDF.value, utils.namespaces.GEO.hasGeometry))
        graph.add((spatial_qualifier, rdflib.RDFS.comment, rdflib.Literal(spatial_comment)))

        # Check for preparedDate
        if not row["preparedDate"]:
            # Add Temporal Qualifier
            temporal_comment = "Date unknown, template eventDate used as proxy"
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Check for dataGeneralizations
        if row["dataGeneralizations"]:
            # Add Data Generalizations Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, generalizations))

        # Check for basisOfRecord and if Row has a Specimen
        if has_specimen(row) and row["basisOfRecord"]:
            # Add Basis Of Record Attribute
            graph.add((uri, utils.namespaces.TERN.hasAttribute, basis))

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
        recorded_by: rdflib.URIRef,
        owner_institution_code: rdflib.URIRef,
        institution_code: rdflib.URIRef,
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
            recorded_by (rdflib.URIRef): Recorded By Agent associated with this
                node
            owner_institution_code (rdflib.URIRef): Owner Institution Code
                Agent associated with this node
            institution_code (rdflib.URIRef): Institution Code Agent associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.kingdom.KINGDOM_OCCURRENCE.get(
            graph=graph,
            value=row["kingdom"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("field-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_field))
        graph.add((uri, rdflib.SOSA.isSampleOf, feature_of_interest))
        graph.add((uri, utils.namespaces.TERN.featureType, vocab))

        # Check for recordNumber
        if row["recordNumber"]:
            # Add to Graph
            graph.add((uri, utils.namespaces.DWC.recordNumber, rdflib.Literal(row["recordNumber"])))

        # Check for recordNumber and recordedBy
        if row["recordNumber"] and row["recordedBy"]:
            # Add Provenance (recordedBy)
            provenance = rdflib.BNode()
            graph.add((provenance, a, rdflib.RDF.Statement))
            graph.add((provenance, rdflib.RDF.subject, uri))
            graph.add((provenance, rdflib.RDF.predicate, utils.namespaces.DWC.recordNumber))
            graph.add((provenance, rdflib.RDF.object, rdflib.Literal(row["recordNumber"])))
            graph.add((provenance, rdflib.SKOS.prefLabel, rdflib.Literal("recordNumber source")))
            qualifier = rdflib.BNode()
            graph.add((provenance, rdflib.PROV.qualifiedAttribution, qualifier))
            graph.add((qualifier, rdflib.PROV.Agent, recorded_by))
            graph.add((qualifier, utils.namespaces.ABISDM.hadRole, ROLE_ORIGINATOR))

        # Check for occurrenceID
        if row["occurrenceID"]:
            # Add to Graph
            graph.add((uri, utils.namespaces.DWC.occurrenceID, rdflib.Literal(row["occurrenceID"])))

        # Check for occurrenceID and ownerInstitutionCode
        if row["occurrenceID"] and row["ownerInstitutionCode"]:
            # Add Provenance (ownerInstitutionCode)
            provenance = rdflib.BNode()
            graph.add((provenance, a, rdflib.RDF.Statement))
            graph.add((provenance, rdflib.RDF.subject, uri))
            graph.add((provenance, rdflib.RDF.predicate, utils.namespaces.DWC.occurrenceID))
            graph.add((provenance, rdflib.RDF.object, rdflib.Literal(row["occurrenceID"])))
            graph.add((provenance, rdflib.SKOS.prefLabel, rdflib.Literal("occurrenceID source")))
            qualifier = rdflib.BNode()
            graph.add((provenance, rdflib.PROV.qualifiedAttribution, qualifier))
            graph.add((qualifier, rdflib.PROV.Agent, owner_institution_code))
            graph.add((qualifier, utils.namespaces.ABISDM.hadRole, ROLE_CUSTODIAN))

    def add_sample_specimen(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sampling_specimen: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        preparations: rdflib.URIRef,
        owner_institution_code: rdflib.URIRef,
        institution_code: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sample Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sampling_specimen (rdflib.URIRef): Sampling Specimen associated
                with this node
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            preparations (rdflib.URIRef): Preparations Attribute associated
                with this node
            owner_institution_code (rdflib.URIRef): Owner Institution Code
                Agent associated with this node.
            institution_code (rdflib.URIRef): Institution Code Agent associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check if Row has a Specimen
        if not has_specimen(row):
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.kingdom.KINGDOM_SPECIMEN.get(
            graph=graph,
            value=row["kingdom"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_specimen))
        graph.add((uri, rdflib.SOSA.isSampleOf, sample_field))
        graph.add((uri, utils.namespaces.TERN.featureType, vocab))

        # Check for catalogNumber
        if row["catalogNumber"]:
            # Add to Graph
            graph.add((uri, utils.namespaces.DWC.catalogNumber, rdflib.Literal(row["catalogNumber"])))

        # Check for catalogNumber and ownerInstitutionCode
        if row["catalogNumber"] and row["ownerInstitutionCode"]:
            # Add Provenance (ownerInstitutionCode)
            provenance = rdflib.BNode()
            graph.add((provenance, a, rdflib.RDF.Statement))
            graph.add((provenance, rdflib.RDF.subject, uri))
            graph.add((provenance, rdflib.RDF.predicate, utils.namespaces.DWC.catalogNumber))
            graph.add((provenance, rdflib.RDF.object, rdflib.Literal(row["catalogNumber"])))
            graph.add((provenance, rdflib.SKOS.prefLabel, rdflib.Literal("catalogNumber source")))
            qualifier = rdflib.BNode()
            graph.add((provenance, rdflib.PROV.qualifiedAttribution, qualifier))
            graph.add((qualifier, rdflib.PROV.Agent, owner_institution_code))
            graph.add((qualifier, utils.namespaces.ABISDM.hadRole, ROLE_CUSTODIAN))

            # Check for collectionCode
            if row["collectionCode"]:
                # Add to Graph
                graph.add((provenance, utils.namespaces.DWC.collectionCode, rdflib.Literal(row["collectionCode"])))

        # Check for otherCatalogNumbers
        if row["otherCatalogNumbers"]:
            # Loop through Other Catalog Numbers
            for identifier in row["otherCatalogNumbers"]:
                # Add to Graph
                graph.add((uri, utils.namespaces.DWC.otherCatalogNumbers, rdflib.Literal(identifier)))

        # Check for otherCatalogNumbers and institutionCode
        if row["otherCatalogNumbers"] and row["institutionCode"]:
            # Loop through Other Catalog Numbers
            for identifier in row["otherCatalogNumbers"]:
                # Add Provenance (institutionCode)
                provenance = rdflib.BNode()
                graph.add((provenance, a, rdflib.RDF.Statement))
                graph.add((provenance, rdflib.RDF.subject, uri))
                graph.add((provenance, rdflib.RDF.predicate, utils.namespaces.DWC.otherCatalogNumbers))
                graph.add((provenance, rdflib.RDF.object, rdflib.Literal(identifier)))
                graph.add((provenance, rdflib.SKOS.prefLabel, rdflib.Literal("otherCatalogNumbers stakeholder")))
                qualifier = rdflib.BNode()
                graph.add((provenance, rdflib.PROV.qualifiedAttribution, qualifier))
                graph.add((qualifier, rdflib.PROV.Agent, institution_code))
                graph.add((qualifier, utils.namespaces.ABISDM.hadRole, ROLE_STAKEHOLDER))

        # Check for preparations
        if row["preparations"]:
            # Add Preparations
            graph.add((uri, utils.namespaces.TERN.hasAttribute, preparations))

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
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Kingdom Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.kingdom.KINGDOM.get(
            graph=graph,
            value=row["kingdom"],
            source=dataset,
        )

        # Kingdom Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"kingdom = {row['kingdom']}")))
        graph.add((uri, rdflib.RDF.value, vocab))

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
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Taxon Rank Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["taxonRank"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.taxon_tank.TAXON_RANK.get(
            graph=graph,
            value=row["taxonRank"],
            source=dataset,
        )

        # Taxon Rank Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"taxon rank = {row['taxonRank']}")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_individual_count_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        individual_count_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Individual Count Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            individual_count_value (rdflib.URIRef): Individual Count Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["individualCount"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Individual Count Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("individualCount-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, individual_count_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["individualCount"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_INDIVIDUAL_COUNT))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_individual_count_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Individual Count Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["individualCount"]:
            return

        # Individual Count Value
        graph.add((uri, a, utils.namespaces.TERN.Integer))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("individual-count")))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["individualCount"])))

    def add_organism_remarks_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        organism_remarks_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Organism Remarks Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            organism_remarks_value (rdflib.URIRef): Organism Remarks Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["organismRemarks"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Organism Remarks Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("organismRemarks-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, organism_remarks_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["organismRemarks"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_ORGANISM_REMARKS))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_organism_remarks_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Organism Remarks Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["organismRemarks"]:
            return

        # Organism Remarks Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("organism-remarks")))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["organismRemarks"])))

    def add_habitat_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        habitat_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Habitat Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            habitat_value (rdflib.URIRef): Habitat Value associated with this
                node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["habitat"]:
            return

        # Habitat Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_HABITAT))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["habitat"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, habitat_value))

    def add_habitat_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Habitat Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["habitat"]:
            return

        # Habitat Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("habitat")))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["habitat"])))

    def add_basis_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        basis_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Basis of Record Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            basis_value (rdflib.URIRef): Basis of Record Value associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["basisOfRecord"]:
            return

        # Basis of Record Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_BASIS_OF_RECORD))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["basisOfRecord"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, basis_value))

    def add_basis_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Basis of Record Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["basisOfRecord"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.basis_of_record.BASIS_OF_RECORD.get(
            graph=graph,
            value=row["basisOfRecord"],
            source=dataset,
        )

        # Basis of Record Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("basisOfRecord")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_owner_institution_provider(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Owner Institution Provider to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # TODO -> Retrieve this from a known list of institutions
        # Check Existence
        if not row["ownerInstitutionCode"]:
            return

        # Owner Institution Provider
        graph.add((uri, a, rdflib.SDO.Organization))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["ownerInstitutionCode"])))
        graph.add((uri, rdflib.SDO.url, rdflib.Literal("https://example.org/", datatype=rdflib.XSD.anyURI)))

    def add_institution_provider(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Institution Provider to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # TODO -> Retrieve this from a known list of institutions
        # Check Existence
        if not row["institutionCode"]:
            return

        # Institution Provider
        graph.add((uri, a, rdflib.SDO.Organization))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["institutionCode"])))
        graph.add((uri, rdflib.SDO.url, rdflib.Literal("https://example.org/", datatype=rdflib.XSD.anyURI)))

    def add_occurrence_status_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        occurrence_status_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Occurrence Status Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            occurrence_status_value (rdflib.URIRef): Occurrence Status Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["occurrenceStatus"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Occurrence Status Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("occurrenceStatus-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, occurrence_status_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["occurrenceStatus"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_OCCURRENCE_STATUS))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_occurrence_status_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Occurrence Status Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["occurrenceStatus"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.occurrence_status.OCCURRENCE_STATUS.get(
            graph=graph,
            value=row["occurrenceStatus"],
            source=dataset,
        )

        # Occurrence Status Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"occurrenceStatus = {row['occurrenceStatus']}")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_preparations_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        preparations_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Preparations Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            preparations_value (rdflib.URIRef): Preparations Value associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["preparations"]:
            return

        # Preparations Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_PREPARATIONS))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["preparations"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, preparations_value))

    def add_preparations_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Preparations Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["preparations"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.preparations.PREPARATIONS.get(
            graph=graph,
            value=row["preparations"],
            source=dataset,
        )

        # Preparations Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("preparations")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_establishment_means_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        establishment_means_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Establishment Means Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            establishment_means_value (rdflib.URIRef): Establishment Means
                Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["establishmentMeans"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Establishment Means Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("establishmentMeans-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, sample_field))
        graph.add((uri, rdflib.SOSA.hasResult, establishment_means_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["establishmentMeans"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_ESTABLISHMENT_MEANS))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_establishment_means_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Establishment Means Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["establishmentMeans"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.establishment_means.ESTABLISHMENT_MEANS.get(
            graph=graph,
            value=row["establishmentMeans"],
            source=dataset,
        )

        # Establishment Means Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("establishmentMeans-value")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_life_stage_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        life_stage_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Life Stage Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            life_stage_value (rdflib.URIRef): Life Stage Value associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["lifeStage"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else sample_field

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Life Stage Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("lifeStage-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, life_stage_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["lifeStage"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_LIFE_STAGE))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_life_stage_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Life Stage Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["lifeStage"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.life_stage.LIFE_STAGE.get(
            graph=graph,
            value=row["lifeStage"],
            source=dataset,
        )

        # Life Stage Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("lifeStage-value")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_sex_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        sex_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sex Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            sex_value (rdflib.URIRef): Sex Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["sex"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else sample_field

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Sex Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sex-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, sex_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["sex"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_SEX))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_sex_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sex Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["sex"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sex.SEX.get(
            graph=graph,
            value=row["sex"],
            source=dataset,
        )

        # Sex Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("sex-value")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_reproductive_condition_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sample_field: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        reproductive_condition_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Reproductive Condition Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            reproductive_condition_value (rdflib.URIRef): Reproductive
                Condition Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["reproductiveCondition"]:
            return

        # Get Timestamp
        event_date = row["eventDate"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else sample_field

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Reproductive Condition Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("reproductiveCondition-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, reproductive_condition_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["reproductiveCondition"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_REPRODUCTIVE_CONDITION))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(event_date)))

        # Add Temporal Qualifier
        temporal_comment = "Date unknown, template eventDate used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        method_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, method_qualifier))
        graph.add((method_qualifier, a, rdflib.RDF.Statement))
        graph.add((method_qualifier, rdflib.RDF.value, rdflib.SOSA.usedProcedure))
        graph.add((method_qualifier, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_reproductive_condition_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Reproductive Condition Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["reproductiveCondition"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.reproductive_condition.REPRODUCTIVE_CONDITION.get(
            graph=graph,
            value=row["reproductiveCondition"],
            source=dataset,
        )

        # Reproductive Condition Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("reproductiveCondition-value")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_accepted_name_usage_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        scientific_name: rdflib.URIRef,
        accepted_name_usage_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Accepted Name Usage Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            scientific_name (rdflib.URIRef): Scientific Name associated with
                this node
            accepted_name_usage_value (rdflib.URIRef): Accepted Name Usage
                Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["acceptedNameUsage"]:
            return

        # Get Timestamps
        event_date = row["eventDate"]
        date_identified = row["dateIdentified"] or row["eventDate"]

        # Accepted Name Usage Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("acceptedNameUsage-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, scientific_name))
        graph.add((uri, rdflib.SOSA.hasResult, accepted_name_usage_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["acceptedNameUsage"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_NAME_CHECK_METHOD))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(date_identified)))

        # Add Temporal Qualifier
        timestamp_used = "dateIdentified" if row["dateIdentified"] else "eventDate"  # Determine which field was used
        temporal_comment = f"Date unknown, template {timestamp_used} used as proxy"
        temporal_qualifier = rdflib.BNode()
        graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
        graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
        graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
        graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

    def add_accepted_name_usage_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Accepted Name Usage Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["acceptedNameUsage"]:
            return

        # Accepted Name Usage Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("acceptedNameUsage-value")))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["acceptedNameUsage"])))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_ACCEPTED_NAME_USAGE))

    def add_sampling_sequencing(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sample_sequence: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sampling Sequencing to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sample_field (rdflib.URIRef): Sample Field associated with this
                node
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node
            sample_sequence (rdflib.URIRef): Sample Sequence associated with
                this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["associatedSequences"]:
            return

        # Create WKT from Latitude and Longitude
        wkt = utils.rdf.toWKT(
            latitude=row["decimalLatitude"],
            longitude=row["decimalLongitude"],
            datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(row["geodeticDatum"]),
        )

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sequencing_method.SEQUENCING_METHOD.get(
            graph=graph,
            value=row["sequencingMethod"],
            source=dataset,
        )

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sequencing-sampling")))
        geometry = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry))
        graph.add((geometry, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, feature_of_interest))
        graph.add((uri, rdflib.SOSA.hasResult, sample_sequence))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(row["eventDate"])))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

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

    def add_sample_sequence(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sampling_sequencing: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Sample Sequence to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node
            sampling_sequencing (rdflib.URIRef): Sampling Sequencing associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["associatedSequences"]:
            return

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sequence-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_sequencing))
        graph.add((uri, rdflib.SOSA.isSampleOf, feature_of_interest))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_SEQUENCE))

        # Loop Through Associated Sequences
        for identifier in row["associatedSequences"]:
            # Add Identifier
            graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(identifier)))

    def add_provider_determined_by(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Determined By Provider to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check for threatStatusDeterminedBy
        if not row["threatStatusDeterminedBy"]:
            return

        # Add to Graph
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.FOAF.name, rdflib.Literal(row["threatStatusDeterminedBy"])))

    def add_threat_status_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        accepted_name_usage: rdflib.URIRef,
        scientific_name: rdflib.URIRef,
        threat_status_value: rdflib.URIRef,
        jurisdiction_attribute: rdflib.URIRef,
        determined_by: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Threat Status Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            accepted_name_usage (rdflib.URIRef): Accepted Name Usage associated
                with this node
            scientific_name (rdflib.URIRef): Scientific Name associated with
                this node
            threat_status_value (rdflib.URIRef): Threat Status Value associated
                with this node
            jurisdiction_attribute (rdflib.URIRef): Conservation Jurisdiction
                Attribute associated with this node
            determined_by (rdflib.URIRef): Determined By Provider associated
                with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["threatStatus"]:
            return

        # Choose Feature of Interest
        # Feature of Interest is the Accepted Name Usage Value if it exists,
        # otherwise it is the Scientific Name Text
        foi = accepted_name_usage if row["acceptedNameUsage"] else scientific_name

        # Get Timestamps
        # Prefer `threatStatusDateDetermined` > `dateIdentified` > `eventDate` (fallback)
        event_date = row["eventDate"]
        date_determined = (
            row["threatStatusDateDetermined"]
            or row["dateIdentified"]
            or row["preparedDate"]
            or row["eventDate"]
        )

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.check_protocol.CHECK_PROTOCOL.get(
            graph=graph,
            value=row["threatStatusCheckProtocol"],
            source=dataset,
        )

        # Threat Status Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("threatStatus-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, threat_status_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["threatStatus"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_CONSERVATION_STATUS))
        graph.add((uri, rdflib.PROV.wasInfluencedBy, jurisdiction_attribute))
        phenomenon_time = rdflib.BNode()
        graph.add((uri, rdflib.SOSA.phenomenonTime, phenomenon_time))
        graph.add((phenomenon_time, a, rdflib.TIME.Instant))
        graph.add((phenomenon_time, utils.rdf.inXSDSmart(event_date), utils.rdf.toTimestamp(event_date)))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        graph.add((uri, utils.namespaces.TERN.resultDateTime, utils.rdf.toTimestamp(date_determined)))

        # Check for threatStatusDeterminedBy
        if row["threatStatusDeterminedBy"]:
            # Add wasAssociatedWith
            graph.add((uri, rdflib.PROV.wasAssociatedWith, determined_by))

        # Check for threatStatusDateDetermined
        if not row["threatStatusDateDetermined"]:
            # Determine Used Date Column
            date_used = (
                "dateIdentified" if row["dateIdentified"] else
                "preparedDate" if row["preparedDate"] else
                "eventDate"
            )

            # Comment
            comment = f"Date unknown, template {date_used} used as proxy"

            # Add Temporal Qualifier
            temporal_qualifier = rdflib.BNode()
            graph.add((uri, utils.namespaces.TERN.qualifiedValue, temporal_qualifier))
            graph.add((temporal_qualifier, a, rdflib.RDF.Statement))
            graph.add((temporal_qualifier, rdflib.RDF.value, utils.namespaces.TERN.resultDateTime))
            graph.add((temporal_qualifier, rdflib.RDFS.comment, rdflib.Literal(comment)))

    def add_threat_status_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Threat Status Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["threatStatus"]:
            return

        # Combine conservationJurisdiction and threatStatus
        value = f"{row['conservationJurisdiction']}/{row['threatStatus']}"

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.threat_status.THREAT_STATUS.get(
            graph=graph,
            value=value,
            source=dataset,
        )

        # Threat Status Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"Conservation status = {row['threatStatus']}")))
        graph.add((uri, rdflib.RDF.value, vocab))

    def add_conservation_jurisdiction_attribute(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        conservation_jurisdiction_value: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Conservation Jurisdiction Attribute to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            conservation_jurisdiction_value (rdflib.URIRef): Conservation
                Jurisdiction Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["conservationJurisdiction"]:
            return

        # Conservation Jurisdiction Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        graph.add((uri, rdflib.VOID.inDataset, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_CONSERVATION_JURISDICTION))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(row["conservationJurisdiction"])))
        graph.add((uri, utils.namespaces.TERN.hasValue, conservation_jurisdiction_value))

    def add_conservation_jurisdiction_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Conservation Jurisdiction Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["conservationJurisdiction"]:
            return

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.conservation_jurisdiction.CONSERVATION_JURISDICTION.get(row["conservationJurisdiction"])

        # Construct Label
        label = f"Conservation Jurisdiction = {row['conservationJurisdiction']}"

        # Conservation Jurisdiction Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(label)))
        graph.add((uri, rdflib.RDF.value, vocab))


# Helper Functions
# These utility helper functions are specific to this template, and as such are
# defined here instead of in a common utilities module.
def has_specimen(row: frictionless.Row) -> bool:
    """Determines whether a row has a specimen associated with it or not.

    This method is used when determining whether to add the specimen specific
    `/sampling/specimen/x` and `/sample/specimen/x` nodes to the graph.

    Args:
        row (frictionless.Row): Row to retrieve data from.

    Returns:
        bool: Whether this row has a specimen associated with it.
    """
    # Check Specimen Rules
    if any((
        row["preparations"],
        row["catalogNumber"],
        row["associatedSequences"],
        row["otherCatalogNumbers"],
        row["recordNumber"],
    )):
        # If any of `preparations`, `catalogNumber`, `associatedSequences`,
        # `otherCatalogNumbers` or `recordNumber` are provided, regardless of
        # the value of `basisOfRecord` we can infer that there is a specimen
        # associated with the row.
        specimen = True

    elif (
        not row["basisOfRecord"]  # Blank
        or vocabs.basis_of_record.HUMAN_OBSERVATION.match(row["basisOfRecord"])  # HumanObservation
        or vocabs.basis_of_record.OCCURRENCE.match(row["basisOfRecord"])  # Occurrence
    ):
        # Otherwise, if none of `preparations`, `catalogNumber`,
        # `associatedSequences`, `otherCatalogNumbers` or `recordNumber` were
        # provided, and the `basisOfRecord` is either blank or one of
        # "HumanObservation" or "Occurrence", then we cannot infer that there
        # is a specimen associated with the row.
        specimen = False

    else:
        # Finally, none of `preparations`, `catalogNumber`,
        # `associatedSequences`, `otherCatalogNumbers` or `recordNumber` were
        # provided, but the `basisOfRecord` is a value that implies that there
        # is a specimen associated with the row.
        specimen = True

    # Return
    return specimen


# Register Mapper
base.mapper.ABISMapper.register_mapper(OccurrenceExtendedMapper)
