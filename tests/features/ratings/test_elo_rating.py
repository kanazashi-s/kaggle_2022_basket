import pandas as pd
import features

block = features.ratings.elo_rating.EloRating()


def test_elo_rating_fit():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1985, 1985, 1986, 1986, 1986],
        "ATeamID": [1228, 1106, 1116, 1328, 1228, 1354, 1368, 1328],
        "BTeamID": [1328, 1354, 1368, 1228, 1328, 1106, 1116, 1228],
        "DayNum": [20, 25, 30, 35, 135, 140, 20, 25],
        "is_AWin": [1, 0, 1, 0, 1, 0, 1, 0],
        "data_from": ["regular", "regular", "regular", "regular", "tourney_cr", "tourney_cr", "regular", "regular"]
    })

    # block = features.ratings.elo_rating.EloRating()
    actual = block.fit(input_df, is_create=True)

    assert len(actual) == len(input_df)


def test_regular_point_avg_transform():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1986, 1986, 1986],
        "ATeamID": [1228, 1106, 1116, 1328, 1354, 1368],
        "BTeamID": [1328, 1354, 1368, 1228, 1106, 1116],
    })

    actual = block.transform(input_df, is_create=True)

    assert len(actual) == len(input_df)
