"""Functions related to documentation."""

# Standard library
import urllib.parse

# Third-party
import pydantic

# Local
from abis_mapping import settings


def get_submission_properties_url() -> str:
    """Get a url to the submission properties page of the documentation."""
    # Create url to the docs
    url = urllib.parse.urljoin(
        base=settings.SETTINGS.INSTRUCTIONS_BASE_URL,
        url="/".join([settings.SETTINGS.INSTRUCTIONS_VERSION, "submission_properties"]),
    )
    # Check it is valid url
    pydantic.AnyUrl(url)
    return url
