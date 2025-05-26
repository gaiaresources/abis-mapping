"""Tests for the submission properties docs."""

# Local
import abis_mapping.documentation


def test_get_dataset_properties_url() -> None:
    assert (
        abis_mapping.documentation.get_dataset_properties_url()
        == "https://gaiaresources.github.io/abis-mapping/dev/dataset_properties"
    )
