from pathlib import Path
import pandas as pd


def save_regular_final_rating(input_df):
    input_regular_df = input_df.loc[
        input_df["data_from"] == "regular"
        ].reset_index(drop=True)

    a_input_regular_df = input_regular_df.loc[
                         :, ["Season", "DayNum", "ATeamID", "ATeamEloRating"]
                         ].rename(
        columns={"ATeamID": "TeamID", "ATeamEloRating": "TeamEloRating"}
    )

    b_input_regular_df = input_regular_df.loc[
                         :, ["Season", "DayNum", "BTeamID", "BTeamEloRating"]
                         ].rename(
        columns={"BTeamID": "TeamID", "BTeamEloRating": "TeamEloRating"}
    )

    concat_rating_df = pd.concat([
        a_input_regular_df, b_input_regular_df
    ]).sort_values(by=["Season", "DayNum"])

    season_last = concat_rating_df.drop_duplicates(
        subset=["TeamID", "Season"],
        keep="last"
    )



def make_input_df():
    output_df = pd.DataFrame({
        "ATeamID": [1120, 1120, 1230, 1240],
        "BTeamID": [1230, 1300, 1310, 1120],
        "ATeamEloRating": [10, 10, 20, 30],
        "BTeamEloRating": [15, 30, 15, 40],
        "Season": [2000, 2000, 2000, 2000],
        "DayNum": [30, 40, 50, 60],
        "data_from": ["regular", "regular", "regular", "regular"]
    })
    return output_df


if __name__ == "__main__":
    input_df = make_input_df()
    save_regular_final_rating(input_df)
