"""Mapper implementation for the incidental occurrence delete v1 template."""

# Standard library
import datetime

# Third-Party
import frictionless
import rdflib

# Local
from abis_mapping import base
from abis_mapping import plugins

# Typing
from typing import Any


class IncidentalOccurrenceDeleteMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `incidental_occurrence_delete.csv` - version 1"""

    def apply_validation(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `incidental_occurrence_delete.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct Schema
        schema = self.regular_fields_schema()

        # Construct Resource
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=schema,
            encoding="utf-8",
        )

        # Validate
        report: frictionless.Report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra Custom Checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                ],
            ),
        )

        # Return Validation Report
        return report

    def apply_mapping_row(
        self,
        *,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        extra_schema: frictionless.Schema,
        base_iri: rdflib.Namespace,
        submission_iri: rdflib.URIRef | None,
        submitted_on_date: datetime.date,
        **kwargs: Any,
    ) -> None:
        """Applies Mapping for a Row in the `incidental_occurrence_delete.csv` Template

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset uri this row is apart of.
            graph (rdflib.Graph): Graph to map row into.
            extra_schema (frictionless.Schema): Schema of extra fields.
            base_iri (rdflib.Namespace): Base IRI namespace to use for mapping.
            submitted_on_date: The date the data was submitted.

        Returns:
            rdflib.Graph: Graph with row mapped into it.
        """
        # TODO mapping
        # TODO might need to get rid of per-chunk mapping for this template?


# Register mapper
base.mapper.register_mapper(IncidentalOccurrenceDeleteMapper)
