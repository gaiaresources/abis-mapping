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
    *,
    survey_id: str | None,
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
