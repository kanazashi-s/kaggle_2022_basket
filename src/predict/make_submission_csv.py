import pandas as pd


def make_submission_csv(
        models,
        test_features,
        output_path,
):
    no_use_cols = [
        "ATeamID",
        "BTeamID",
        "Season",
    ]

    X = test_features.drop(no_use_cols, axis=1)
    preds = models.predict_proba(X)

    sub_df = pd.read_csv("data/processed/submission.csv")
    sub_df["Pred"] = preds
    sub_df.to_csv(output_path, index=False)