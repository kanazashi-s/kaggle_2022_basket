from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock


class RegularPointAvg(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "results", "regular_point_avg")

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()

        input_path = Path("data", "processed")
        src_df = pd.read_csv(input_path / "switched_regular_compact.csv")

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_point_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["DayNum"] < row["DayNum"]) &
                (src_df["ATeamID"] == row["ATeamID"]),
                "AScore"].mean()

            output_df.loc[idx, "ATeamPointAvg"] = a_point_avg

            b_point_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["DayNum"] < row["DayNum"]) &
                (src_df["ATeamID"] == row["BTeamID"]),
                "AScore"].mean()

            output_df.loc[idx, "BTeamPointAvg"] = b_point_avg

        output_df = output_df[["ATeamPointAvg", "BTeamPointAvg"]]

        if is_overwrite:
            mode = "fit"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df

    def transform_create(
            self,
            input_df: pd.DataFrame,
            from_fit: bool = False,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()
        output_df["ATeamPointAvg"] = 0
        output_df["BTeamPointAvg"] = 0

        input_path = Path("data", "processed")
        src_df = pd.read_csv(input_path / "switched_regular_compact.csv")

        for idx, row in tqdm.tqdm(input_df.iterrows()):

            a_point_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["ATeamID"] == row["ATeamID"]),
                "AScore"].mean()

            output_df.loc[idx, "ATeamPointAvg"] = a_point_avg

            b_point_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["ATeamID"] == row["BTeamID"]),
                "AScore"].mean()

            output_df.loc[idx, "BTeamPointAvg"] = b_point_avg

        output_df = output_df[["ATeamPointAvg", "BTeamPointAvg"]]

        if is_overwrite:
            mode = "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df




