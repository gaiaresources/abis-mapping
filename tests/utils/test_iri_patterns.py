import rdflib

from abis_mapping.utils import iri_patterns


def test_site_iri() -> None:
    result = iri_patterns.site_iri("GAIA", "S1")
    assert result == rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/sites/GAIA/S1")


def test_site_iri_with_special_chars() -> None:
    result = iri_patterns.site_iri("GAIA (WA)", "P1:S1/QQ")
    assert result == rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/sites/GAIA-WA/P1%3AS1%2FQQ")
