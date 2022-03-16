import pickle
from typing import List
from pathlib import Path
import pandas as pd


def make_cv1():
    input_path = Path("data", "processed")
    base_df = pd.read_csv(input_path / "train_base.csv")

    test_years = [2016, 2017, 2018, 2019, 2021]
    cv = []
    for test_year in test_years:
        split_list = get_split_list(base_df, test_year)
        cv.append(split_list)

    return cv


def get_split_list(base_df, test_year) -> List[List]:
    """
    returns a cv element [[train_indices], [test_indices]].
    - train_indices:
        all data before test_year's March Madness
    - test_indices:
        test_year's March Madness
    """

    use_df = base_df[base_df["Season"] <= test_year]
    use_df = filter_ncaa_teams(use_df)

    train_indices = use_df[
        ~(
            (use_df["Season"] == test_year) &
            ((use_df["data_from"] == "tourney_cr") | (use_df["data_from"] == "secondary_tourney_cr"))
        )
    ].index

    test_indices = use_df[
        (use_df["Season"] == test_year) &
        (use_df["data_from"] == "tourney_cr")
    ].index

    return [train_indices, test_indices]


def get_ncaa_teams():
    input_path = Path("data", "raw", "MDataFiles_Stage1", "MNCAATourneySeeds.csv")
    seeds_df = pd.read_csv(input_path)
    teams_dict = {}
    for season in seeds_df["Season"].unique():
        teams = seeds_df.loc[seeds_df["Season"] == season, "TeamID"].unique().tolist()
        teams_dict[season] = teams

    return teams_dict


def filter_ncaa_teams(base_df):
    teams_dict = get_ncaa_teams()
    use_indices = []
    for season, teams in teams_dict.items():
        use_idx = base_df[
            (base_df["Season"] == season) &
            (base_df["ATeamID"].isin(teams)) &
            (base_df["BTeamID"].isin(teams))
        ].index.tolist()
        use_indices += use_idx

    return base_df.loc[use_indices]


if __name__ == "__main__":
    ret = make_cv1()
    with open("models/cv_list.pkl", "wb") as f:
        pickle.dump(ret, f)
    
    print("end")