import pandas as pd
from features.base import AbstractBaseBlock


class MetaFeaturesBlock(AbstractBaseBlock):
    """
    Features that must be added to execute training and testing.
    - For training:
        - target_col(is_AWin)
    - For testing:
        - None (currently...)
    """

    def fit(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False
    ):
        return input_df["is_AWin"]

    def transform(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        return pd.DataFrame()