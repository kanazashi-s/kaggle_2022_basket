import pandas as pd
from features.base import AbstractBaseBlock


class TrainWeights(AbstractBaseBlock):
    def __init__(
            self,
            tourney_weight: int = 1,
            year_weight_rate: float = 0.05,
            year_weight_base: float = 1.5,
    ):
        self.tourney_weight = tourney_weight
        self.year_weight_rate = year_weight_rate
        self.year_weight_base = year_weight_base

    def fit(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False,
    ):

        category_weights = input_df["data_from"].map({
            "tourney_cr": self.tourney_weight,
            "regular": 1,
            "secondary_tourney_cr": 2
        })
        year_weights = input_df["Season"].apply(
            lambda x: max(0, (x - 2010) * self.year_weight_rate + self.year_weight_base)
        )

        weights = (category_weights * year_weights).rename("Weights")
        return weights

    def transform(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False,
    ):
        return pd.DataFrame()