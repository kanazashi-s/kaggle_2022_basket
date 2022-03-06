from pathlib import Path
import pandas as pd
from features.base import AbstractBaseBlock


class RegularWLRate(AbstractBaseBlock):
    def transform(self, input_df: pd.DataFrame):
        output_df = input_df.copy()

        input_path = Path("data", "raw", "MDataFiles_Stage1")
        regular_cr_df = pd.read_csv(input_path / "MRegularSeasonCompactResults.csv")


