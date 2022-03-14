from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock


class RegularActionsAvg(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "actions", "regular_actions_avg")

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()

        input_path = Path("data", "processed")
        src_df = pd.read_csv(input_path / "switched_regular_detailed.csv")
        a_features = ["AFGM", "AFGA", "AFGM3", "AFGA3", "AFTM", "AFTA",
                      "AOR", "ADR", "AAst", "ATO", "AStl", "ABlk", "APF"]
        b_features = ["BFGM", "BFGA", "BFGM3", "BFGA3", "BFTM", "BFTA",
                      "BOR", "BDR", "BAst", "BTO", "BStl", "BBlk", "BPF"]

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_actions_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["DayNum"] < row["DayNum"]) &
                (src_df["ATeamID"] == row["ATeamID"]),
                a_features].mean(axis=0)

            output_df.loc[idx, a_features] = a_actions_avg

            b_actions_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["DayNum"] < row["DayNum"]) &
                (src_df["ATeamID"] == row["BTeamID"]),
                b_features].mean(axis=0)

            output_df.loc[idx, b_features] = b_actions_avg

        output_df = output_df[a_features + b_features]

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

        input_path = Path("data", "processed")
        src_df = pd.read_csv(input_path / "switched_regular_detailed.csv")

        a_features = ["AFGM", "AFGA", "AFGM3", "AFGA3", "AFTM", "AFTA",
                      "AOR", "ADR", "AAst", "ATO", "AStl", "ABlk", "APF"]
        b_features = ["BFGM", "BFGA", "BFGM3", "BFGA3", "BFTM", "BFTA",
                      "BOR", "BDR", "BAst", "BTO", "BStl", "BBlk", "BPF"]

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_actions_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["ATeamID"] == row["ATeamID"]),
                a_features].mean(axis=0)

            output_df.loc[idx, a_features] = a_actions_avg

            b_actions_avg = src_df.loc[
                (src_df["Season"] == row["Season"]) &
                (src_df["ATeamID"] == row["BTeamID"]),
                b_features].mean(axis=0)

            output_df.loc[idx, b_features] = b_actions_avg

        output_df = output_df[a_features + b_features]

        if is_overwrite:
            mode = "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df




