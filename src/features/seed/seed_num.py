from pathlib import Path
import pandas as pd
from features.base import AbstractBaseBlock


class SeedNumBlock(AbstractBaseBlock):
    def transform(self, input_df: pd.DataFrame):
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

        return output_df[["ASeed", "BSeed"]]
