import pandas as pd


def make_submission_csv(
        models,
        test_features,
        output_path,
):

    X = test_features
    preds = models.predict_proba(X)

    sub_df = pd.read_csv("data/processed/submission.csv")
    sub_df["Pred"] = preds[:, 1]
    sub_df.to_csv(output_path, index=False)