"""Provides ABIS Mapper for `dwc_mvp.xlsx` Template"""


# Third-Party
import rdflib

# Local
from abis_mapping import base


class DWCMVPMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `dwc_mvp.xlsx`"""

    def apply_mapping(
        self,
        data: base.types.CSVType,
        metadata: base.metadata.DatasetMetadata,
        ) -> rdflib.Graph:
        """Applies Mapping for the `dwc_mvp.xlsx` Template

        Args:
            data (base.types.CSVType): Raw pandas csv data to be mapped
            metadata (base.metadata.DatasetMetadata): Metadata for dataset

        Returns:
            rdflib.Graph: ABIS conformant rdf mapped from the csv
        """
        # TODO -> Implement
        raise NotImplementedError


# Register Mapper
base.mapper.ABISMapper.register_mapper(DWCMVPMapper, "dwc_mvp.xlsx")
