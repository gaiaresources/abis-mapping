"""Provides ABIS Mapper for `dwc_mvp` Template"""


# Third-Party
import rdflib

# Local
from abis_mapping import base


class DWCMVPMapper(base.ABISMapper):
    """ABIS Mapper for `dwc_mvp"""

    def apply_mapping(self, data: base.CSVType) -> rdflib.Graph:
        """Applies Mapping for the `dwc_mvp` Template

        Args:
            data (base.CSVType): Raw pandas readable csv data to be mapped

        Returns:
            rdflib.Graph: ABIS conformant rdf mapped from the csv
        """
        # TODO -> Implement
        raise NotImplementedError


# Register Mapper
base.ABISMapper.register_mapper(DWCMVPMapper, "dwc_mvp.xlsx")
