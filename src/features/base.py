import os
from pathlib import Path
import pandas as pd


class AbstractBaseBlock:
    def __init__(self):
        self.feature_path = None

    def fit(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False
    ):
        """
        train_features にマージする特徴量を生成するブロック
        1. if is_overwrite:
            1.a. 作成して返す
        2. else:
            2.a. セーブされたfit特徴量を読み込んでそのまま返す
        """

        if is_create:
            feature_df = self.fit_create(input_df, is_overwrite=is_overwrite)
        else:
            feature_df = self.read_feature_csv(self.feature_path, mode="fit")

        assert len(input_df) == len(feature_df)
        return feature_df

    def fit_create(
            self,
            input_df: pd.DataFrame,
            is_overwrite: bool = False,
    ):
        return self.transform_create(input_df, from_fit=True, is_overwrite=is_overwrite)

    def transform(
            self,
            input_df: pd.DataFrame,
            is_create: bool = False,
            is_overwrite: bool = False,
    ):
        """
        test_features にマージする特徴量を生成するブロック
        1. if is_overwrite:
            1.a. 作成して返す
        2. else:
            2.a. セーブされたfit特徴量を読み込んでそのまま返す
        """

        if is_create:
            feature_df = self.transform_create(input_df, is_overwrite=is_overwrite)
        else:
            feature_df = self.read_feature_csv(self.feature_path, mode="transform")

        assert len(input_df) == len(feature_df)
        return feature_df

    def transform_create(
            self,
            input_df: pd.DataFrame,
            from_fit: bool = False,
            is_overwrite: bool = False,
    ):
        raise NotImplementedError

    @staticmethod
    def read_feature_csv(feature_path: Path, mode: str = "fit"):
        if mode not in ["fit", "transform"]:
            raise ValueError("mode is not in ['fit', 'transform'].")

        file_path = feature_path / f"{mode}.csv"
        if os.path.isfile(file_path):
            return pd.read_csv(file_path)
        else:
            raise FileNotFoundError(f"The feature csv {file_path} was not found.")

    @staticmethod
    def save_feature_csv(save_df: pd.DataFrame, feature_path: Path, mode: str = "fit"):
        if mode not in ["fit", "transform"]:
            raise ValueError("mode is not in ['fit', 'transform'].")

        os.makedirs(feature_path, exist_ok=True)
        file_path = feature_path / f"{mode}.csv"
        save_df.to_csv(file_path, index=False)
