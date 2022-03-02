import pandas as pd


class AbstractBaseBlock:
    def fit(self, input_df: pd.DataFrame):
        return self.transform(input_df)

    def transform(self,input_df: pd.DataFrame):
        raise NotImplementedError()