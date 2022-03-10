from typing import List
import pandas as pd


def build_features(
        base_df: pd.DataFrame,
        feature_list: List,
        is_test: bool = False,
        is_create: bool = False,
        is_overwrite: bool = False,
):
    out_df = pd.DataFrame()

    for block in feature_list:
        print(f"block: {block.__class__.__name__}, is_test: {is_test}")
        if is_test:
            out_i = block.transform(base_df, is_create=is_create, is_overwrite=is_overwrite)
        else:
            out_i = block.fit(base_df, is_create=is_create, is_overwrite=is_overwrite)
        assert len(base_df) == len(out_i) or len(out_i) == 0
        out_df = pd.concat([out_df, out_i], axis=1)

    return out_df
