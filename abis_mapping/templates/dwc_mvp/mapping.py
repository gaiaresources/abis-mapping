"""Provides ABIS Mapper for `dwc_mvp.xlsx` Template"""


# Third-Party
import pandas as pd
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

    def apply_mapping_row(
        self,
        row: pd.Series,
        row_number: int,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        ) -> rdflib.Graph:
        """Applies Mapping for a Row in the `dwc_mvp.xlsx` Template

        Args:
            row (pd.Series): Row to be processed in the dataset.
            row_number (int): Row number to be processed.
            dataset (rdflib.URIRef): Dataset uri this row is apart of.
            graph (rdflib.Graph): Graph to map row into.

        Returns:
            rdflib.Graph: Graph with row mapped into it.
        """
        # TODO -> Implement
        raise NotImplementedError


# Register Mapper
base.mapper.ABISMapper.register_mapper(DWCMVPMapper, "dwc_mvp.xlsx")
