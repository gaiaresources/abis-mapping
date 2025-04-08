import rdflib

from abis_mapping.utils import iri_patterns


def test_site_iri() -> None:
    result = iri_patterns.site_iri("GAIA", "S1")
    assert result == rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/sites/GAIA/S1")


def test_site_iri_with_special_chars() -> None:
    result = iri_patterns.site_iri("GAIA (WA)", "P1:S1/QQ")
    assert result == rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/sites/GAIA-WA/P1%3AS1%2FQQ")


def test_association_iri() -> None:
    result = iri_patterns.association_iri("resourceProvider", "Some Org", source_type="org")
    assert result == rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/association/Some-Org/resourceProvider")


def test_association_iri_for_person() -> None:
    result = iri_patterns.association_iri("resourceProvider", "Some Person", source_type="person")
    assert result == rdflib.URIRef(
        "https://linked.data.gov.au/dataset/bdr/association/d64b38038ac0eb40/resourceProvider"
    )


def test_hash_person_for_iri() -> None:
    """Test the _hash_person_for_iri function"""
    # This test should never change, or it means everyone will get new IRIs.
    assert iri_patterns._hash_person_for_iri("Some Person") == "d64b38038ac0eb40"
    assert iri_patterns._hash_person_for_iri("person@example.com") == "cf9fc50ba9c93e55"


def test_delegation_iri() -> None:
    result = iri_patterns.delegation_iri("resourceProvider", "Some Person", "Some Org")
    assert result == rdflib.URIRef(
        "https://linked.data.gov.au/dataset/bdr/delegation/d64b38038ac0eb40/Some-Org/resourceProvider"
    )
