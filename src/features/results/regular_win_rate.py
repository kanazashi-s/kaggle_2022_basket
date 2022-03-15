from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock


class RegularWinRate(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "results", "regular_win_rate")

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()
        output_df["ATeamWinRate"] = 0

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_win_rate = input_df.loc[
                (input_df["Season"] == row["Season"]) &
                (input_df["DayNum"] < row["DayNum"]) &
                (input_df["ATeamID"] == row["ATeamID"]),
                "is_AWin"].mean()

            output_df.loc[idx, "ATeamWinRate"] = a_win_rate

            b_win_rate = input_df.loc[
                (input_df["Season"] == row["Season"]) &
                (input_df["DayNum"] < row["DayNum"]) &
                (input_df["ATeamID"] == row["BTeamID"]),
                "is_AWin"].mean()

            output_df.loc[idx, "BTeamWinRate"] = b_win_rate

        output_df["TeamWinRateDiff"] = output_df["ATeamWinRate"] - output_df["BTeamWinRate"]
        output_df = output_df[["ATeamWinRate", "BTeamWinRate", "TeamWinRateDiff"]]

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
        output_df["ATeamWinRate"] = 0
        train_base_df = pd.read_csv(Path("data", "processed", "train_base.csv"))

        for idx, row in tqdm.tqdm(input_df.iterrows()):

            a_win_rate = train_base_df.loc[
                (train_base_df["Season"] == row["Season"]) &
                (train_base_df["ATeamID"] == row["ATeamID"]) &
                (train_base_df["data_from"] == "regular"),
                "is_AWin"].mean()

            output_df.loc[idx, "ATeamWinRate"] = a_win_rate

            b_win_rate = train_base_df.loc[
                (train_base_df["Season"] == row["Season"]) &
                (train_base_df["ATeamID"] == row["BTeamID"]) &
                (train_base_df["data_from"] == "regular"),
                "is_AWin"].mean()

            output_df.loc[idx, "BTeamWinRate"] = b_win_rate

        output_df["TeamWinRateDiff"] = output_df["ATeamWinRate"] - output_df["BTeamWinRate"]
        output_df = output_df[["ATeamWinRate", "BTeamWinRate", "TeamWinRateDiff"]]

        if is_overwrite:
            mode = "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df




