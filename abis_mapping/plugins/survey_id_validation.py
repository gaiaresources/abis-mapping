# Third-Party
import attrs
import frictionless
import frictionless.errors

# Typing
from collections.abc import Iterator, Set


@attrs.define(kw_only=True, repr=False)
class SurveyIDValidation(frictionless.Check):
    """Validates that the surveyID field, if provided, is valid.

    Attributes:
        valid_survey_ids: surveyIDs from the metadata template.
    """

    # Check Attributes
    type = "survey-id-validation"
    Errors = [frictionless.errors.RowConstraintError]

    # Attributes specific to this check
    valid_survey_ids: Set[str]

    def validate_row(self, row: frictionless.Row) -> Iterator[frictionless.Error]:
        """Called to validate the given row (on every row).

        Args:
            row (frictionless.Row): The row to check.

        Yields:
            frictionless.Error: Any errors detected.
        """
        # Get surveyID value, which can be None
        survey_id: str | None = row["surveyID"]
        # If you want surveyID to be required, use "required": true in conjunction
        # with this check.

        # If None, don't check anything
        if survey_id is None:
            return

        # Otherwise check that surveyID is one of the valid values
        if survey_id not in self.valid_survey_ids:
            yield frictionless.errors.ConstraintError.from_row(
                row=row,
                note="surveyID must match a surveyID in the survey_metadata template",
                field_name="surveyID",
            )
