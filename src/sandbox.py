from typing import List
from pathlib import Path
import pandas as pd


def main():
    input_path = Path("features")
    my_elo_ratings = pd.read_csv(input_path / "rating" / "elo_rating" / "transform.csv")
    elo_538 = pd.read_csv(input_path / "ranking" / "rate_538" / "transform.csv")

    my_elo_ratings["is_AWin"] = my_elo_ratings["ATeamEloRating"] >= my_elo_ratings["BTeamEloRating"]
    elo_538["is_AWin"] = elo_538["ATeamRate538"] >= elo_538["BTeamRate538"]
    (my_elo_ratings["is_AWin"] == elo_538["is_AWin"]).sum()


if __name__ == "__main__":
    main()