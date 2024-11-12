"""This module contains functions for constructing IRIs according to common patterns.

This is important when the exact same IRI needs to be constructed from multiple template
mappings so that the output RDF links together on these IRIs."""

# third party
import rdflib

# local
from abis_mapping import utils

# typing
from typing import Literal


def survey_iri(
    base_iri: rdflib.Namespace | None,
    survey_id: str | None,
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
        # surveyID is an optional field. When missing fallback to the row number.
        # (which is always 1 for a Survey, since metadata template must have 1 row)
        survey_id=(survey_id or "1"),
    )


def site_iri(
    base_iri: rdflib.Namespace | None,
    site_id: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI for the tern:Site node, constructed from the siteID field.

    This IRI is used in mapping multiple Systematic Survey template,
    and needs to be the same for all of them.

    Args:
        base_iri: The namespace to construct the IRI from.
        site_id: The siteID field from the template.

    Returns:
        The IRI for the tern:Survey node.
    """
    return utils.rdf.uri_quoted(base_iri, "Site/{site_id}", site_id=site_id)


def site_visit_iri(
    base_iri: rdflib.Namespace | None,
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


def attribute_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"attribute/{attribute}/{value}", namespace=base_iri)


def attribute_value_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"value/{attribute}/{value}", namespace=base_iri)


def attribute_collection_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"{collection_type}Collection/{attribute}/{value}", namespace=base_iri)


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
    return utils.rdf.uri(
        f"{identifier_type}/{identifier_source}",
        namespace=utils.namespaces.BDR_DATATYPES,
    )


def agent_iri(
    org: str,
    /,
) -> rdflib.URIRef:
    """Get the IRI to use for a prov:Agent node.

    Args:
        org: The org this agent node represents.

    Returns:
        URIRef for the prov:Agent node.
    """
    return utils.rdf.uri(
        f"{org}",
        namespace=utils.namespaces.BDR_ORGS,
    )


def observation_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"observation/{observation_type}/{provider_record_id}", namespace=base_iri)


def observation_value_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"result/{observation_type}/{observation_value}", namespace=base_iri)


def specimen_observation_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"observation/specimen/{observation_type}/{provider_record_id}", namespace=base_iri)


def specimen_observation_value_iri(
    base_iri: rdflib.Namespace | None,
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
    return utils.rdf.uri(f"result/specimen/{observation_type}/{observation_value}", namespace=base_iri)


def sample_iri(
    base_iri: rdflib.Namespace | None,
    sample_type: str,
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
    return utils.rdf.uri(f"sample/{sample_type}/{provider_record_id}", namespace=base_iri)


def sampling_iri(
    base_iri: rdflib.Namespace | None,
    sampling_type: str,
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
    return utils.rdf.uri(f"sampling/{sampling_type}/{provider_record_id}", namespace=base_iri)


def plan_iri(
    base_iri: rdflib.Namespace | None,
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
