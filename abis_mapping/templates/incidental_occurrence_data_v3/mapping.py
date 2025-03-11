"""Mapper implementation for the incidental occurrence data v3 template."""

# Standard library
import datetime
import decimal

# Third-Party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import utils
from abis_mapping import plugins
from abis_mapping import models
from abis_mapping import vocabs

# Typing
from typing import Any


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
CONCEPT_SCIENTIFIC_NAME = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/56195246-ec5d-4050-a1c6-af786fbec715")
CONCEPT_DATA_GENERALIZATIONS = utils.rdf.uri(
    "concept/data-generalizations", utils.namespaces.EXAMPLE
)  # TODO -> Need real URI
CONCEPT_TAXON_RANK = utils.rdf.uri("concept/taxonRank", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_INDIVIDUAL_COUNT = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/74c71500-0bae-43c9-8db0-bd6940899af1")
CONCEPT_ORGANISM_REMARKS = utils.rdf.uri("concept/organismRemarks", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_HABITAT = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99")
CONCEPT_BASIS_OF_RECORD = utils.rdf.uri("concept/basisOfRecord", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_OCCURRENCE_STATUS = utils.rdf.uri("concept/occurrenceStatus", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_PREPARATIONS = utils.rdf.uri("concept/preparations", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_ESTABLISHMENT_MEANS = utils.rdf.uri(
    "concept/establishmentMeans", utils.namespaces.EXAMPLE
)  # TODO -> Need real URI
CONCEPT_LIFE_STAGE = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/abb0ee19-b2e8-42f3-8a25-d1f39ca3ebc3")
CONCEPT_SEX = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/05cbf534-c233-4aa8-a08c-00b28976ed36")
CONCEPT_REPRODUCTIVE_CONDITION = utils.rdf.uri(
    "concept/reproductiveCondition", utils.namespaces.EXAMPLE
)  # TODO -> Need real URI
CONCEPT_ACCEPTED_NAME_USAGE = utils.rdf.uri(
    "concept/acceptedNameUsage", utils.namespaces.EXAMPLE
)  # TODO -> Need real URI
CONCEPT_NAME_CHECK_METHOD = utils.rdf.uri(
    "methods/name-check-method", utils.namespaces.EXAMPLE
)  # TODO -> Need real URI
CONCEPT_SEQUENCE = utils.rdf.uri("concept/sequence", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
CONCEPT_CONSERVATION_STATUS = rdflib.URIRef(
    "http://linked.data.gov.au/def/tern-cv/1466cc29-350d-4a23-858b-3da653fd24a6"
)
# TODO: Concept uri still to be created, for now leaving as the conservation jurisdiction uri.
CONCEPT_CONSERVATION_AUTHORITY = rdflib.URIRef(
    "http://linked.data.gov.au/def/tern-cv/755b1456-b76f-4d54-8690-10e41e25c5a7"
)
CONCEPT_SENSITIVITY_CATEGORY = utils.rdf.uri(
    "concept/sensitiveCategory", utils.namespaces.EXAMPLE
)  # TODO Need real URI
CONCEPT_ORGANISM_QUANTITY = utils.rdf.uri("concept/organismQuantity", utils.namespaces.EXAMPLE)  # TODO Need real URI

# Roles
DATA_ROLE_RESOURCE_PROVIDER = rdflib.URIRef("https://linked.data.gov.au/def/data-roles/resourceProvider")
DATA_ROLE_OWNER = rdflib.URIRef("https://linked.data.gov.au/def/data-roles/owner")


class IncidentalOccurrenceMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `incidental_occurrence_data.csv` - version 3"""

    def apply_validation(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `incidental_occurrence_data.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.
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
                        field_names=["eventDateStart", "eventDateEnd"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["threatStatus", "conservationAuthority"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["organismQuantity", "organismQuantityType"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["catalogNumber", "catalogNumberSource"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["otherCatalogNumbers", "otherCatalogNumbersSource"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["ownerRecordID", "ownerRecordIDSource"],
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=["sensitivityCategory", "sensitivityAuthority"],
                    ),
                ],
            ),
        )

        # Return Validation Report
        return report

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
        """Applies Mapping for a Row in the `incidental_occurrence_data.csv` Template

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset uri this row is apart of.
            graph (rdflib.Graph): Graph to map row into.
            extra_schema (frictionless.Schema): Schema of extra fields.
            base_iri (rdflib.Namespace): Base IRI namespace to use for mapping.
            submitted_on_date: The date the data was submitted.

        Returns:
            rdflib.Graph: Graph with row mapped into it.
        """
        # Get values from row
        provider_record_id: str = row["providerRecordID"]
        provider_record_id_source: str = row["providerRecordIDSource"]

        # Create URIs
        if identified_by := row["identifiedBy"]:
            provider_identified = utils.iri_patterns.agent_iri("person", identified_by)
        else:
            provider_identified = None
        sample_specimen = utils.iri_patterns.sample_iri(base_iri, "specimen", provider_record_id)
        sampling_specimen = utils.iri_patterns.sampling_iri(base_iri, "specimen", provider_record_id)
        sample_sequence = utils.iri_patterns.sample_iri(base_iri, "sequence", provider_record_id)
        sampling_sequencing = utils.iri_patterns.sampling_iri(base_iri, "sequencing", provider_record_id)
        if threat_status_determined_by := row["threatStatusDeterminedBy"]:
            provider_determined_by = utils.iri_patterns.agent_iri("person", threat_status_determined_by)
        else:
            provider_determined_by = None

        provider_record_id_datatype = utils.iri_patterns.datatype_iri("recordID", provider_record_id_source)
        provider_record_id_agent = utils.iri_patterns.agent_iri("org", provider_record_id_source)
        provider_record_id_attribution = utils.iri_patterns.attribution_iri(
            "resourceProvider", provider_record_id_source
        )
        provider_record_id_occurrence = utils.iri_patterns.occurrence_iri(base_iri, provider_record_id)
        provider_record_id_biodiversity_record = utils.iri_patterns.biodiversity_record_iri(
            base_iri, provider_record_id
        )

        # Create URIs for Observations and Observation Values
        observation_scientific_name = utils.iri_patterns.observation_iri(base_iri, "scientificName", provider_record_id)
        text_scientific_name = utils.iri_patterns.observation_value_iri(
            base_iri, "scientificName", row["scientificName"]
        )
        individual_count_observation = utils.iri_patterns.observation_iri(
            base_iri, "individualCount", provider_record_id
        )
        individual_count_value = utils.iri_patterns.observation_value_iri(
            base_iri, "individualCount", row["individualCount"]
        )
        organism_remarks_observation = utils.iri_patterns.observation_iri(
            base_iri, "organismRemarks", provider_record_id
        )
        organism_remarks_value = utils.iri_patterns.observation_value_iri(
            base_iri, "organismRemarks", row["organismRemarks"]
        )
        organism_quantity_observation = utils.iri_patterns.observation_iri(
            base_iri, "organismQuantity", provider_record_id
        )
        organism_quantity_value = utils.iri_patterns.observation_value_iri(
            base_iri, "organismQuantity", row["organismQuantity"]
        )
        occurrence_status_observation = utils.iri_patterns.observation_iri(
            base_iri, "occurrenceStatus", provider_record_id
        )
        occurrence_status_value = utils.iri_patterns.observation_value_iri(
            base_iri, "occurrenceStatus", row["occurrenceStatus"]
        )
        establishment_means_observation = utils.iri_patterns.observation_iri(
            base_iri, "establishmentMeans", provider_record_id
        )
        establishment_means_value = utils.iri_patterns.observation_value_iri(
            base_iri, "establishmentMeans", row["establishmentMeans"]
        )
        accepted_name_usage_observation = utils.iri_patterns.observation_iri(
            base_iri, "acceptedNameUsage", provider_record_id
        )
        accepted_name_usage_value = utils.iri_patterns.observation_value_iri(
            base_iri, "acceptedNameUsage", row["acceptedNameUsage"]
        )
        threat_status_observation = utils.iri_patterns.observation_iri(base_iri, "threatStatus", provider_record_id)
        threat_status_value = utils.iri_patterns.observation_value_iri(base_iri, "threatStatus", row["threatStatus"])

        # Create URIs for Observations+Values that depend on if there is a specimen.
        if has_specimen(row):
            _specimen_dependant_observation_iri = utils.iri_patterns.specimen_observation_iri
            _specimen_dependant_observation_value_iri = utils.iri_patterns.specimen_observation_value_iri
        else:
            _specimen_dependant_observation_iri = utils.iri_patterns.observation_iri
            _specimen_dependant_observation_value_iri = utils.iri_patterns.observation_value_iri
        observation_verbatim_id = _specimen_dependant_observation_iri(
            base_iri, "verbatimIdentification", provider_record_id
        )
        text_verbatim_id = _specimen_dependant_observation_value_iri(
            base_iri, "verbatimIdentification", row["verbatimIdentification"]
        )
        life_stage_observation = _specimen_dependant_observation_iri(base_iri, "lifeStage", provider_record_id)
        life_stage_value = _specimen_dependant_observation_value_iri(base_iri, "lifeStage", row["lifeStage"])
        sex_observation = _specimen_dependant_observation_iri(base_iri, "sex", provider_record_id)
        sex_value = _specimen_dependant_observation_value_iri(base_iri, "sex", row["sex"])
        reproductive_condition_observation = _specimen_dependant_observation_iri(
            base_iri, "reproductiveCondition", provider_record_id
        )
        reproductive_condition_value = _specimen_dependant_observation_value_iri(
            base_iri, "reproductiveCondition", row["reproductiveCondition"]
        )

        # Conditionally create uris dependent on ownerRecordIDSource field
        if owner_record_id_source := row["ownerRecordIDSource"]:
            owner_record_id_datatype = utils.iri_patterns.datatype_iri("recordID", owner_record_id_source)
            owner_record_id_provider = utils.iri_patterns.agent_iri("org", owner_record_id_source)
            owner_record_id_attribution = utils.iri_patterns.attribution_iri("owner", owner_record_id_source)
        else:
            owner_record_id_datatype = None
            owner_record_id_provider = None
            owner_record_id_attribution = None

        # Conditionally create uris dependant of dataGeneralizations field
        if data_generalizations := row["dataGeneralizations"]:
            data_generalizations_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "dataGeneralizations", data_generalizations
            )
            data_generalizations_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "dataGeneralizations", data_generalizations
            )
            data_generalizations_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "dataGeneralizations", data_generalizations
            )
        else:
            data_generalizations_attribute = None
            data_generalizations_value = None
            data_generalizations_collection = None

        # Conditionally create uris dependant of basisOfRecord field
        if basis_of_record := row["basisOfRecord"]:
            basis_attribute = utils.iri_patterns.attribute_iri(base_iri, "basisOfRecord", basis_of_record)
            basis_value = utils.iri_patterns.attribute_value_iri(base_iri, "basisOfRecord", basis_of_record)
            basis_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "basisOfRecord", basis_of_record
            )
        else:
            basis_attribute = None
            basis_value = None
            basis_collection = None

        # Conditionally create uri's dependent on recordedBy field.
        if recorded_by := row["recordedBy"]:
            record_number_datatype = utils.iri_patterns.datatype_iri("recordNumber", recorded_by)
            provider_recorded_by = utils.iri_patterns.agent_iri("person", recorded_by)
        else:
            record_number_datatype = None
            provider_recorded_by = None

        # Conditionally create uri's dependent on habitat field.
        if habitat := row["habitat"]:
            habitat_attribute = utils.iri_patterns.attribute_iri(base_iri, "habitat", habitat)
            habitat_value = utils.iri_patterns.attribute_value_iri(base_iri, "habitat", habitat)
            habitat_collection = utils.iri_patterns.attribute_collection_iri(base_iri, "Occurrence", "habitat", habitat)
        else:
            habitat_attribute = None
            habitat_value = None
            habitat_collection = None

        # Conditionally create uris dependent on catalogNumberSource field.
        if catalog_number_source := row["catalogNumberSource"]:
            catalog_number_datatype = utils.iri_patterns.datatype_iri("catalogNumber", catalog_number_source)
            catalog_number_provider = utils.iri_patterns.agent_iri("org", catalog_number_source)
        else:
            catalog_number_datatype = None
            catalog_number_provider = None

        # Conditionally create uris dependent on otherCatalogNumbersSource field.
        if other_catalog_numbers_source := row["otherCatalogNumbersSource"]:
            other_catalog_numbers_datatype = utils.iri_patterns.datatype_iri(
                "catalogNumber", other_catalog_numbers_source
            )
            other_catalog_numbers_provider = utils.iri_patterns.agent_iri("org", other_catalog_numbers_source)
        else:
            other_catalog_numbers_datatype = None
            other_catalog_numbers_provider = None

        # Conditionally create uris dependent on preparations field
        if preparations := row["preparations"]:
            preparations_attribute = utils.iri_patterns.attribute_iri(base_iri, "preparations", preparations)
            preparations_value = utils.iri_patterns.attribute_value_iri(base_iri, "preparations", preparations)
            preparations_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "preparations", preparations
            )
        else:
            preparations_attribute = None
            preparations_value = None
            preparations_collection = None

        # Conditionally create IRIs for the identificationQualifier field
        id_qualifier: str | None = row["identificationQualifier"]
        if id_qualifier:
            id_qualifier_attribute = utils.iri_patterns.attribute_iri(base_iri, "identificationQualifier", id_qualifier)
            id_qualifier_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "identificationQualifier", id_qualifier
            )
            id_qualifier_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "identificationQualifier", id_qualifier
            )
        else:
            id_qualifier_attribute = None
            id_qualifier_value = None
            id_qualifier_collection = None

        # Conditionally create IRIs for the identificationRemarks field
        id_remarks: str | None = row["identificationRemarks"]
        if id_remarks:
            id_remarks_attribute = utils.iri_patterns.attribute_iri(base_iri, "identificationRemarks", id_remarks)
            id_remarks_value = utils.iri_patterns.attribute_value_iri(base_iri, "identificationRemarks", id_remarks)
            id_remarks_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "identificationRemarks", id_remarks
            )
        else:
            id_remarks_attribute = None
            id_remarks_value = None
            id_remarks_collection = None

        # Conditionally create IRIs for the taxonRank field
        taxon_rank: str | None = row["taxonRank"]
        if taxon_rank:
            taxon_rank_attribute = utils.iri_patterns.attribute_iri(base_iri, "taxonRank", taxon_rank)
            taxon_rank_value = utils.iri_patterns.attribute_value_iri(base_iri, "taxonRank", taxon_rank)
            taxon_rank_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "taxonRank", taxon_rank
            )
        else:
            taxon_rank_attribute = None
            taxon_rank_value = None
            taxon_rank_collection = None

        # Conditionally create IRIs for the conservationAuthority field
        conservation_authority: str | None = row["conservationAuthority"]
        if conservation_authority:
            conservation_authority_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "conservationAuthority", conservation_authority
            )
            conservation_authority_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "conservationAuthority", conservation_authority
            )
            conservation_authority_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "conservationAuthority", conservation_authority
            )
        else:
            conservation_authority_attribute = None
            conservation_authority_value = None
            conservation_authority_collection = None

        # Conditionally create IRIs for the sensitivityCategory field
        sensitivity_category: str | None = row["sensitivityCategory"]
        if sensitivity_category:
            sensitivity_category_attribute = utils.iri_patterns.attribute_iri(
                base_iri, "sensitivityCategory", sensitivity_category
            )
            sensitivity_category_value = utils.iri_patterns.attribute_value_iri(
                base_iri, "sensitivityCategory", sensitivity_category
            )
            sensitivity_category_collection = utils.iri_patterns.attribute_collection_iri(
                base_iri, "Occurrence", "sensitivityCategory", sensitivity_category
            )
        else:
            sensitivity_category_attribute = None
            sensitivity_category_value = None
            sensitivity_category_collection = None

        # Add Provider Identified By
        self.add_provider_identified(
            uri=provider_identified,
            row=row,
            graph=graph,
        )

        # Add record number datatype
        self.add_record_number_datatype(
            uri=record_number_datatype,
            provider=provider_recorded_by,
            row=row,
            graph=graph,
        )

        # Add provider provider agent
        self.add_provider_recorded_by_agent(
            uri=provider_recorded_by,
            row=row,
            graph=graph,
        )

        # Add owner record id datatype
        self.add_record_id_datatype(
            uri=owner_record_id_datatype,
            attribution=owner_record_id_attribution,
            value=owner_record_id_source,
            graph=graph,
        )

        # Add attribution for record id datatype
        self.add_attribution(
            uri=owner_record_id_attribution,
            provider=owner_record_id_provider,
            provider_role_type=DATA_ROLE_OWNER,
            graph=graph,
        )

        # Add the provider owner record id
        self.add_owner_record_id_provider(
            uri=owner_record_id_provider,
            row=row,
            graph=graph,
        )

        # Add provider record ID datatype
        self.add_record_id_datatype(
            uri=provider_record_id_datatype,
            attribution=provider_record_id_attribution,
            value=provider_record_id_source,
            graph=graph,
        )

        # Add attribution for provider record id datatype
        self.add_attribution(
            uri=provider_record_id_attribution,
            provider=provider_record_id_agent,
            provider_role_type=DATA_ROLE_RESOURCE_PROVIDER,
            graph=graph,
        )

        # Add provider agent
        self.add_provider_record_id_agent(
            uri=provider_record_id_agent,
            row=row,
            graph=graph,
        )

        # Add Sample Specimen
        self.add_sample_specimen(
            uri=sample_specimen,
            row=row,
            dataset=dataset,
            sampling_specimen=sampling_specimen,
            provider_record_id_occurrence=provider_record_id_occurrence,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add catalog number datatype
        self.add_catalog_number_datatype(
            uri=catalog_number_datatype,
            provider=catalog_number_provider,
            value=catalog_number_source,
            graph=graph,
        )

        # Add catalog number provider
        self.add_catalog_number_provider(
            uri=catalog_number_provider,
            row=row,
            graph=graph,
        )

        # Add other catalog numbers datatype
        self.add_catalog_number_datatype(
            uri=other_catalog_numbers_datatype,
            provider=other_catalog_numbers_provider,
            value=other_catalog_numbers_source,
            graph=graph,
        )

        # Add other catalog numbers provider
        self.add_other_catalog_numbers_provider(
            uri=other_catalog_numbers_provider,
            row=row,
            graph=graph,
        )

        # Add Sampling Specimen
        self.add_sampling_specimen(
            uri=sampling_specimen,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            sample_specimen=sample_specimen,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Text for Scientific Name
        self.add_text_scientific_name(
            uri=text_scientific_name, dataset=dataset, row=row, graph=graph, submission_iri=submission_iri
        )

        # Add Identification Qualifier Attribute
        self.add_id_qualifier_attribute(
            uri=id_qualifier_attribute,
            id_qualifier=id_qualifier,
            id_qualifier_value=id_qualifier_value,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Identification Qualifier Value
        self.add_id_qualifier_value(
            uri=id_qualifier_value,
            id_qualifier=id_qualifier,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Identification Qualifier Collection
        self.add_id_qualifier_collection(
            uri=id_qualifier_collection,
            id_qualifier=id_qualifier,
            id_qualifier_attribute=id_qualifier_attribute,
            observation_scientific_name=observation_scientific_name,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Identification Remarks Attribute
        self.add_id_remarks_attribute(
            uri=id_remarks_attribute,
            id_remarks=id_remarks,
            id_remarks_value=id_remarks_value,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Identification Remarks Value
        self.add_id_remarks_value(
            uri=id_remarks_value,
            id_remarks=id_remarks,
            graph=graph,
        )

        # Add identification Remarks collection
        self.add_id_remarks_collection(
            uri=id_remarks_collection,
            id_remarks=id_remarks,
            id_remarks_attribute=id_remarks_attribute,
            observation_scientific_name=observation_scientific_name,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
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
            provider_record_id_occurrence=provider_record_id_occurrence,
            scientific_name=text_scientific_name,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add Observation for Verbatim ID
        self.add_observation_verbatim_id(
            uri=observation_verbatim_id,
            row=row,
            dataset=dataset,
            provider=provider_identified,
            provider_record_id_occurrence=provider_record_id_occurrence,
            sample_specimen=sample_specimen,
            verbatim_id=text_verbatim_id,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add Data Generalizations Attribute
        self.add_data_generalizations_attribute(
            uri=data_generalizations_attribute,
            data_generalizations=data_generalizations,
            dataset=dataset,
            data_generalizations_value=data_generalizations_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Data Generalizations Value
        self.add_data_generalizations_value(
            uri=data_generalizations_value,
            data_generalizations=data_generalizations,
            graph=graph,
        )

        # Add Data Generalizations Sample Collection
        self.add_data_generalizations_collection(
            uri=data_generalizations_collection,
            data_generalizations=data_generalizations,
            data_generalizations_attribute=data_generalizations_attribute,
            provider_record_id_occurrence=provider_record_id_occurrence,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Taxon Rank Attribute
        self.add_taxon_rank_attribute(
            uri=taxon_rank_attribute,
            taxon_rank=taxon_rank,
            dataset=dataset,
            taxon_rank_value=taxon_rank_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Taxon Rank Value
        self.add_taxon_rank_value(
            uri=taxon_rank_value,
            taxon_rank=taxon_rank,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Taxon Rank collection
        self.add_taxon_rank_collection(
            uri=taxon_rank_collection,
            taxon_rank=taxon_rank,
            taxon_rank_attribute=taxon_rank_attribute,
            observation_scientific_name=observation_scientific_name,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Individual Count Observation
        self.add_individual_count_observation(
            uri=individual_count_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            individual_count_value=individual_count_value,
            graph=graph,
            submission_iri=submission_iri,
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
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            organism_remarks_value=organism_remarks_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Organism Remarks Value
        self.add_organism_remarks_value(
            uri=organism_remarks_value,
            row=row,
            graph=graph,
        )

        # Add organism quantity observation
        self.add_organism_quantity_observation(
            uri=organism_quantity_observation,
            provider_record_id_occurrence=provider_record_id_occurrence,
            dataset=dataset,
            row=row,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add organism quantity value
        self.add_organism_quantity_value(
            uri=organism_quantity_value,
            organism_qty_observation=organism_quantity_observation,
            dataset=dataset,
            row=row,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Habitat Attribute
        self.add_habitat_attribute(
            uri=habitat_attribute,
            habitat=habitat,
            dataset=dataset,
            habitat_value=habitat_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Habitat Value
        self.add_habitat_value(
            uri=habitat_value,
            habitat=habitat,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add habitat attribute sample collection
        self.add_habitat_collection(
            uri=habitat_collection,
            habitat=habitat,
            habitat_attribute=habitat_attribute,
            provider_record_id_occurrence=provider_record_id_occurrence,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Basis of Record Attribute
        self.add_basis_attribute(
            uri=basis_attribute,
            basis_of_record=basis_of_record,
            dataset=dataset,
            basis_value=basis_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Basis of Record Value
        self.add_basis_value(
            uri=basis_value,
            basis_of_record=basis_of_record,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Basis of Record Sample Collection
        self.add_basis_collection(
            uri=basis_collection,
            basis_of_record=basis_of_record,
            basis_attribute=basis_attribute,
            sample_specimen=sample_specimen,
            provider_record_id_occurrence=provider_record_id_occurrence,
            row=row,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Owner Institution Provider
        self.add_owner_institution_provider(
            uri=owner_record_id_provider,
            row=row,
            graph=graph,
        )

        # Add Occurrence Status Observation
        self.add_occurrence_status_observation(
            uri=occurrence_status_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            occurrence_status_value=occurrence_status_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Occurrence Status Value
        self.add_occurrence_status_value(
            uri=occurrence_status_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Preparations Attribute
        self.add_preparations_attribute(
            uri=preparations_attribute,
            preparations=preparations,
            dataset=dataset,
            preparations_value=preparations_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Preparations Value
        self.add_preparations_value(
            uri=preparations_value,
            preparations=preparations,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Preparations attribute Sample Collection
        self.add_preparations_collection(
            uri=preparations_collection,
            preparations=preparations,
            preparations_attribute=preparations_attribute,
            sample_specimen=sample_specimen,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Establishment Means Observation
        self.add_establishment_means_observation(
            uri=establishment_means_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            establishment_means_value=establishment_means_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Establishment Means Value
        self.add_establishment_means_value(
            uri=establishment_means_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Life Stage Observation
        self.add_life_stage_observation(
            uri=life_stage_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            sample_specimen=sample_specimen,
            life_stage_value=life_stage_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Life Stage Value
        self.add_life_stage_value(
            uri=life_stage_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Sex Observation
        self.add_sex_observation(
            uri=sex_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            sample_specimen=sample_specimen,
            sex_value=sex_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Sex Value
        self.add_sex_value(
            uri=sex_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Reproductive Condition Observation
        self.add_reproductive_condition_observation(
            uri=reproductive_condition_observation,
            row=row,
            dataset=dataset,
            provider_record_id_occurrence=provider_record_id_occurrence,
            sample_specimen=sample_specimen,
            reproductive_condition_value=reproductive_condition_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Reproductive Condition Value
        self.add_reproductive_condition_value(
            uri=reproductive_condition_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Accepted Name Usage Observation
        self.add_accepted_name_usage_observation(
            uri=accepted_name_usage_observation,
            row=row,
            dataset=dataset,
            scientific_name=text_scientific_name,
            accepted_name_usage_value=accepted_name_usage_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Accepted Name Usage Value
        self.add_accepted_name_usage_value(
            uri=accepted_name_usage_value, dataset=dataset, row=row, graph=graph, submission_iri=submission_iri
        )

        # Add Sampling Sequencing
        self.add_sampling_sequencing(
            uri=sampling_sequencing,
            row=row,
            dataset=dataset,
            feature_of_interest=sample_specimen,
            sample_sequence=sample_sequence,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add Sample Sequence
        self.add_sample_sequence(
            uri=sample_sequence,
            row=row,
            dataset=dataset,
            feature_of_interest=sample_specimen,
            sampling_sequencing=sampling_sequencing,
            graph=graph,
            submission_iri=submission_iri,
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
            provider_record_id_occurrence=provider_record_id_occurrence,
            threat_status_value=threat_status_value,
            determined_by=provider_determined_by,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add Threat Status Value
        self.add_threat_status_value(
            uri=threat_status_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Conservation Authority Attribute
        self.add_conservation_authority_attribute(
            uri=conservation_authority_attribute,
            conservation_authority=conservation_authority,
            conservation_authority_value=conservation_authority_value,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Conservation Authority Value
        self.add_conservation_authority_value(
            uri=conservation_authority_value,
            conservation_authority=conservation_authority,
            graph=graph,
        )

        # Add conservation Authority Collection
        self.add_conservation_authority_collection(
            uri=conservation_authority_collection,
            conservation_authority=conservation_authority,
            conservation_authority_attribute=conservation_authority_attribute,
            threat_status_observation=threat_status_observation,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Sensitivity Category Attribute
        self.add_sensitivity_category_attribute(
            uri=sensitivity_category_attribute,
            row=row,
            dataset=dataset,
            sensitivity_category_value=sensitivity_category_value,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add Sensitivity Category Value
        self.add_sensitivity_category_value(
            uri=sensitivity_category_value,
            row=row,
            dataset=dataset,
            graph=graph,
            submitted_on_date=submitted_on_date,
        )

        # Add Sensitivity Category Collection
        self.add_sensitivity_category_collection(
            uri=sensitivity_category_collection,
            sensitivity_category=sensitivity_category,
            sensitivity_category_attribute=sensitivity_category_attribute,
            provider_record_id_biodiversity_record=provider_record_id_biodiversity_record,
            dataset=dataset,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add biodiversity record
        self.add_biodiversity_record(
            uri=provider_record_id_biodiversity_record,
            provider_record_id_datatype=provider_record_id_datatype,
            provider_record_id_occurrence=provider_record_id_occurrence,
            dataset=dataset,
            row=row,
            graph=graph,
            submission_iri=submission_iri,
        )

        # Add occurrence
        self.add_occurrence(
            uri=provider_record_id_occurrence,
            record_number_datatype=record_number_datatype,
            owner_record_id_datatype=owner_record_id_datatype,
            other_catalog_numbers_datatype=other_catalog_numbers_datatype,
            catalog_number_datatype=catalog_number_datatype,
            provider_recorded_by=provider_recorded_by,
            dataset=dataset,
            row=row,
            graph=graph,
            submission_iri=submission_iri,
            submitted_on_date=submitted_on_date,
        )

        # Add extra fields JSON
        self.add_extra_fields_json(
            subject_uri=provider_record_id_occurrence,
            row=row,
            graph=graph,
            extra_schema=extra_schema,
        )

    def add_provider_identified(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identified By Provider to the Graph

        Args:
            uri: URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check for identifiedBy
        if not uri:
            return

        # Add to Graph
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["identifiedBy"])))

    def add_observation_scientific_name(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider: rdflib.URIRef | None,
        provider_record_id_occurrence: rdflib.URIRef,
        scientific_name: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Observation Scientific Name to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider: Provider associated with this node
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            scientific_name (rdflib.URIRef): Scientific Name associated with
                this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
            submitted_on_date: The date the data was submitted.
        """
        # Get Timestamp
        date_identified: models.temporal.Timestamp = row["dateIdentified"] or row["eventDateStart"]

        # Retrieve vocab for field
        vocab = self.fields()["identificationMethod"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["identificationMethod"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("scientificName-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, scientific_name))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["scientificName"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, date_identified.rdf_in_xsd, date_identified.to_rdf_literal()))
        graph.add((uri, rdflib.SOSA.usedProcedure, term))

        # Check for identifiedBy
        if provider:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Add comment to temporal entity
            comment = "Date unknown, template eventDateStart used as proxy"
            graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(comment)))

    def add_observation_verbatim_id(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider: rdflib.URIRef | None,
        provider_record_id_occurrence: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        verbatim_id: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Observation Verbatim ID to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider: Provider associated with this node
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            verbatim_id (rdflib.URIRef): Verbatim ID associated with this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rflib.URIRef): submission IRI
            submitted_on_date: The date the data was submitted.
        """
        # Check for verbatimIdentification
        if not row["verbatimIdentification"]:
            return

        # Get Timestamp
        date_identified: models.temporal.Timestamp = row["dateIdentified"] or row["eventDateStart"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else provider_record_id_occurrence

        # Retrieve vocab for field
        vocab = self.fields()["identificationMethod"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["identificationMethod"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("verbatimID-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, verbatim_id))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["verbatimIdentification"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, date_identified.rdf_in_xsd, date_identified.to_rdf_literal()))
        graph.add((uri, rdflib.SOSA.usedProcedure, term))

        # Check for identifiedBy
        if provider:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider))

        # Check for dateIdentified
        if not row["dateIdentified"]:
            # Add comment to temporal entity
            comment = "Date unknown, template eventDateStart used as proxy"
            graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(comment)))

    def add_provider_recorded_by_agent(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the provider agent to the graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Ensure data and URI passed in
        if uri is None or not row["recordedBy"]:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["recordedBy"])))

    def add_record_id_datatype(
        self,
        uri: rdflib.URIRef | None,
        attribution: rdflib.URIRef | None,
        value: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the owner record id datatype to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node or None.
            attribution (rdflib.URIRef | None): Attribution of the recordID datatype or None.
            value (str | None): Raw value provided for the record id source.
            graph (rdflid.Graph): Graph to be modified.
        """
        # Check to see subject provided.
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        if value is not None:
            graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{value} recordID")))

        # Add definition
        graph.add((uri, rdflib.SKOS.definition, rdflib.Literal("An identifier for the record")))

        # Add attribution
        if attribution is not None:
            graph.add((uri, rdflib.PROV.qualifiedAttribution, attribution))

    def add_attribution(
        self,
        uri: rdflib.URIRef | None,
        provider: rdflib.URIRef | None,
        provider_role_type: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds an attribution node to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node or None.
            provider (rdflib.URIRef | None): Provider of the datatype or None.
            provider_role_type (rdflib.URIRef): Role type of provider.
            graph (rdflid.Graph): Graph to be modified.
        """
        # Check to see subject provided.
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Attribution))

        if provider is not None:
            graph.add((uri, rdflib.PROV.agent, provider))

        graph.add((uri, rdflib.PROV.hadRole, provider_role_type))

    def add_owner_record_id_provider(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the provider owner record id node.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.:
        """
        # Check that a subject uri was supplied
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["ownerRecordIDSource"])))

    def add_provider_record_id_agent(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds provider record id agent to the graph.

        Args:
            uri (rdflib.URIRef): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["providerRecordIDSource"])))

    def add_id_qualifier_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_qualifier: str | None,
        id_qualifier_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Identification Qualifier Attribute to the Graph

        Args:
            uri: URI to use for this node.
            id_qualifier: identificationQualifier value from the template
            id_qualifier_value: Identification Qualifier Value associated with this node.
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submission_iri (rflib.Graph): Submission IRI
        """
        # Check identificationQualifier
        if uri is None:
            return

        # Identification Qualifier Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_ID_UNCERTAINTY))
        if id_qualifier:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(id_qualifier)))
        if id_qualifier_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, id_qualifier_value))

    def add_id_qualifier_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_qualifier: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Identification Qualifier Value to the Graph

        Args:
            uri: URI to use for this node.
            id_qualifier: identificationQualifier value from the template
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check node should be created
        if uri is None:
            return

        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if id_qualifier:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(id_qualifier)))

            # Retrieve vocab for field
            vocab = self.fields()["identificationQualifier"].get_flexible_vocab()
            # Retrieve term or Create on the Fly
            term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(id_qualifier)
            # Identification Qualifier Value
            graph.add((uri, rdflib.RDF.value, term))

    def add_id_qualifier_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_qualifier: str | None,
        id_qualifier_attribute: rdflib.URIRef | None,
        observation_scientific_name: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a identification qualifier Collection to the graph

        Args:
            uri: The uri for the Collection.
            id_qualifier: identificationQualifier value from template.
            id_qualifier_attribute: The uri for the attribute node.
            observation_scientific_name: The node that should be a member of the collection.
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
        if id_qualifier:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Identification Qualifier - {id_qualifier}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the scientific name observation node
        graph.add((uri, rdflib.SDO.member, observation_scientific_name))
        # Add link to attribute
        if id_qualifier_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, id_qualifier_attribute))

    def add_id_remarks_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_remarks: str | None,
        id_remarks_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Identification Remarks Attribute to the Graph

        Args:
            uri: URI to use for this node.
            id_remarks: identificationRemarks value from the template
            id_remarks_value: Identification Remarks Value associated with this node
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check identificationRemarks
        if uri is None:
            return

        # Identification Remarks Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_ID_REMARKS))
        if id_remarks:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(id_remarks)))
        if id_remarks_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, id_remarks_value))

    def add_id_remarks_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_remarks: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Identification Remarks Value to the Graph

        Args:
            uri: URI to use for this node
            id_remarks: identificationRemarks value from the template
            graph (rdflib.Graph): Graph to add to
        """
        # Check identificationRemarks
        if uri is None:
            return

        # Identification Remarks Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(id_remarks)))

    def add_id_remarks_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        id_remarks: str | None,
        id_remarks_attribute: rdflib.URIRef | None,
        observation_scientific_name: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a identification remarks Collection to the graph

        Args:
            uri: The uri for the Collection.
            id_remarks: identificationRemarks value from template
            id_remarks_attribute: The uri for the attribute node.
            observation_scientific_name: The node that should be a member of the collection.
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
        if id_remarks:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Identification Remarks - {id_remarks}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the scientific name observation node
        graph.add((uri, rdflib.SDO.member, observation_scientific_name))
        # Add link to attribute
        if id_remarks_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, id_remarks_attribute))

    def add_text_scientific_name(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Text Scientific Name to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset this belongs to
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("scientificName")))
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(row["scientificName"])))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_SCIENTIFIC_NAME))

    def add_catalog_number_datatype(
        self,
        uri: rdflib.URIRef | None,
        provider: rdflib.URIRef | None,
        value: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds catalog number datatype to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            provider (rdflib.URIRef | None): Corresponding provider.
            value (str | None): Catalog number source name obtained from raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject was provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        if value is not None:
            graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{value} catalogNumber")))

        # Add definition
        graph.add((uri, rdflib.SKOS.definition, rdflib.Literal("A catalog number for the sample")))

        # Add attribution
        if provider is not None:
            graph.add((uri, rdflib.PROV.wasAttributedTo, provider))

    def add_catalog_number_provider(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the catalog number provider to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject was provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["catalogNumberSource"])))

    def add_other_catalog_numbers_provider(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds other catalog numbers provider to the graph.

        Args:
            uri (rdflib.URIRef | None): Subject of the node.
            row (frictionless.Row): Raw data.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check that subject was provided
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.PROV.Agent))

        # Add name
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["otherCatalogNumbersSource"])))

    def add_sampling_specimen(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Sampling Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            sample_specimen (rdflib.URIRef): Sample Specimen associated with
                this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check if Row has a Specimen
        if not has_specimen(row):
            return

        # Create geometry
        geometry = models.spatial.Geometry(
            raw=models.spatial.LatLong(row["decimalLatitude"], row["decimalLongitude"]),
            datum=row["geodeticDatum"],
        )

        # Get Timestamp
        timestamp: models.temporal.Timestamp = row["preparedDate"] or row["eventDateStart"]

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sampling")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, sample_specimen))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_PROCEDURE_SAMPLING))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, timestamp.rdf_in_xsd, timestamp.to_rdf_literal()))

        # Add geometry
        geometry_node = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))
        spatial_comment = "Location unknown, location of field sampling used as proxy"
        graph.add((geometry_node, rdflib.RDFS.comment, rdflib.Literal(spatial_comment)))

        # Add 'supplied as' geometry
        self.add_geometry_supplied_as(
            subj=uri,
            pred=utils.namespaces.GEO.hasGeometry,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
        )

        # Check for preparedDate
        if not row["preparedDate"]:
            # Add comment to temporal entity
            temporal_comment = "Date unknown, template eventDateStart used as proxy"
            graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

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

    def add_record_number_datatype(
        self,
        uri: rdflib.URIRef | None,
        provider: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds record number datatype to the graph.

        Args:
            uri (rdflib.URIRef | None): The subject of the node
                or None if uri wasn't created.
            provider (rdflib.URIRef | None): The corresponding
                provider uri.
            row (frictionless.Row): Row from the template.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Check subject provided
        if uri is None:
            return

        # if no recordNumber, don't create this datatype because it would be unused.
        if not row["recordNumber"]:
            return

        # Add type
        graph.add((uri, a, rdflib.RDFS.Datatype))

        # Add label
        if recorded_by := row["recordedBy"]:
            graph.add((uri, rdflib.SKOS.prefLabel, rdflib.Literal(f"{recorded_by} recordNumber")))

        # Add definition
        graph.add(
            (
                uri,
                rdflib.SKOS.definition,
                rdflib.Literal(
                    "The record number of the original observation from the original observer of the organism"
                ),
            ),
        )

        # Add attribution
        if provider is not None:
            graph.add((uri, rdflib.PROV.wasAttributedTo, provider))

    def add_sample_specimen(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sampling_specimen: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Sample Specimen to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            sampling_specimen (rdflib.URIRef): Sampling Specimen associated
                with this node
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
            submitted_on_date: The date the data was submitted.
        """
        # Check if Row has a Specimen
        if not has_specimen(row):
            return

        # Retrieve vocab for field
        vocab = self.fields()["kingdom"].get_flexible_vocab("KINGDOM_SPECIMEN")

        # Retrieve Vocab or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["kingdom"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        graph.add((uri, a, utils.namespaces.TERN.Sample))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("specimen-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_specimen))
        graph.add((uri, rdflib.SOSA.isSampleOf, provider_record_id_occurrence))
        graph.add((uri, utils.namespaces.TERN.featureType, term))

    def add_data_generalizations_attribute(
        self,
        uri: rdflib.URIRef | None,
        data_generalizations: str | None,
        dataset: rdflib.URIRef,
        data_generalizations_value: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Data Generalizations Attribute to the Graph

        Args:
            uri: URI to use for this node.
            data_generalizations: dataGeneralizations value from the CSV
            dataset: Dataset this belongs to
            data_generalizations_value: Data Generalizations Value associated with this node
            graph: Graph to add to
            submission_iri: Submission IRI
        """
        # Check Existence
        if uri is None:
            return

        # Data Generalizations Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_DATA_GENERALIZATIONS))
        if data_generalizations:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(data_generalizations)))
        if data_generalizations_value is not None:
            graph.add((uri, utils.namespaces.TERN.hasValue, data_generalizations_value))

    def add_data_generalizations_value(
        self,
        uri: rdflib.URIRef | None,
        data_generalizations: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Data Generalizations Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            data_generalizations: dataGeneralizations value from the CSV
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        # Data Generalizations Value
        graph.add((uri, a, utils.namespaces.TERN.Text))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(data_generalizations)))

    def add_data_generalizations_collection(
        self,
        uri: rdflib.URIRef | None,
        data_generalizations: str | None,
        data_generalizations_attribute: rdflib.URIRef | None,
        provider_record_id_occurrence: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a data generalizations attribute Sample Collection to the graph

        Args:
            uri: The uri for the SampleCollection.
            data_generalizations: dataGeneralizations value from template.
            data_generalizations_attribute: The uri for the attribute node.
            provider_record_id_occurrence: Occurrence associated with this
                node
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
        if data_generalizations:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(
                        f"Occurrence Collection - Data Generalizations - {data_generalizations}",
                    ),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the sample field
        graph.add((uri, rdflib.SDO.member, provider_record_id_occurrence))
        # Add link to attribute
        if data_generalizations_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, data_generalizations_attribute))

    def add_taxon_rank_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        taxon_rank: str | None,
        taxon_rank_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Taxon Rank Attribute to the Graph

        Args:
            uri: URI to use for this node.
            taxon_rank: taxonRank value from the template.
            taxon_rank_value: Taxon Rank Value associated with this node
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check Existence
        if uri is None:
            return

        # Taxon Rank Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_TAXON_RANK))
        if taxon_rank:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(taxon_rank)))
        if taxon_rank_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, taxon_rank_value))

    def add_taxon_rank_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        taxon_rank: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Taxon Rank Value to the Graph

        Args:
            uri: URI to use for this node
            taxon_rank: taxonRank value from the template.
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if uri is None:
            return

        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if taxon_rank:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(taxon_rank)))

            # Retrieve vocab for field
            vocab = self.fields()["taxonRank"].get_flexible_vocab()
            # Retrieve term or Create on the Fly
            term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(taxon_rank)
            # Taxon Rank Value
            graph.add((uri, rdflib.RDF.value, term))

    def add_taxon_rank_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        taxon_rank: str | None,
        taxon_rank_attribute: rdflib.URIRef | None,
        observation_scientific_name: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a taxon rank Collection to the graph

        Args:
            uri: The uri for the Collection.
            taxon_rank: taxonRank value from template.
            taxon_rank_attribute: The uri for the attribute node.
            observation_scientific_name: The node that should be a member of the collection.
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
        if taxon_rank:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Taxon Rank - {taxon_rank}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the scientific name observation node
        graph.add((uri, rdflib.SDO.member, observation_scientific_name))
        # Add link to attribute
        if taxon_rank_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, taxon_rank_attribute))

    def add_individual_count_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        individual_count_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Individual Count Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            individual_count_value (rdflib.URIRef): Individual Count Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check Existence
        if not row["individualCount"]:
            return

        # Get Timestamp
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Individual Count Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("individualCount-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, individual_count_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["individualCount"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_INDIVIDUAL_COUNT))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add Method Qualifier comment
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

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
        provider_record_id_occurrence: rdflib.URIRef,
        organism_remarks_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Organism Remarks Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            organism_remarks_value (rdflib.URIRef): Organism Remarks Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check Existence
        if not row["organismRemarks"]:
            return

        # Get Timestamp
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Organism Remarks Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("organismRemarks-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, organism_remarks_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["organismRemarks"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_ORGANISM_REMARKS))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

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

    def add_organism_quantity_observation(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds observation organism quantity to the graph.

        Args:
            uri: URI to use for this node.
            dataset: Dataset which data belongs.
            provider_record_id_occurrence: Occurrence associated with this node
            row: Row to retrieve data from.
            graph: Graph to be modified.
            submission_iri: URI for submission
        """
        # Extract values
        event_date: models.temporal.Timestamp = row["eventDateStart"]
        organism_qty: decimal.Decimal | None = row["organismQuantity"]
        organism_qty_type: str | None = row["organismQuantityType"]

        # Check if organism quantity values were provided
        if organism_qty is None or not organism_qty_type:
            return

        # Attach node to sample field and dataset
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("organismQuantity-observation")))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_ORGANISM_QUANTITY))

        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))
        # Add comment to temporal entity
        graph.add(
            (
                temporal_entity,
                rdflib.RDFS.comment,
                rdflib.Literal("Date unknown, template eventDateStart used as proxy"),
            )
        )

        # Add Human observation as proxy for observation method
        human_observation = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157")
        graph.add((uri, rdflib.SOSA.usedProcedure, human_observation))

        # Add organism quantity and type values
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(f"{organism_qty} {organism_qty_type}")))

        # Add method comment to node
        graph.add(
            (
                uri,
                rdflib.RDFS.comment,
                rdflib.Literal("Observation method unknown, 'human observation' used as proxy"),
            )
        )

    def add_organism_quantity_value(
        self,
        uri: rdflib.URIRef,
        organism_qty_observation: rdflib.URIRef,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds organism quantity value to graph.

        Args:
            uri: URI to use for this node.
            organism_qty_observation: Observation URI.
            dataset: Dataset this is a part of.
            row: Row to retrieve data from.
            graph: Graph to be modified.
            submitted_on_date: The date the data was submitted.
        """
        # Extract values if any
        organism_qty: decimal.Decimal | None = row["organismQuantity"]
        organism_qty_type: str | None = row["organismQuantityType"]

        # Check for values
        if organism_qty is None or not organism_qty_type:
            return

        # Retrieve vocab for field
        vocab = self.fields()["organismQuantityType"].get_flexible_vocab()

        # Get term or create on the fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(organism_qty_type)

        # Add to graph
        graph.add((organism_qty_observation, rdflib.SOSA.hasResult, uri))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, a, utils.namespaces.TERN.Float))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("organism-quantity")))
        graph.add((uri, utils.namespaces.TERN.unit, term))
        graph.add((uri, rdflib.RDF.value, rdflib.Literal(organism_qty, datatype=rdflib.XSD.float)))

    def add_habitat_attribute(
        self,
        uri: rdflib.URIRef | None,
        habitat: str | None,
        dataset: rdflib.URIRef,
        habitat_value: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Habitat Attribute to the Graph

        Args:
            uri: URI to use for this node.
            habitat: Raw habitat from CSV.
            dataset: Dataset this belongs to
            habitat_value: Habitat Value associated with this node
            graph: Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        # Habitat Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_HABITAT))
        if habitat:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(habitat)))
        if habitat_value is not None:
            graph.add((uri, utils.namespaces.TERN.hasValue, habitat_value))

    def add_habitat_value(
        self,
        uri: rdflib.URIRef | None,
        habitat: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Habitat Value to the Graph

        Args:
            uri: URI to use for this node
            habitat: Habitat from the CSV
            dataset: Dataset this belongs to
            graph: Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if uri is None:
            return

        # Habitat Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        if habitat:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(habitat)))

            # Retrieve vocab for field
            vocab = self.fields()["habitat"].get_flexible_vocab()
            # Retrieve term or Create on the Fly
            term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(habitat)
            # Add value
            graph.add((uri, rdflib.RDF.value, term))

    def add_habitat_collection(
        self,
        uri: rdflib.URIRef | None,
        habitat: str | None,
        habitat_attribute: rdflib.URIRef | None,
        provider_record_id_occurrence: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a habitat attribute Sample Collection to the graph

        Args:
            uri: The uri for the SampleCollection.
            habitat: Habitat value from template.
            habitat_attribute: The uri for the attribute node.
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
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
        if habitat:
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(f"Occurrence Collection - Habitat - {habitat}")))
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the sample field
        graph.add((uri, rdflib.SDO.member, provider_record_id_occurrence))
        # Add link to attribute
        if habitat_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, habitat_attribute))

    def add_basis_attribute(
        self,
        uri: rdflib.URIRef | None,
        basis_of_record: str | None,
        dataset: rdflib.URIRef,
        basis_value: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Basis of Record Attribute to the Graph

        Args:
            uri: URI to use for this node.
            basis_of_record: basisOfRecord value from the CSV
            dataset: Dataset this belongs to
            basis_value: Basis of Record Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        # Basis of Record Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_BASIS_OF_RECORD))
        if basis_of_record:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(basis_of_record)))
        if basis_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, basis_value))

    def add_basis_value(
        self,
        uri: rdflib.URIRef | None,
        basis_of_record: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Basis of Record Value to the Graph

        Args:
            uri: URI to use for this node
            basis_of_record: basisOfRecord value from the CSV
            dataset: Dataset this belongs to
            graph: Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if uri is None:
            return

        # Basis of Record Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        if basis_of_record:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(basis_of_record)))

            # Retrieve vocab for field
            vocab = self.fields()["basisOfRecord"].get_flexible_vocab()
            # Retrieve term or Create on the Fly
            term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(basis_of_record)
            # Add value
            graph.add((uri, rdflib.RDF.value, term))

    def add_basis_collection(
        self,
        uri: rdflib.URIRef | None,
        basis_of_record: str | None,
        basis_attribute: rdflib.URIRef | None,
        sample_specimen: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a basisOfRecord attribute Sample Collection to the graph

        Either the sample_specimen node or the sample_field node should be a member
        of this collection, depending on if the row has a specimen.

        Args:
            uri: The uri for the SampleCollection.
            basis_of_record: basisOfRecord value from template.
            basis_attribute: The uri for the attribute node.
            sample_specimen: The sample specimen node.
            provider_record_id_occurrence: Occurrence associated with this
                node
            row: The CSV row.
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
        if basis_of_record:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Basis Of Record - {basis_of_record}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the appropriate sample node
        if has_specimen(row):
            graph.add((uri, rdflib.SDO.member, sample_specimen))
        else:
            graph.add((uri, rdflib.SDO.member, provider_record_id_occurrence))
        # Add link to attribute
        if basis_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, basis_attribute))

    def add_owner_institution_provider(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Owner Institution Provider to the Graph

        Args:
            uri (rdflib.URIRef | None): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # TODO -> Retrieve this from a known list of institutions
        # Check Existence
        if not row["ownerRecordIDSource"] or uri is None:
            return

        # Owner Institution Provider
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["ownerRecordIDSource"])))

    def add_occurrence_status_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        occurrence_status_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Occurrence Status Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            occurrence_status_value (rdflib.URIRef): Occurrence Status Value
                associated with this node
            graph (rdflib.Graph): Graph to add to
            submission_iri (rdflib.URIRef): Submission IRI
        """
        # Check Existence
        if not row["occurrenceStatus"]:
            return

        # Get Timestamp
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Occurrence Status Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("occurrenceStatus-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, occurrence_status_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["occurrenceStatus"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_OCCURRENCE_STATUS))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_occurrence_status_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Occurrence Status Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["occurrenceStatus"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["occurrenceStatus"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["occurrenceStatus"])

        # Occurrence Status Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"occurrenceStatus = {row['occurrenceStatus']}")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_preparations_attribute(
        self,
        uri: rdflib.URIRef | None,
        preparations: str | None,
        dataset: rdflib.URIRef,
        preparations_value: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Preparations Attribute to the Graph

        Args:
            uri: URI to use for this node.
            preparations: preparations value from the CSV
            dataset: Dataset this belongs to
            preparations_value: Preparations Value associated with this node
            graph: Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        # Preparations Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_PREPARATIONS))
        if preparations:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(preparations)))
        if preparations_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, preparations_value))

    def add_preparations_value(
        self,
        uri: rdflib.URIRef | None,
        preparations: str | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Preparations Value to the Graph

        Args:
            uri: URI to use for this node
            preparations: preparations value from the CSV
            dataset: Dataset this belongs to
            graph: Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if uri is None:
            return

        # Preparations Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        if preparations:
            # Add label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(preparations)))

            # Retrieve vocab for field
            vocab = self.fields()["preparations"].get_flexible_vocab()
            # Retrieve term or Create on the Fly
            term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(preparations)
            # Add value
            graph.add((uri, rdflib.RDF.value, term))

    def add_preparations_collection(
        self,
        uri: rdflib.URIRef | None,
        preparations: str | None,
        preparations_attribute: rdflib.URIRef | None,
        sample_specimen: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a preparations attribute Sample Collection to the graph

        Args:
            uri: The uri for the SampleCollection.
            preparations: preparations value from template.
            preparations_attribute: The uri for the attribute node.
            sample_specimen: The sample specimen node that should be a member of the collection.
            dataset: The uri for the dateset node.
            graph: The graph
            submission_iri: The submission IRI
        """
        if uri is None:
            return

        # Add type
        graph.add((uri, a, rdflib.SDO.Collection))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add identifier
        if preparations:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Preparations - {preparations}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the sample_specimen node
        graph.add((uri, rdflib.SDO.member, sample_specimen))
        # Add link to attribute
        if preparations_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, preparations_attribute))

    def add_establishment_means_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        establishment_means_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Establishment Means Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
                node
            establishment_means_value (rdflib.URIRef): Establishment Means
                Value associated with this node
            graph (rdflib.Graph): Graph to add to
        """
        # Check Existence
        if not row["establishmentMeans"]:
            return

        # Get Timestamp
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Establishment Means Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("establishmentMeans-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, establishment_means_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["establishmentMeans"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_ESTABLISHMENT_MEANS))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_establishment_means_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Establishment Means Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["establishmentMeans"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["establishmentMeans"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["establishmentMeans"])

        # Establishment Means Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("establishmentMeans-value")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_life_stage_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        life_stage_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Life Stage Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
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
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else provider_record_id_occurrence

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Life Stage Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("lifeStage-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, life_stage_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["lifeStage"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_LIFE_STAGE))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_life_stage_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Life Stage Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["lifeStage"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["lifeStage"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["lifeStage"])

        # Life Stage Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("lifeStage-value")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_sex_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        sex_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Sex Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
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
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else provider_record_id_occurrence

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Sex Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sex-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, sex_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["sex"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_SEX))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_sex_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Sex Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["sex"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["sex"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["sex"])

        # Sex Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("sex-value")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_reproductive_condition_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        sample_specimen: rdflib.URIRef,
        reproductive_condition_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Reproductive Condition Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this
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
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Choose Feature of Interest
        # The Feature of Interest is the Specimen Sample if it is determined
        # that this row has a specimen, otherwise it is Field Sample
        foi = sample_specimen if has_specimen(row) else provider_record_id_occurrence

        # Retrieve Vocab or Create on the Fly
        vocab = vocabs.sampling_protocol.HUMAN_OBSERVATION.iri  # Always Human Observation

        # Reproductive Condition Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("reproductiveCondition-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, foi))
        graph.add((uri, rdflib.SOSA.hasResult, reproductive_condition_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["reproductiveCondition"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_REPRODUCTIVE_CONDITION))
        graph.add((uri, rdflib.SOSA.usedProcedure, vocab))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add method comment to node
        method_comment = "Observation method unknown, 'human observation' used as proxy"
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal(method_comment)))

    def add_reproductive_condition_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Reproductive Condition Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["reproductiveCondition"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["reproductiveCondition"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["reproductiveCondition"])

        # Reproductive Condition Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("reproductiveCondition-value")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_accepted_name_usage_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        scientific_name: rdflib.URIRef,
        accepted_name_usage_value: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
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

        # Get Timestamp
        date_identified: models.temporal.Timestamp = row["dateIdentified"] or row["eventDateStart"]

        # Accepted Name Usage Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("acceptedNameUsage-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, scientific_name))
        graph.add((uri, rdflib.SOSA.hasResult, accepted_name_usage_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["acceptedNameUsage"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_TAXON))
        graph.add((uri, rdflib.SOSA.usedProcedure, CONCEPT_NAME_CHECK_METHOD))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, date_identified.rdf_in_xsd, date_identified.to_rdf_literal()))

        # Add comment to temporal entity
        # Determine which field was used
        timestamp_used = "dateIdentified" if row["dateIdentified"] else "eventDateStart"
        temporal_comment = f"Date unknown, template {timestamp_used} used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

    def add_accepted_name_usage_value(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Accepted Name Usage Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            dataset (rdflib.URIRef): Dataset this belongs to
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal("acceptedNameUsage-value")))
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
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
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Sampling Sequencing to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            feature_of_interest (rdflib.URIRef): Feature of Interest associated
                with this node
            sample_sequence (rdflib.URIRef): Sample Sequence associated with
                this node
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Extract values from row
        event_date: models.temporal.Timestamp = row["eventDateStart"]

        # Check Existence
        if not row["associatedSequences"]:
            return

        # Create geometry
        geometry = models.spatial.Geometry(
            raw=models.spatial.LatLong(row["decimalLatitude"], row["decimalLongitude"]),
            datum=row["geodeticDatum"],
        )

        # Retrieve vocab for field
        vocab = self.fields()["sequencingMethod"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(row["sequencingMethod"])

        # Add to Graph
        graph.add((uri, a, utils.namespaces.TERN.Sampling))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sequencing-sampling")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, feature_of_interest))
        graph.add((uri, rdflib.SOSA.hasResult, sample_sequence))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, event_date.rdf_in_xsd, event_date.to_rdf_literal()))
        graph.add((uri, rdflib.SOSA.usedProcedure, term))

        # Add geometry
        geometry_node = rdflib.BNode()
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))

        # Add 'supplied as' geometry
        self.add_geometry_supplied_as(
            subj=uri,
            pred=utils.namespaces.GEO.hasGeometry,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
        )

        # Check for coordinateUncertaintyInMeters
        if row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(row["coordinateUncertaintyInMeters"], datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Add comment to temporal entity
        temporal_comment = "Date unknown, template eventDateStart used as proxy"
        graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(temporal_comment)))

        # Add comment to geometry
        spatial_comment = "Location unknown, location of field sampling used as proxy"
        graph.add((geometry_node, rdflib.RDFS.comment, rdflib.Literal(spatial_comment)))

    def add_sample_sequence(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        feature_of_interest: rdflib.URIRef,
        sampling_sequencing: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
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
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("sequence-sample")))
        graph.add((uri, rdflib.SOSA.isResultOf, sampling_sequencing))
        graph.add((uri, rdflib.SOSA.isSampleOf, feature_of_interest))
        graph.add((uri, utils.namespaces.TERN.featureType, CONCEPT_SEQUENCE))

        # Loop Through Associated Sequences
        for identifier in row["associatedSequences"]:
            # Add Identifier
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(identifier)))

    def add_provider_determined_by(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Determined By Provider to the Graph

        Args:
            uri: URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            graph (rdflib.Graph): Graph to add to
        """
        # Check for threatStatusDeterminedBy
        if not uri:
            return

        # Add to Graph
        graph.add((uri, a, rdflib.PROV.Agent))
        graph.add((uri, rdflib.SDO.name, rdflib.Literal(row["threatStatusDeterminedBy"])))

    def add_threat_status_observation(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        threat_status_value: rdflib.URIRef,
        determined_by: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Threat Status Observation to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            provider_record_id_occurrence (rdflib.URIRef): Occurrence associated with this node
            threat_status_value (rdflib.URIRef): Threat Status Value associated
                with this node
            determined_by: Determined By Provider associated with this node
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["threatStatus"]:
            return

        # Get Timestamp
        # Prefer `threatStatusDateDetermined` > `dateIdentified` > `eventDateStart` (fallback)
        date_determined: models.temporal.Timestamp = (
            row["threatStatusDateDetermined"] or row["dateIdentified"] or row["preparedDate"] or row["eventDateStart"]
        )

        # Retrieve vocab for field
        vocab = self.fields()["threatStatusCheckProtocol"].get_flexible_vocab()

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(
            row["threatStatusCheckProtocol"]
        )

        # Threat Status Observation
        graph.add((uri, a, utils.namespaces.TERN.Observation))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, rdflib.RDFS.comment, rdflib.Literal("threatStatus-observation")))
        graph.add((uri, rdflib.SOSA.hasFeatureOfInterest, provider_record_id_occurrence))
        graph.add((uri, rdflib.SOSA.hasResult, threat_status_value))
        graph.add((uri, rdflib.SOSA.hasSimpleResult, rdflib.Literal(row["threatStatus"])))
        graph.add((uri, rdflib.SOSA.observedProperty, CONCEPT_CONSERVATION_STATUS))
        graph.add((uri, rdflib.SOSA.usedProcedure, term))
        temporal_entity = rdflib.BNode()
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))
        graph.add((temporal_entity, a, rdflib.TIME.Instant))
        graph.add((temporal_entity, date_determined.rdf_in_xsd, date_determined.to_rdf_literal()))

        # Check for threatStatusDeterminedBy
        if determined_by:
            # Add wasAssociatedWith
            graph.add((uri, rdflib.PROV.wasAssociatedWith, determined_by))

        # Check for threatStatusDateDetermined
        if not row["threatStatusDateDetermined"]:
            # Determine Used Date Column
            date_used = (
                "dateIdentified"
                if row["dateIdentified"]
                else "preparedDate"
                if row["preparedDate"]
                else "eventDateStart"
            )

            # Add comment to temporal entity
            comment = f"Date unknown, template {date_used} used as proxy"
            graph.add((temporal_entity, rdflib.RDFS.comment, rdflib.Literal(comment)))

    def add_threat_status_value(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Threat Status Value to the Graph

        Args:
            uri (rdflib.URIRef): URI to use for this node
            row (frictionless.Row): Row to retrieve data from
            dataset (rdflib.URIRef): Dataset this belongs to
            graph (rdflib.Graph): Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if not row["threatStatus"]:
            return

        # Retrieve vocab for field
        vocab = self.fields()["threatStatus"].get_flexible_vocab()
        if not issubclass(vocab, vocabs.threat_status.ThreatStatus):
            raise RuntimeError("threatStatus vocabulary is expected to be ThreatStatus")

        # Retrieve term or Create on the Fly
        term = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get_threat_status(
            conservation_authority=row["conservationAuthority"], threat_status=row["threatStatus"]
        )

        # Threat Status Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(f"Conservation status = {row['threatStatus']}")))
        graph.add((uri, rdflib.RDF.value, term))

    def add_conservation_authority_attribute(
        self,
        *,
        uri: rdflib.URIRef | None,
        conservation_authority: str | None,
        conservation_authority_value: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Conservation Authority Attribute to the Graph

        Args:
            uri: URI to use for this node.
            conservation_authority: conservationAuthority value from the CSV
            conservation_authority_value: Conservation Authority Value associated with this node
            dataset: Dataset this belongs to
            graph: Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        # Conservation Authority Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_CONSERVATION_AUTHORITY))
        if conservation_authority:
            graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(conservation_authority)))
        if conservation_authority_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, conservation_authority_value))

    def add_conservation_authority_value(
        self,
        *,
        uri: rdflib.URIRef | None,
        conservation_authority: str | None,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Conservation Authority Value to the Graph

        Args:
            uri: URI to use for this node
            conservation_authority: conservationAuthority value from the CSV
            graph: Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))

        if conservation_authority:
            # Construct Label
            graph.add((uri, rdflib.RDFS.label, rdflib.Literal(conservation_authority)))

            # Retrieve vocab for field
            vocab = self.fields()["conservationAuthority"].get_vocab()
            # Retrieve term
            term = vocab().get(conservation_authority)
            # Conservation Authority Value
            graph.add((uri, rdflib.RDF.value, term))

    def add_conservation_authority_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        conservation_authority: str | None,
        conservation_authority_attribute: rdflib.URIRef | None,
        threat_status_observation: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a conservation authority Collection to the graph

        Args:
            uri: The uri for the SampleCollection.
            conservation_authority: conservationAuthority value from template.
            conservation_authority_attribute: The uri for the attribute node.
            threat_status_observation: The node that should be a member of the collection.
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
        if conservation_authority:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Conservation Authority - {conservation_authority}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # add link to the threat status observation node
        graph.add((uri, rdflib.SDO.member, threat_status_observation))
        # Add link to attribute
        if conservation_authority_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, conservation_authority_attribute))

    def add_sensitivity_category_attribute(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        sensitivity_category_value: rdflib.URIRef | None,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds Sensitivity Category Attribute to the Graph

        Args:
            uri: URI to use for this node.
            row: Row to retrieve data from
            dataset: Dataset this belongs to
            sensitivity_category_value: Sensitivity Category Value associated with this node
            graph: Graph to add to
        """
        # Check Existence
        if uri is None:
            return

        simple_value = f"{row['sensitivityCategory']} - {row['sensitivityAuthority']}"

        # Sensitivity Category Attribute
        graph.add((uri, a, utils.namespaces.TERN.Attribute))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        graph.add((uri, utils.namespaces.TERN.attribute, CONCEPT_SENSITIVITY_CATEGORY))
        graph.add((uri, utils.namespaces.TERN.hasSimpleValue, rdflib.Literal(simple_value)))
        if sensitivity_category_value:
            graph.add((uri, utils.namespaces.TERN.hasValue, sensitivity_category_value))

    def add_sensitivity_category_value(
        self,
        uri: rdflib.URIRef | None,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds Sensitivity Category Value to the Graph

        Args:
            uri: URI to use for this node
            row: Row to retrieve data from
            dataset: Dataset this belongs to
            graph: Graph to add to
            submitted_on_date: The date the data was submitted.
        """
        # Check Existence
        if uri is None:
            return

        # Retrieve vocab for field
        vocab = self.fields()["sensitivityCategory"].get_flexible_vocab()
        vocab_instance = vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date)

        # Set the scope note to use if a new term is created on the fly.
        scope_note = f"Under the authority of {row['sensitivityAuthority']}"
        if not isinstance(vocab_instance, utils.vocabs.FlexibleVocabulary):
            raise RuntimeError("sensitiveCategory vocabulary is expected to be a FlexibleVocabulary")
        vocab_instance.scope_note = rdflib.Literal(scope_note)
        # This has to be done here, instead of at the Vocabulary definition,
        # because the value is computed from another field (sensitivityAuthority).

        # Retrieve term or Create on the Fly
        term = vocab_instance.get(row["sensitivityCategory"])

        # Construct Label
        label = f"sensitivity category = {row['sensitivityCategory']}"

        # Conservation Authority Value
        graph.add((uri, a, utils.namespaces.TERN.IRI))
        graph.add((uri, a, utils.namespaces.TERN.Value))
        graph.add((uri, rdflib.RDFS.label, rdflib.Literal(label)))
        graph.add((uri, rdflib.RDF.value, term))

    def add_sensitivity_category_collection(
        self,
        *,
        uri: rdflib.URIRef | None,
        sensitivity_category: str | None,
        sensitivity_category_attribute: rdflib.URIRef | None,
        provider_record_id_biodiversity_record: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Add a sensitivity category Collection to the graph

        Args:
            uri: The uri for the Collection.
            sensitivity_category: sensitivityCategory value from template.
            sensitivity_category_attribute: The uri for the attribute node.
            provider_record_id_biodiversity_record: The biodiversity record.
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
        if sensitivity_category:
            graph.add(
                (
                    uri,
                    rdflib.SDO.name,
                    rdflib.Literal(f"Occurrence Collection - Sensitivity Category - {sensitivity_category}"),
                )
            )
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))
        # Add link to attribute
        if sensitivity_category_attribute:
            graph.add((uri, utils.namespaces.TERN.hasAttribute, sensitivity_category_attribute))
        # Add link to the biodiversity record
        graph.add((uri, rdflib.SDO.member, provider_record_id_biodiversity_record))

    def add_biodiversity_record(
        self,
        uri: rdflib.URIRef,
        provider_record_id_datatype: rdflib.URIRef,
        provider_record_id_occurrence: rdflib.URIRef,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
    ) -> None:
        """Adds biodiversity record node to graph.

        Args:
            uri: Subject of the node.
            provider_record_id_datatype: The datatype associated with
                the provider record id.
            provider_record_id_occurrence: Reference to the occurrence
                of the row.
            dataset: The uri for the dateset node.
            row: Raw data for row.
            graph: Graph to be modified.
        """
        # Add class
        graph.add((uri, a, utils.namespaces.ABIS.BiodiversityRecord))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))
        # Add identifier value literal
        graph.add(
            (uri, rdflib.SDO.identifier, rdflib.Literal(row["providerRecordID"], datatype=provider_record_id_datatype))
        )
        # Add about property
        graph.add((uri, rdflib.SDO.about, provider_record_id_occurrence))
        # Add link to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

    def add_occurrence(
        self,
        uri: rdflib.URIRef,
        record_number_datatype: rdflib.URIRef | None,
        owner_record_id_datatype: rdflib.URIRef | None,
        other_catalog_numbers_datatype: rdflib.URIRef | None,
        catalog_number_datatype: rdflib.URIRef | None,
        provider_recorded_by: rdflib.URIRef | None,
        dataset: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
    ) -> None:
        """Adds occurrence node to the graph.

        Args:
            uri: Subject of the node.
            record_number_datatype: Datatype associated with the recordNumber.
            owner_record_id_datatype: Datatype associated with the owner recordID.
            other_catalog_numbers_datatype: Datatype associated with other catalog numbers.
            catalog_number_datatype: Catalog number source datatype.
            provider_recorded_by: Agent derived from the recordedBy field.
            dataset: The uri for the dateset node.
            row: Raw data from the row.
            graph: Graph to be modified.
            submitted_on_date: The date the data was submitted.
        """
        # Class
        graph.add((uri, a, utils.namespaces.DWC.Occurrence))
        graph.add((uri, a, utils.namespaces.TERN.FeatureOfInterest))
        if submission_iri:
            graph.add((uri, rdflib.VOID.inDataset, submission_iri))

        # Add to dataset
        graph.add((uri, rdflib.SDO.isPartOf, dataset))

        # Add identifiers
        if record_number := row["recordNumber"]:
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(record_number, datatype=record_number_datatype)))
        if owner_record_id := row["ownerRecordID"]:
            graph.add((uri, rdflib.SDO.identifier, rdflib.Literal(owner_record_id, datatype=owner_record_id_datatype)))
        for catalog_number in row["otherCatalogNumbers"] or []:
            graph.add(
                (uri, rdflib.SDO.identifier, rdflib.Literal(catalog_number, datatype=other_catalog_numbers_datatype))
            )

        # Add feature type from vocab
        kingdom_vocab = self.fields()["kingdom"].get_flexible_vocab("KINGDOM_OCCURRENCE")
        kingdom_term = kingdom_vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(
            row["kingdom"]
        )
        graph.add((uri, utils.namespaces.TERN.featureType, kingdom_term))

        # Create geometry
        geometry = models.spatial.Geometry(
            raw=models.spatial.LatLong(row["decimalLatitude"], row["decimalLongitude"]),
            datum=row["geodeticDatum"],
        )

        # Add geometry
        geometry_node = rdflib.BNode()
        graph.add((uri, rdflib.SDO.spatial, geometry_node))
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, geometry.to_transformed_crs_rdf_literal()))

        # Check for coordinateUncertaintyInMeters
        accuracy: rdflib.Literal | None = None
        if coordinate_uncertainty := row["coordinateUncertaintyInMeters"]:
            # Add Spatial Accuracy
            accuracy = rdflib.Literal(coordinate_uncertainty, datatype=rdflib.XSD.double)
            graph.add((geometry_node, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

        # Add 'supplied as' geometry
        self.add_geometry_supplied_as(
            subj=uri,
            pred=rdflib.SDO.spatial,
            obj=geometry_node,
            geom=geometry,
            graph=graph,
            spatial_accuracy=accuracy,
        )

        # Add temporal entity
        event_date_start: models.temporal.Timestamp = row["eventDateStart"]
        event_date_end: models.temporal.Timestamp | None = row["eventDateEnd"]
        temporal_node = rdflib.BNode()
        graph.add((uri, rdflib.SDO.temporal, temporal_node))
        # When end date is provided, give temporal node a start/end
        if event_date_end is not None:
            graph.add((temporal_node, a, rdflib.TIME.TemporalEntity))
            # Start date
            start_instant = rdflib.BNode()
            graph.add((start_instant, a, rdflib.TIME.Instant))
            graph.add((start_instant, event_date_start.rdf_in_xsd, event_date_start.to_rdf_literal()))
            graph.add((temporal_node, rdflib.TIME.hasBeginning, start_instant))
            # End date
            end_instant = rdflib.BNode()
            graph.add((end_instant, a, rdflib.TIME.Instant))
            graph.add((end_instant, event_date_end.rdf_in_xsd, event_date_end.to_rdf_literal()))
            graph.add((temporal_node, rdflib.TIME.hasEnd, end_instant))
        # Else only start date, make temporal node an Instant
        else:
            graph.add((temporal_node, a, rdflib.TIME.Instant))
            graph.add((temporal_node, event_date_start.rdf_in_xsd, event_date_start.to_rdf_literal()))

        # Add procedure from vocab
        protocol_vocab = self.fields()["samplingProtocol"].get_flexible_vocab()
        protocol_term = protocol_vocab(graph=graph, source=dataset, submitted_on_date=submitted_on_date).get(
            row["samplingProtocol"]
        )
        graph.add((uri, rdflib.SOSA.usedProcedure, protocol_term))

        # Add location description if provided
        if locality := row["locality"]:
            graph.add((uri, utils.namespaces.TERN.locationDescription, rdflib.Literal(locality)))

        # Add associated with agents if provided
        if provider_recorded_by is not None:
            graph.add((uri, rdflib.PROV.wasAssociatedWith, provider_recorded_by))

        # Check for catalogNumber
        if row["catalogNumber"]:
            # Add to Graph
            graph.add(
                (
                    uri,
                    utils.namespaces.DWC.catalogNumber,
                    rdflib.Literal(row["catalogNumber"], datatype=catalog_number_datatype),
                )
            )

        # Check for collectionCode
        if row["collectionCode"]:
            # Add to Graph
            graph.add((uri, utils.namespaces.DWC.collectionCode, rdflib.Literal(row["collectionCode"])))


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
    if row["preparations"] or row["associatedSequences"]:
        # If either of `preparations` or `associatedSequences`
        # are provided, regardless of the value of `basisOfRecord` we can infer
        # that there is a specimen associated with the row.
        specimen = True

    elif (
        not row["basisOfRecord"]  # Blank
        or vocabs.basis_of_record.HUMAN_OBSERVATION.match(row["basisOfRecord"])  # HumanObservation
        or vocabs.basis_of_record.OCCURRENCE.match(row["basisOfRecord"])  # Occurrence
    ):
        # Otherwise, if neither of `preparations` or
        # `associatedSequences` were provided, and the `basisOfRecord` is
        # either blank or one of "HumanObservation" or "Occurrence", then we
        # cannot infer that there is a specimen associated with the row.
        specimen = False

    else:
        # Finally, neither of `preparations` or
        # `associatedSequences` were provided, but the `basisOfRecord` is a
        # value that implies that there is a specimen associated with the row.
        specimen = True

    # Return
    return specimen


# Register mapper
base.mapper.register_mapper(IncidentalOccurrenceMapper)
