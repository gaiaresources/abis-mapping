"""Provides csv utilities for the package"""


# Third-Party
import pandas as pd

# Local
from abis_mapping.base import types


def read_csv(data: types.CSVType) -> pd.DataFrame:
    """Reads raw csv data into a pandas DataFrame

    Args:
        data (types.CSVType): Pandas readable CSV type.

    Returns:
        pd.DataFrame: Pandas DataFrame containing CSV data.
    """
    # Read CSV and Return
    return pd.read_csv(data, keep_default_na=False)
