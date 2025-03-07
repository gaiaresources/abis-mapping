"""This module contains functions for constructing IRIs according to common patterns.

This is important when the exact same IRI needs to be constructed from multiple template
mappings so that the output RDF links together on these IRIs."""

# Standard library
import functools
import hashlib

# third party
import rdflib

# local
from abis_mapping import utils

# typing
from typing import Literal


def survey_iri(
    base_iri: rdflib.Namespace,
    survey_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI for the tern:Survey node, constructed from the surveyID field.

    This IRI is used in mapping multiple Systematic Survey template,
    and needs to be the same for all of them.

    Args:
        base_iri: The namespace to construct the IRI from.
        survey_id: The surveyID field from the template.

    Returns:
        The IRI for the tern:Survey node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "Survey/{survey_id}",
        survey_id=survey_id,
    )


def site_iri(
    site_id_source: str,
    site_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI for the tern:Site node, constructed from the siteID+siteIDSource fields.

    This IRI is used in mapping multiple Systematic Survey template,
    and needs to be the same for all of them.

    Args:
        site_id: The siteID field from the template.
        site_id_source: The siteIDSource field from the template.

    Returns:
        The IRI for the tern:Survey node.
    """
    # Note: the site_id_source (typically an organisation name) is slugified for readability,
    # But the site_id is url-quoted, to preserve any special characters with their representation.
    site_id_source = utils.rdf.slugify_for_uri(site_id_source)
    site_id = utils.rdf.quote_for_uri(site_id)
    return utils.namespaces.DATASET_BDR[f"sites/{site_id_source}/{site_id}"]


def site_visit_iri(
    base_iri: rdflib.Namespace,
    site_visit_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI for the tern:SiteVisit node, constructed from the siteVisitID field.

    This IRI is used in mapping multiple Systematic Survey template,
    and needs to be the same for all of them.

    Args:
        base_iri: The namespace to construct the IRI from.
        site_visit_id: The siteVisitID field from the template.

    Returns:
        The IRI for the tern:Survey node.
    """
    return utils.rdf.uri_quoted(base_iri, "SiteVisit/{site_visit_id}", site_visit_id=site_visit_id)


def occurrence_iri(
    base_iri: rdflib.Namespace,
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """
    Get the IRI to use for a dwc:Occurrence node.

    Args:
        base_iri: The Namespace to construct the IRI from.
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the dwc:Occurrence node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "occurrence/{provider_record_id}",
        provider_record_id=provider_record_id,
    )


def biodiversity_record_iri(
    base_iri: rdflib.Namespace,
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """
    Get the IRI to use for an abis:BiodiversityRecord node.

    Args:
        base_iri: The Namespace to construct the IRI from.
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the abis:BiodiversityRecord node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "biodiversityRecord/{provider_record_id}",
        provider_record_id=provider_record_id,
    )


def attribute_iri(
    base_iri: rdflib.Namespace,
    attribute: str,
    value: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Attribute node.

    Args:
        base_iri: The namespace to construct the IRI from.
        attribute: Typically the name of the CSV field.
        value: The value of the attribute.

    Returns:
        IRI for the tern:Attribute node.
    """
    return utils.rdf.uri_slugified(base_iri, "attribute/{attribute}/{value}", attribute=attribute, value=value)


def attribute_value_iri(
    base_iri: rdflib.Namespace,
    attribute: str,
    value: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Value node associated with a tern:Attribute node.

    Args:
        base_iri: The namespace to construct the IRI from.
        attribute: Typically the name of the CSV field.
        value: The value of the attribute.

    Returns:
        IRI for the tern:Value node.
    """
    return utils.rdf.uri_slugified(base_iri, "value/{attribute}/{value}", attribute=attribute, value=value)


def attribute_collection_iri(
    base_iri: rdflib.Namespace,
    collection_type: Literal["Survey", "Occurrence", "Site", "SiteVisit"],
    attribute: str,
    value: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a schema:Collection node associated with a tern:Attribute node.

    Args:
        base_iri: The namespace to construct the IRI from.
        collection_type: What 'type' of Collection this is. Corresponds to the template being mapped.
        attribute: Typically the name of the CSV field.
        value: The value of the attribute.

    Returns:
        IRI for the schema:Collection node.
    """
    return utils.rdf.uri_slugified(
        base_iri,
        "{collection_type}Collection/{attribute}/{value}",
        collection_type=collection_type,
        attribute=attribute,
        value=value,
    )


def datatype_iri(
    identifier_type: str,
    identifier_source: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a rdfs:Datatype node.

    This node typically represents the source of an identifier.

    Args:
        identifier_type: What identifier the datatype is for. e.g. "surveyID", "catalogNumber"
        identifier_source: The source of the identifier.
            e.g. the value for the "surveyOrgs" or "catalogNumberSource" template fields.

    Returns:
        URIRef for the rdfs:Datatype node.
    """
    return utils.rdf.uri_slugified(
        utils.namespaces.BDR_DATATYPES,
        "{identifier_type}/{identifier_source}",
        identifier_type=identifier_type,
        identifier_source=identifier_source,
    )


@functools.lru_cache()
def _hash_person_for_iri(agent: str, /) -> str:
    """Standard function for hashing an agent string to use in an IRI."""
    return hashlib.blake2b(agent.encode("utf-8"), digest_size=8, person=b"person_iri_hash").hexdigest()


def agent_iri(
    agent_type: Literal["org", "person", "software"],
    agent: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a prov:Agent node.

    Args:
        agent_type: What type of agent this is.
        agent: The organization or person this agent node represents.

    Returns:
        URIRef for the prov:Agent node.
    """
    # For person IRIs, use a hash of the name, instead of the name itself.
    if agent_type == "person":
        agent = _hash_person_for_iri(agent)

    return utils.rdf.uri_slugified(
        utils.namespaces.DATASET_BDR,
        "{agent_type}/{agent}",
        agent_type=agent_type,
        agent=agent,
    )


def observation_iri(
    base_iri: rdflib.Namespace,
    observation_type: str,
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Observation node, when the observation is related to an Occurrence.

    Args:
        base_iri: Namespace to construct the IRI from.
        observation_type: The observation type, e.g. "scientificName"
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the tern:Observation node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "observation/{observation_type}/{provider_record_id}",
        observation_type=observation_type,
        provider_record_id=provider_record_id,
    )


def observation_value_iri(
    base_iri: rdflib.Namespace,
    observation_type: str,
    observation_value: str | None,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Value node, that represent the "result" of an observation.

    Args:
        base_iri: Namespace to construct the IRI from.
        observation_type: The observation type, e.g. "scientificName"
        observation_value: The value of the observation from the template.

    Returns:
        The IRI for the tern:Value node.
    """
    return utils.rdf.uri_slugified(
        base_iri,
        "result/{observation_type}/{observation_value}",
        observation_type=observation_type,
        # Should probably be refactored to return None when observation_value is None
        # but that would need lots of changes to mapping.
        observation_value=str(observation_value),
    )


def specimen_observation_iri(
    base_iri: rdflib.Namespace,
    observation_type: str,
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Observation node, when the observation is related to a Specimen.

    Args:
        base_iri: Namespace to construct the IRI from.
        observation_type: The observation type, e.g. "scientificName"
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the tern:Observation node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "observation/specimen/{observation_type}/{provider_record_id}",
        observation_type=observation_type,
        provider_record_id=provider_record_id,
    )


def specimen_observation_value_iri(
    base_iri: rdflib.Namespace,
    observation_type: str,
    observation_value: str | None,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Value node, that represent the "result" of a specimen observation.

    Args:
        base_iri: Namespace to construct the IRI from.
        observation_type: The observation type, e.g. "scientificName"
        observation_value: The value of the observation from the template.

    Returns:
        The IRI for the tern:Value node.
    """
    return utils.rdf.uri_slugified(
        base_iri,
        "result/specimen/{observation_type}/{observation_value}",
        observation_type=observation_type,
        # Should probably be refactored to return None when observation_value is None
        # but that would need lots of changes to mapping.
        observation_value=str(observation_value),
    )


def sample_iri(
    base_iri: rdflib.Namespace,
    sample_type: Literal["specimen", "sequence"],
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Sample node.

    Args:
        base_iri: Namespace to construct the IRI from.
        sample_type: The sample type, e.g. "specimen"
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the tern:Sample node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "sample/{sample_type}/{provider_record_id}",
        sample_type=sample_type,
        provider_record_id=provider_record_id,
    )


def sampling_iri(
    base_iri: rdflib.Namespace,
    sampling_type: Literal["specimen", "sequencing"],
    provider_record_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a tern:Sampling node.

    Args:
        base_iri: Namespace to construct the IRI from.
        sampling_type: The sampling type, e.g. "specimen"
        provider_record_id: The providerRecordID field from the template.

    Returns:
        The IRI for the tern:Sampling node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "sampling/{sampling_type}/{provider_record_id}",
        sampling_type=sampling_type,
        provider_record_id=provider_record_id,
    )


def plan_iri(
    base_iri: rdflib.Namespace,
    plan_type: Literal["survey", "visit"],
    plan_type_id: str,
) -> rdflib.URIRef:
    """Get the IRI to use for a prov:Plan node.

    These are associated with a Survey or a Site Visit.

    Args:
        base_iri: The Namespace to construct the IRI from.
        plan_type: Either "survey" or "visit"
        plan_type_id: The id to put at the end of the IRI

    Returns:
        The IRI for the prov:Plan node.
    """
    return utils.rdf.uri_quoted(
        base_iri,
        "{plan_type}/plan/{plan_type_id}",
        plan_type=plan_type,
        plan_type_id=plan_type_id,
    )


def attribution_iri(
    role: Literal[
        "contributor",
        "creator",
        "custodian",
        "funder",
        "originator",
        "owner",
        "principalInvestigator",
        "resourceProvider",
        "rightsHolder",
    ],
    source: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a prov:Attribution node.

    Args:
        role: Corresponds to the Object of the PROV:hadRole predicate on the prov:Attribution node.
        source: Who the attribution is for, e.g. "providerRecordIDSource" value.

    Returns:
        The IRI for the prov:Attribution node.
    """
    return utils.rdf.uri_slugified(
        utils.namespaces.DATASET_BDR,
        "attribution/{source}/{role}",
        source=source,
        role=role,
    )
