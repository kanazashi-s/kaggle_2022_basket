from pathlib import Path
import pandas as pd


def make_all():
    input_path = Path("data", "raw", "MDataFiles_Stage1")
    output_path = Path("data", "processed")

    in_out_dict = {
        'MNCAATourneyCompactResults.csv': 'switched_tourney_compact.csv',
        'MSecondaryTourneyCompactResults.csv': 'switched_secondary_compact.csv',
        'MRegularSeasonCompactResults.csv': 'switched_regular_compact.csv',
        'MNCAATourneyDetailedResults.csv': 'switched_tourney_detailed.csv',
        'MRegularSeasonDetailedResults.csv': 'switched_regular_detailed.csv',
    }

    for input_name, output_name in in_out_dict.items():
        input_df = pd.read_csv(input_path / input_name)
        # input_df = input_df.drop("WLoc", axis=1)

        df_1 = input_df.copy()

        df_1["ALoc"] = input_df["WLoc"].map({
            "H": 1,
            "N": 0,
            "A": -1,
        })
        df_1["BLoc"] = df_1["ALoc"] * -1
        df_1 = df_1.drop("WLoc", axis=1)

        df_1.columns = df_1.columns.str.replace('^W', 'A', regex=True)
        df_1.columns = df_1.columns.str.replace('^L', 'B', regex=True)
        df_1['is_AWin'] = 1

        df_2 = input_df.copy()
        df_2["ALoc"] = input_df["WLoc"].map({
            "H": -1,
            "N": 0,
            "A": 1,
        })
        df_2["BLoc"] = df_2["ALoc"] * -1
        df_2 = df_2.drop("WLoc", axis=1)
        df_2.columns = df_2.columns.str.replace('^W', 'B', regex=True)
        df_2.columns = df_2.columns.str.replace('^L', 'A', regex=True)
        df_2['is_AWin'] = 0

        output_df = pd.concat([df_1, df_2])
        output_df.to_csv(output_path / output_name, index=False)
