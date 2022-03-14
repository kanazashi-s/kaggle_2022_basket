import pandas as pd


class EloRatingCalculator:
    def __init__(self):
        self.elo_rating_df = pd.DataFrame({
            "TeamID": [],
            "EloRating": [],
            "Season": [],
            "DayNum": [],
        })

    @property
    def teams(self):
        team_id_series = self.elo_rating_df["TeamID"]
        return team_id_series.tolist()

    def get_rating(self, team_id):
        return self.elo_rating_df.loc[
            self.elo_rating_df["TeamID"] == team_id,
            "EloRating"
        ].squeeze()

    def update_rating(self, team_id, new_rating, season, daynum):
        new_row = pd.DataFrame({
            "TeamID": [team_id],
            "EloRating": [new_rating],
            "Season": [season],
            "DayNum": [daynum],
        })

        self.elo_rating_df.loc[self.elo_rating_df["TeamID"] == team_id] = new_row
        assert self.elo_rating_df["TeamID"].is_unique

    def add_new_team(self, team_id, season, daynum):
        new_row = pd.DataFrame({
            "TeamID": [team_id],
            "EloRating": [1300],
            "Season": [season],
            "DayNum": [daynum],
        })
        self.elo_rating_df = pd.concat(
            [self.elo_rating_df, new_row]
        )
        assert self.elo_rating_df["TeamID"].is_unique

    def update_season(self, team_id, season, daynum):
        if self.elo_rating_df.loc[
            self.elo_rating_df["TeamID"] == team_id, "Season"
        ].squeeze() != season:

            new_rating = self.elo_rating_df.loc[
                self.elo_rating_df["TeamID"] == team_id, "EloRating"
            ] * 0.75 + 1505 * 0.25

            self.update_rating(team_id, new_rating, season, daynum)
            assert self.elo_rating_df["TeamID"].is_unique

    def do_match(self, match, scores, season, daynum):

        # シーズンが変わってないかチェック
        self.update_season(match[0], season, daynum)
        self.update_season(match[1], season, daynum)

        if scores[0] >= scores[1]:  # 引き分けは考えない
            win_idx = 0
            lose_idx = 1
        else:
            win_idx = 1
            lose_idx = 0
        
        a_rate = self.get_rating(match[0])
        b_rate = self.get_rating(match[1])
        
        a_e_value = self._calc_e_value(a_rate, b_rate)
        b_e_value = 1 - a_e_value
        
        k_value = self._calc_k_value((a_rate, b_rate), scores, win_idx, lose_idx)

        if win_idx == 0:
            a_s_value, b_s_value = 1, 0
        else:
            a_s_value, b_s_value = 0, 1

        new_a_rate = (k_value * (a_s_value - a_e_value) + a_rate)
        new_b_rate = (k_value * (b_s_value - b_e_value) + b_rate)

        self.update_rating(match[0], new_a_rate, season, daynum)
        self.update_rating(match[1], new_b_rate, season, daynum)

        return new_a_rate, new_b_rate
    
    @staticmethod
    def _calc_e_value(team_r, opp_r):
        rating_diff = opp_r - team_r
        return 1. / (1 + 10 ** (rating_diff/400.))
    
    @staticmethod
    def _calc_k_value(ratings, scores, win_idx, lose_idx):
        rating_diff = ratings[win_idx] - ratings[lose_idx]
        score_diff = scores[win_idx] - scores[lose_idx]

        numerator = 20 * (score_diff + 3) ** 0.8
        denominator = 7.5 + 0.006 * rating_diff

        return numerator / denominator
