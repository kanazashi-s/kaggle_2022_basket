import pandas as pd
import features


def test_regular_point_avg_fit():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985, 1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1229, 1229, 1246, 1246],
        "BTeamID": [1229, 1246, 1246, 1246, 1120, 1229],
        "DayNum": [20, 30, 40, 20, 30, 40],
        "is_AWin": [1, 1, 1, 0, 0, 0],
    })

    block = features.actions.regular_actions_avg.RegularActionsAvg()
    actual = block.fit(input_df, is_create=True)

    assert True


def test_regular_point_avg_transform():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985],
        "ATeamID": [1246, 1120, 1207],
        "BTeamID": [1229, 1246, 1120],
    })

    block = features.actions.regular_actions_avg.RegularActionsAvg()
    actual = block.transform(input_df, is_create=True)

    assert True
