"""Provides extra frictionless tabular checks for the package"""


# Third-Party
import frictionless
import frictionless.errors

# Typing
from typing import Iterator


class IsTabular(frictionless.Check):
    """Checks whether the resource is at least tabular data in nature."""

    # Check Attributes
    type = "is-tabular"
    Errors = [frictionless.errors.SourceError]

    def validate_start(self) -> Iterator[frictionless.Error]:
        """Called to validate the resource after opening

        Yields:
            frictionless.Error: If the resource is not tabular data.
        """
        # Check if tabular
        if not self.resource.tabular:
            # Yield Error
            yield frictionless.errors.SourceError(
                note="the source is not tabular data",
            )
