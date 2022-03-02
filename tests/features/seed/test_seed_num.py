import pandas as pd
import features


def test_seed_num():
    input_df = pd.DataFrame({
        "Season": [1985, 1985, 1985],
        "ATeamID": [1116, 1120, 1207],
        "BTeamID": [1229, 1242, 1246],
    })
    expected = pd.DataFrame({
        "ASeed": [9, 11, 1],
        "BSeed": [9, 3, 12],
    })

    block = features.seed.seed_num.SeedNumBlock()
    actual = block.transform(input_df)

    assert actual.equals(expected)
