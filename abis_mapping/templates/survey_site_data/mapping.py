"""Provides ABIS Mapper for `survey_site_data.csv` Template"""


# Local
from abis_mapping import base

# Third-party
import rdflib
import frictionless

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
