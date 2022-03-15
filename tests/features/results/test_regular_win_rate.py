import pandas as pd
import features


def test_regular_win_rate_fit():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1207, 1246, 1246],
        "BTeamID": [1229, 1246, 1246, 1120, 1207],
        "DayNum": [20, 30, 40, 50, 60],
        "is_AWin": [1, 0, 1, 0, 1],
    })
    expected = pd.DataFrame({
        "ATeamWinRate": [None, None, None, 1, 0.5],
        "BTeamWinRate": [None, 1, 1, 0, 1],
        "TeamWinRateDiff": [None, None, None, 1, -0.5]
    })

    block = features.results.regular_win_rate.RegularWinRate()
    actual = block.fit(input_df, is_create=True)

    assert actual.equals(expected)


def test_regular_win_rate_transform(monkeypatch):
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1207],
        "BTeamID": [1229, 1246, 1120],
    })

    def patch_pd_read_csv(path):
        dummy_train_base = pd.DataFrame({
            "Season": [1985, 1985, 1985, 1985, 1985],
            "ATeamID": [1246, 1120, 1207, 1246, 1120],
            "BTeamID": [1229, 1246, 1246, 1120, 1207],
            "DayNum": [1, 2, 3, 4, 5],
            "data_from": ["regular", "regular", "regular", "regular", "ore"],
            "is_AWin": [1, 1, 1, 0, 0],
        })
        return dummy_train_base

    expected = pd.DataFrame({
        "ATeamWinRate": [0.5, 1, 1],
        "BTeamWinRate": [None, 0.5, 1],
        "TeamWinRateDiff": [None, 0.5, 0]
    })

    monkeypatch.setattr(
        "pandas.read_csv",
        patch_pd_read_csv,
    )

    block = features.results.regular_win_rate.RegularWinRate()
    actual = block.transform(input_df, is_create=True)

    assert actual.equals(expected)