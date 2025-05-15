"""Tests for the submission properties docs."""

# Local
import abis_mapping.documentation


def test_get_submission_properties_url() -> None:
    assert (
        abis_mapping.documentation.get_submission_properties_url()
        == "https://gaiaresources.github.io/abis-mapping/dev/submission_properties"
    )
