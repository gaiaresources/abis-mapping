"""Provides more generic custom implementations of the row_constraint check"""

# Third-party
import attrs
import frictionless
import frictionless.checks
import frictionless.errors
import simpleeval

# Typing
from typing import Any, Mapping, Iterable


class SideInputError(frictionless.errors.TableError):
    type = "side-input"
    title = "Side Input Error"
    description = "This error can happen if there is issue with provided side input data."
    template = "The side input data does not comply with requirements: {note}"


@attrs.define(kw_only=True, repr=False)
class RowConstraintSideInput(frictionless.checks.row_constraint):
    """Implementation of row_constraint providing a side input.

    A way of providing simplistic forms of custom validation on a
    row-wise basis, through provision of a formula as a string.

    Attributes:
        side_inputs: Map of names and extra values to provide to
            formula.
        original_schema: Optional schema to limit the names that can
            be used by the formula, preventing extra fields being
            injected into validation.
        _field_names: List of field names included in the schema to be
            used by the check. Populated at the start of validation.
    """

    Errors = [frictionless.errors.RowConstraintError, SideInputError]
    side_inputs: Mapping[str, Any]
    original_schema: frictionless.Schema | None = None
    _field_names: list[str] = attrs.field(factory=list, alias="field_names")

    def validate_start(self) -> Iterable[SideInputError]:
        """Start of validation

        Yields:
            If there is an unresolvable name clash between the side
                inputs and the row fieldnames.
        """
        # Determine which schema to use
        schema = self.original_schema or self.resource.schema
        # Assign field names to be used in later validations
        self._field_names = [*schema.field_names]
        clashes: set[str] = set(self.side_inputs).intersection(set(self._field_names))
        if clashes:
            yield SideInputError(note=f"Name clashes between side inputs and schema: {clashes}")

    def validate_row(self, row: frictionless.Row) -> Iterable[frictionless.Error]:
        """Validate row (every row).

        Args:
            row: Row of data to be validated.

        Yields:
            Errors encountered, if any
        """
        try:
            # Check original_schema
            # Filter names based on schema originally supplied - no additional columns can be used
            names: dict[str, object] = {k: v for k, v in row.items() if k in self._field_names}
            # Concatenate the the side inputs
            names.update(self.side_inputs)
            # This call should be considered as a safe expression evaluation
            evalclass = simpleeval.EvalWithCompoundTypes
            assert evalclass(names=names).eval(self.formula)  # noqa: S101
        except Exception:
            yield frictionless.errors.RowConstraintError.from_row(
                row,
                note='the row constraint to conform is "%s"' % self.formula,
            )
