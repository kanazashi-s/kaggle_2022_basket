import pandas as pd
from pathlib import Path


def read_train():
    input_path = Path("data", "processed")
    train_base_df = pd.read_csv(input_path / "train_base.csv")
    return train_base_df


def read_test():
    input_path = Path("data", "processed")
    test_base_df = pd.read_csv(input_path / "test_base.csv")
    return test_base_df