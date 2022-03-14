import pandas as pd
import features

block = features.ratings.elo_rating.EloRating()


def test_elo_rating_fit():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1985, 1985, 1985, 1986, 1986],
        "ATeamID": [1228, 1106, 1134, 1412, 1288, 1354, 1359, 1453],
        "BTeamID": [1328, 1354, 1464, 1228, 1354, 1126, 1116, 1274],
        "DayNum": [20, 25, 28, 26, 122, 129, 38, 42],
        "is_AWin": [1, 0, 1, 0, 1, 0, 1, 0],
        "data_from": ["regular", "regular", "regular", "regular", "tourney_cr", "tourney_cr", "regular", "regular"]
    })

    # block = features.ratings.elo_rating.EloRating()
    actual = block.fit(input_df, is_create=True)

    assert len(actual) == len(input_df)


def test_elo_rating_transform():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1986, 1986, 1986],
        "ATeamID": [1228, 1106, 1116, 1328, 1354, 1368],
        "BTeamID": [1328, 1354, 1368, 1228, 1106, 1116],
    })

    actual = block.transform(input_df, is_create=True)

    assert len(actual) == len(input_df)
