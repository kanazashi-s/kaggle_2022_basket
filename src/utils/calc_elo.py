import pandas as pd


class EloRatingCalculator:
    def __init__(self):
        self.elo_rating_df = pd.DataFrame({
            "TeamID": [],
            "EloRating": [],
            "Season": [],
            "DayNum": [],
        })

    def add_new_team(self):
        pass