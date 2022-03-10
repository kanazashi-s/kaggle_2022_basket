import pandas as pd
import features


def test_regular_point_avg_fit(monkeypatch):
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1229, 1229, 1246, 1246],
        "BTeamID": [1229, 1246, 1246, 1246, 1120, 1229],
        "DayNum": [20, 30, 40, 20, 30, 40],
        "is_AWin": [1, 1, 1, 0, 0, 0],
    })

    def patch_pd_read_csv(path):
        dummy_train_base = pd.DataFrame({
            "Season": [1985, 1985, 1985, 1985, 1985, 1985],
            "ATeamID": [1246, 1120, 1229, 1229, 1246, 1246],
            "BTeamID": [1229, 1246, 1246, 1246, 1120, 1229],
            "DayNum": [20, 30, 40, 20, 30, 40],
            "is_AWin": [1, 1, 1, 0, 0, 0],
            "AScore": [50, 30, 50, 0, 20, 10],
            "BScore": [0, 20, 10, 50, 30, 50],
        })
        return dummy_train_base

    expected = pd.DataFrame({
        "ATeamPointAvg": [None, None, 0, None, 50, 35],
        "BTeamPointAvg": [None, 50, 35, None, None, 0],
    })

    monkeypatch.setattr(
        "pandas.read_csv",
        patch_pd_read_csv,
    )

    block = features.results.regular_point_avg.RegularPointAvg()
    actual = block.fit(input_df, is_create=True)

    assert actual.equals(expected)


def test_regular_point_avg_transform(monkeypatch):
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1207],
        "BTeamID": [1229, 1246, 1120],
    })

    def patch_pd_read_csv(path):
        dummy_train_base = pd.DataFrame({
            "Season": [1985, 1985, 1985, 1985, 1985, 1985],
            "ATeamID": [1246, 1120, 1229, 1229, 1246, 1246],
            "BTeamID": [1229, 1246, 1246, 1246, 1120, 1229],
            "DayNum": [20, 30, 40, 20, 30, 40],
            "is_AWin": [1, 1, 1, 0, 0, 0],
            "AScore": [50, 30, 50, 0, 20, 20],
            "BScore": [0, 20, 20, 50, 30, 50],
        })
        return dummy_train_base

    expected = pd.DataFrame({
        "ATeamPointAvg": [30, 30, None],
        "BTeamPointAvg": [25, 30, 30],
    })

    monkeypatch.setattr(
        "pandas.read_csv",
        patch_pd_read_csv,
    )

    block = features.results.regular_point_avg.RegularPointAvg()
    actual = block.transform(input_df, is_create=True)

    assert actual.equals(expected)
