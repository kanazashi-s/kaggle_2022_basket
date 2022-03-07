from pathlib import Path
import pandas as pd
from features.base import AbstractBaseBlock


class SeedNumBlock(AbstractBaseBlock):
    def __init__(self):
        self.feature_path = Path("features", "seed", "seed_num")

    def transform_create(
            self,
            input_df: pd.DataFrame,
            from_fit: bool = False,
            is_overwrite: bool = False,
    ):
        output_df = input_df.copy()

        input_path = Path("data", "raw", "MDataFiles_Stage1")
        df_seeds = pd.read_csv(input_path / "MNCAATourneySeeds.csv")
        df_seeds["Seed"] = df_seeds["Seed"].str[1:3].astype(int)

        output_df = pd.merge(
            output_df,
            df_seeds.rename(columns={"TeamID": "ATeamID", "Seed": "ASeed"}),
            on=["Season", "ATeamID"],
            how="left"
        )

        output_df = pd.merge(
            output_df,
            df_seeds.rename(columns={"TeamID": "BTeamID", "Seed": "BSeed"}),
            on=["Season", "BTeamID"],
            how="left"
        )

        output_df["Seed_diff"] = output_df["ASeed"] - output_df["BSeed"]
        output_df = output_df[["ASeed", "BSeed", "Seed_diff"]]

        if is_overwrite:
            mode = "fit" if from_fit else "transform"
            self.save_feature_csv(output_df, self.feature_path, mode=mode)

        return output_df
