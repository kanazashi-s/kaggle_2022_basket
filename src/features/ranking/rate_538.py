from pathlib import Path
import pandas as pd
from features.base import AbstractBaseBlock


class Rate538(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "ranking", "rate_538")

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()
        input_path = Path("data", "external")
        src_df = pd.read_csv(input_path / "538ratingsMen.csv")

        output_df = output_df.merge(
            src_df[["Season", "TeamID", "538rating"]],
            left_on=["Season", "ATeamID"],
            right_on=["Season", "TeamID"],
            how="left"
        )
        output_df = output_df.rename(columns={"538rating": "ATeamRate538"})

        output_df = output_df.merge(
            src_df[["Season", "TeamID", "538rating"]],
            left_on=["Season", "BTeamID"],
            right_on=["Season", "TeamID"],
            how="left"
        )
        output_df = output_df.rename(columns={"538rating": "BTeamRate538"})

        # 133日目までの試合結果を用いたランキングのため、133日目までの特徴量としては利用しない
        output_df.loc[
            output_df["DayNum"] <= 133,
            ["ATeamRate538", "BTeamRate538"]
        ] = None

        output_df = output_df[["ATeamRate538", "BTeamRate538"]]

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
        input_path = Path("data", "external")
        src_df = pd.read_csv(input_path / "538ratingsMen.csv")

        output_df = output_df.merge(
            src_df[["Season", "TeamID", "538rating"]],
            left_on=["Season", "ATeamID"],
            right_on=["Season", "TeamID"],
            how="left"
        )
        output_df = output_df.rename(columns={"538rating": "ATeamRate538"})

        output_df = output_df.merge(
            src_df[["Season", "TeamID", "538rating"]],
            left_on=["Season", "BTeamID"],
            right_on=["Season", "TeamID"],
            how="left"
        )
        output_df = output_df.rename(columns={"538rating": "BTeamRate538"})

        output_df = output_df[["ATeamRate538", "BTeamRate538"]]

        if is_overwrite:
            mode = "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df




