from typing import Optional, Iterator

import frictionless
import rdflib

from abis_mapping import base
from abis_mapping import plugins


class SurveyMetadataMapper(base.mapper.ABISMapper):
    template_id = "survey_metadata.csv"
    instructions_file = "instructions.pdf"

    def apply_validation(
            self,
            data: base.types.ReadableType
    ) -> frictionless.Report:
        """Applies Frictionless validation for the 'survey_metadata.csv' template

        Args:
            data (base.types.ReadableType): Raw data to be validated

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct Resource (Table with Schema)
        resource = frictionless.Resource(
            source=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=self.schema(),
            onerror="ignore",   # Ignore errors, they will be handled in the report
        )

        # Validate
        report: frictionless.Report = resource.validate(
            checks=[
                # Extra Custom Checks
                plugins.tabular.IsTabular(),
                plugins.empty.NotEmpty(),
                plugins.chronological.ChronologicalOrder(
                    field_names=[
                        "temporalCoverageStartDate",
                        "temporalCoverageEndDate",
                    ]
                ),
            ],
            limit_memory=base.FRICTIONLESS_LIMIT_MEMORY,
        )

        # Return validation report
        return report

    def apply_mapping(
            self,
            data: base.types.ReadableType,
            chunk_size: Optional[int] = None,
            dataset_iri: Optional[rdflib.URIRef] = None,
            base_iri: Optional[rdflib.Namespace] = None
    ) -> Iterator[rdflib.Graph]:
        pass


base.mapper.ABISMapper.register_mapper(SurveyMetadataMapper)
