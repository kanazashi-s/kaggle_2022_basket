from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock
import utils


class EloRating(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "rating", "elo_rating")
        self.regular_final_rating = pd.DataFrame({
            "TeamID": [],
            "EloRating": [],
            "Season": [],
            "DayNum": [],
        })

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()
        input_without_duplicates = self.drop_duplicated(input_df)
        input_with_points_df = self.merge_result_points(input_without_duplicates)
        input_with_points_df = input_with_points_df.sort_values(by=["Season", "DayNum"])
        elo = utils.calc_elo.EloRatingCalculator()

        for idx, row in tqdm.tqdm(input_with_points_df.iterrows()):
            if row["ATeamID"] not in elo.teams:
                elo.add_new_team(row["ATeamID"], row["Season"], row["DayNum"])
            if row["BTeamID"] not in elo.teams:
                elo.add_new_team(row["BTeamID"], row["Season"], row["DayNum"])

            elo.update_season(row["ATeamID"], row["Season"], row["DayNum"])
            elo.update_season(row["BTeamID"], row["Season"], row["DayNum"])

            output_df = self.record_elo_rating(output_df, row, elo)

            new_a_rate, new_b_rate = elo.do_match(
                match=(row["ATeamID"], row["BTeamID"]),
                scores=(row["AScore"], row["BScore"]),
                season=row["Season"],
                daynum=row["DayNum"],
            )

            if row["data_from"] == "regular":
                self.save_regular_rating(row["ATeamID"], row["Season"], row["DayNum"], new_a_rate)
                self.save_regular_rating(row["BTeamID"], row["Season"], row["DayNum"], new_b_rate)

        output_df = output_df[["ATeamEloRating", "BTeamEloRating"]]
        output_df = self.calc_diff(output_df)

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
        output_df["DayNum"] = 136
        input_without_duplicates = self.drop_duplicated(output_df)
        input_with_points_df = self.merge_result_points(input_without_duplicates)
        input_with_points_df = input_with_points_df.sort_values(by=["Season", "DayNum"])
        elo = utils.calc_elo.EloRatingCalculator()

        for idx, row in tqdm.tqdm(input_with_points_df.iterrows()):
            season = row["Season"]
            elo.elo_rating_df = self.regular_final_rating.loc[
                self.regular_final_rating["Season"] == season
            ]

            if row["ATeamID"] not in elo.teams:
                elo.add_new_team(row["ATeamID"], row["Season"], row["DayNum"])
            if row["BTeamID"] not in elo.teams:
                elo.add_new_team(row["BTeamID"], row["Season"], row["DayNum"])

            elo.update_season(row["ATeamID"], row["Season"], row["DayNum"])
            elo.update_season(row["BTeamID"], row["Season"], row["DayNum"])

            output_df = self.record_elo_rating(output_df, row, elo)

        output_df = output_df[["ATeamEloRating", "BTeamEloRating"]]
        output_df = self.calc_diff(output_df)

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
        output_df.reset_index(drop=True, inplace=True)
        return output_df

    @staticmethod
    def merge_result_points(input_df):
        output_df = input_df.copy()

        output_df[["AScore", "BScore", "ALoc", "BLoc"]] = 0
        input_path = Path("data", "processed")
        compact_results = [
            "switched_regular_compact.csv",
            "switched_secondary_compact.csv",
            "switched_tourney_compact.csv",
        ]

        for file_name in compact_results:
            _df = pd.read_csv(input_path / file_name)
            scores_df = input_df.merge(
                _df[["ATeamID", "BTeamID", "Season", "DayNum", "AScore", "BScore", "ALoc", "BLoc"]],
                on=["ATeamID", "BTeamID", "Season", "DayNum"],
                how="left"
            )[["AScore", "BScore", "ALoc", "BLoc"]].fillna(0)
            output_df[["AScore", "BScore", "ALoc", "BLoc"]] += scores_df
        return output_df

    def record_elo_rating(self, input_df, row, elo):
        output_df = input_df.copy()

        if row["DayNum"] <= 135:
            a_elo_rating = elo.get_rating(team_id=row["ATeamID"])
            b_elo_rating = elo.get_rating(team_id=row["BTeamID"])
        else:
            a_elo_rating = self.regular_final_rating.loc[
                (self.regular_final_rating["TeamID"] == row["ATeamID"]) &
                (self.regular_final_rating["Season"] == row["Season"]),
            "EloRating"].squeeze()
            b_elo_rating = self.regular_final_rating.loc[
                (self.regular_final_rating["TeamID"] == row["BTeamID"]) &
                (self.regular_final_rating["Season"] == row["Season"]),
            "EloRating"].squeeze()

        # レートが常識的な範囲内かチェック
        assert 300 < a_elo_rating < 2700

        # home town advantage
        if row["ALoc"] == 1:
            a_elo_rating += 100
        elif row["BLoc"] == 1:
            b_elo_rating += 100

        output_df.loc[
            (output_df["Season"] == row["Season"]) &
            (output_df["ATeamID"] == row["ATeamID"]) &
            (output_df["DayNum"] == row["DayNum"]),
            "ATeamEloRating"
        ] = a_elo_rating
        output_df.loc[
            (output_df["Season"] == row["Season"]) &
            (output_df["BTeamID"] == row["ATeamID"]) &
            (output_df["DayNum"] == row["DayNum"]),
            "BTeamEloRating"
        ] = a_elo_rating

        output_df.loc[
            (output_df["Season"] == row["Season"]) &
            (output_df["ATeamID"] == row["BTeamID"]) &
            (output_df["DayNum"] == row["DayNum"]),
            "ATeamEloRating"
        ] = b_elo_rating
        output_df.loc[
            (output_df["Season"] == row["Season"]) &
            (output_df["BTeamID"] == row["BTeamID"]) &
            (output_df["DayNum"] == row["DayNum"]),
            "BTeamEloRating"
        ] = b_elo_rating
        return output_df

    def save_regular_rating(self, team_id, season, daynum, rating):
        new_row = pd.DataFrame({
            "TeamID": [team_id],
            "EloRating": [rating],
            "Season": [season],
            "DayNum": [daynum],
        })

        save_idx = (self.regular_final_rating["TeamID"] == team_id) & (self.regular_final_rating["Season"] == season)
        if save_idx.sum() == 0:
            self.regular_final_rating = pd.concat([
                self.regular_final_rating, new_row
            ])
        elif save_idx.sum() == 1:
            self.regular_final_rating.loc[save_idx] = new_row
        else:
            raise AssertionError

    @staticmethod
    def calc_diff(input_df):
        output_df = input_df.copy()
        output_df["EloRatingDiff"] = output_df["ATeamEloRating"] - output_df["BTeamEloRating"]
        output_df["AWinProba"] = 1 / (10 ** (-output_df["EloRatingDiff"]/400) + 1)
        return output_df