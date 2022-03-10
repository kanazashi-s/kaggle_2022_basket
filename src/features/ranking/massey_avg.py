from pathlib import Path
import pandas as pd
import tqdm
from features.base import AbstractBaseBlock


class MasseyAvg(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "ranking", "massey_avg")

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        input_path = Path("data", "processed", "massey")
        massey_path_list = list(input_path.glob("*.csv"))
        output_df = pd.DataFrame()

        for path in massey_path_list:
            _df = self._calc_massey_avg_fit(input_df, path)
            output_df = pd.concat([output_df, _df], axis=1)

        if is_overwrite:
            mode = "fit"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df

    @staticmethod
    def _calc_massey_avg_fit(input_df, path):
        """
        input_df: train_base.csv
        path: path of one of the massey csv files.

        output_df: merged massey features.
        """
        output_df = input_df.copy()
        col_name = path.stem

        massey_df = pd.read_csv(path)
        print(f"Creating {col_name} features...")

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_ordinal = massey_df.loc[
                (massey_df["Season"] == row["Season"]) &
                (massey_df["RankingDayNum"] < row["DayNum"]) &
                (massey_df["TeamID"] == row["ATeamID"]),
            "OrdinalRank"].mean()

            output_df.loc[idx, f"AMasseyAvg{col_name}"] = a_ordinal

            b_ordinal = massey_df.loc[
                (massey_df["Season"] == row["Season"]) &
                (massey_df["RankingDayNum"] < row["DayNum"]) &
                (massey_df["TeamID"] == row["BTeamID"]),
            "OrdinalRank"].mean()

            output_df.loc[idx, f"BMasseyAvg{col_name}"] = b_ordinal

        return output_df[[f"AMasseyAvg{col_name}", f"BMasseyAvg{col_name}"]]

    def transform_create(
            self,
            input_df: pd.DataFrame,
            from_fit: bool = False,
            is_overwrite: bool = False,
    ):
        input_path = Path("data", "processed", "massey")
        massey_path_list = list(input_path.glob("*.csv"))
        output_df = pd.DataFrame()

        for path in massey_path_list:
            _df = self._calc_massey_avg_transform(input_df, path)
            output_df = pd.concat([output_df, _df], axis=1)

        if is_overwrite:
            mode = "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df

    @staticmethod
    def _calc_massey_avg_transform(input_df, path):
        """
        input_df: train_base.csv
        path: path of one of the massey csv files.

        output_df: merged massey features.
        """
        output_df = input_df.copy()
        col_name = path.stem

        massey_df = pd.read_csv(path)
        print(f"Creating {col_name} features...")

        for idx, row in tqdm.tqdm(input_df.iterrows()):
            a_ordinal = massey_df.loc[
                (massey_df["Season"] == row["Season"]) &
                (massey_df["TeamID"] == row["ATeamID"]),
                "OrdinalRank"].mean()

            output_df.loc[idx, f"AMasseyAvg{col_name}"] = a_ordinal

            b_ordinal = massey_df.loc[
                (massey_df["Season"] == row["Season"]) &
                (massey_df["TeamID"] == row["BTeamID"]),
                "OrdinalRank"].mean()

            output_df.loc[idx, f"BMasseyAvg{col_name}"] = b_ordinal

        return output_df[[f"AMasseyAvg{col_name}", f"BMasseyAvg{col_name}"]]



