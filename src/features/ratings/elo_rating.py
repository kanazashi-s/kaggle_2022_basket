from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock
import utils


class EloRating(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "rating", "elo_rating")
        self.regular_final_elo = pd.DataFrame({
            "TeamID": [],
            "EloRating": [],
        })

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()
        input_without_duplicates = self.drop_duplicated(input_df)
        input_with_points_df = self.merge_result_points(input_without_duplicates)
        elo = utils.calc_elo.EloRatingCalculator()

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            if row["ATeamID"] not in elo.elo_rating_df["TeamID"]:
                elo.add_new_team()


            if this_season_early_days_df["ATeamEloRating"].isnull().all():  # もしelo_rateが計算されたものがなかったら
                last_season_elo_rate = output_df.loc[
                    (input_with_points_df["Season"] == row["Season"] - 1)
                ][-1, "ATeamEloRating"]
                
            else:
                最新のelo_rate持ってきて、計算する


        # input_path = Path("data", "processed")
        # src_df = pd.read_csv(input_path / "switched_regular_compact.csv")

        # for idx, row in tqdm.tqdm(input_df.iterrows()):
        #     a_point_avg = src_df.loc[
        #         (src_df["Season"] == row["Season"]) &
        #         (src_df["DayNum"] < row["DayNum"]) &
        #         (src_df["ATeamID"] == row["ATeamID"]),
        #         "AScore"].mean()
        #
        #     output_df.loc[idx, "ATeamPointAvg"] = a_point_avg
        #
        #     b_point_avg = src_df.loc[
        #         (src_df["Season"] == row["Season"]) &
        #         (src_df["DayNum"] < row["DayNum"]) &
        #         (src_df["ATeamID"] == row["BTeamID"]),
        #         "AScore"].mean()
        #
        #     output_df.loc[idx, "BTeamPointAvg"] = b_point_avg
        #
        # output_df = output_df[["ATeamPointAvg", "BTeamPointAvg"]]

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

    @staticmethod
    def drop_duplicated(input_df):
        output_df = input_df.copy()
        output_df["TeamIDs"] = input_df[["ATeamID", "BTeamID"]].apply(
            lambda x: "_".join(x.sort_values().astype(str)), axis=1
        )
        output_df.drop_duplicates(subset=["Season", "DayNum", "TeamIDs"], inplace=True)
        return output_df


    @staticmethod
    def merge_result_points(input_df):
        return input_df




