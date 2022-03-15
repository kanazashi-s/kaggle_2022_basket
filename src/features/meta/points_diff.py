from pathlib import Path
import pandas as pd
from features.base import AbstractBaseBlock


class PointsDiff(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "meta", "points_diff")

    def fit(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()

        output_df = self.merge_result_points(output_df)
        output_df["PointsDiff"] = output_df["AScore"] - output_df["BScore"]

        return output_df[["PointsDiff"]]

    def transform(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False,
    ):
        return pd.DataFrame()

    @staticmethod
    def merge_result_points(input_df):
        output_df = input_df.copy()

        output_df[["AScore", "BScore"]] = 0
        input_path = Path("data", "processed")
        compact_results = [
            "switched_regular_compact.csv",
            "switched_secondary_compact.csv",
            "switched_tourney_compact.csv",
        ]

        for file_name in compact_results:
            _df = pd.read_csv(input_path / file_name)
            scores_df = input_df.merge(
                _df[["ATeamID", "BTeamID", "Season", "DayNum", "AScore", "BScore"]],
                on=["ATeamID", "BTeamID", "Season", "DayNum"],
                how="left"
            )[["AScore", "BScore"]].fillna(0)
            output_df[["AScore", "BScore"]] += scores_df
        return output_df



