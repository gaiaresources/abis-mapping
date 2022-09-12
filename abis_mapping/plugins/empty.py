"""Provides extra frictionless empty data checks for the package"""


# Third-Party
import frictionless

# Typing
from typing import Iterator


class NotEmpty(frictionless.Check):
    """Checks whether the resource has at least 1 row."""

    # Check Attributes
    code = "not-empty"
    Errors = [frictionless.errors.TableDimensionsError]

    def validate_end(self) -> Iterator[frictionless.Error]:
        """Called to validate the resource before closing.

        Yields:
            frictionless.Error: If the table is empty.
        """
        # Check Number of Rows
        if not self.resource.stats.get("rows"):
            # Yield Error
            yield frictionless.errors.TableDimensionsError(
                note="Current number of rows is 0, the minimum is 1",
                limits={"minRows": 1, "numberRows": 0},
            )
