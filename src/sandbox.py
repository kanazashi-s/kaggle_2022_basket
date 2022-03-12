from pathlib import Path
import pandas as pd


def drop_duplicated(input_df):
    output_df = input_df.copy()
    output_df["TeamIDs"] = input_df[["ATeamID", "BTeamID"]].apply(
        lambda x: "_".join(x.sort_values().astype(str)), axis=1
    )
    output_df.drop_duplicates(subset=["Season", "DayNum", "TeamIDs"], inplace=True)
    return output_df


def merge_result_points(input_df):
    output_df = input_df.copy()
    output_df = output_df.merge(

    )


if __name__ == "__main__":
    train_base_df = pd.read_csv(Path("data", "processed", "train_base.csv"))
    out_df = drop_duplicated(train_base_df)