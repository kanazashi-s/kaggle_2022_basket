from typing import List
import pandas as pd


def build_features(
        base_df: pd.DataFrame,
        feature_list: List,
        is_test: bool = False,
):
    out_df = pd.DataFrame()

    for block in feature_list:
        if is_test:
            out_i = block.transform(base_df)
        else:
            out_i = block.fit(base_df)

        out_df = pd.concat([out_df, out_i], axis=1)

    return out_df
