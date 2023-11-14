"""Provides ABIS Mapper for `survey_site_data.csv` Template"""


# Local
from abis_mapping import base
from abis_mapping import plugins

# Third-party
import rdflib
import frictionless

# Typing
from typing import Any, Optional, Iterator

# Default Dataset Metadata
DATASET_DEFAULT_NAME = "Example Systematic Survey Site Dataset"
DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Site Dataset by Gaia Resources"


# Constants and shortcuts
a = rdflib.RDF.type


class SurveySiteMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `survey_site_data.csv`"""

    # Template ID and Instructions File
    template_id = "survey_site_data.csv"
    instructions_file = "instructions.pdf"

    def apply_validation(
        self,
        data: base.types.ReadableType,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `survey_site_data.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct resource
        resource = frictionless.Resource(
            data=data,
            format="csv",
            schema=schema,
        )

        # Validate
        report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra custom checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=[
                            "decimalLatitude",
                            "decimalLongitude",
                        ]
                    ),
                    plugins.logical_or.LogicalOr(
                        field_names=[
                            "footprintWKT",
                            "decimalLatitude",
                        ]
                    ),
                    plugins.chronological.ChronologicalOrder(
                        field_names=[
                            "siteVisitStart",
                            "siteVisitEnd"
                        ]
                    )
                ],
                skip_errors=self.skip_errors,
            )
        )

        # Return validation report
        return report

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping for the `survey_site_data.csv` Template

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.

        Keyword Args:
            chunk_size (Optional[int]): How many rows of the original data to
                ingest before yielding a graph. `None` will ingest all rows.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """
        pass


# Register Mapper
base.mapper.ABISMapper.register_mapper(SurveySiteMapper)
