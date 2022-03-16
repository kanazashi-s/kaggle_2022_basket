import pickle
import lightgbm as lgbm
from sklearn.metrics import log_loss


def main():
    with open("reports/AutoML_Elo1/train_features.pkl", "rb") as f:
        train_features = pickle.load(f)

    with open("reports/AutoML_Elo1/test_features.pkl", "rb") as f:
        test_features = pickle.load(f)

    with open("models/cv_list.pkl", "rb") as f:
        cv_list = pickle.load(f)

    target_col = "is_AWin"
    weight_col = "Weights"
    scores = []
    for train_idx, valid_idx in cv_list:
        train_df, valid_df = train_features.loc[train_idx], train_features.loc[valid_idx]
        train_X, train_y, train_weights = train_df.drop([target_col, weight_col], axis=1), train_df[target_col], train_df[weight_col]
        valid_X, valid_y, valid_weights = valid_df.drop([target_col, weight_col], axis=1), valid_df[target_col], valid_df[weight_col]

        model = lgbm.LGBMClassifier(objective='binary')
        model.fit(
            X=train_X,
            y=train_y,
            sample_weight=train_weights,
            eval_set=(valid_X, valid_y),
        )

        pred_i = model.predict_proba(valid_X)[:, 1]
        score = log_loss(valid_y, pred_i, sample_weight=valid_weights)
        scores.append(score)

    print(sum(scores) / len(scores))


if __name__ == "__main__":
    main()