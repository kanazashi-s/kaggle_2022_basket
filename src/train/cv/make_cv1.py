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


if __name__ == "__main__":
    ret = make_cv1()
    print("end")