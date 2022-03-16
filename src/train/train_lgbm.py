from supervised.automl import AutoML
from .cv import get_cv
import lightgbm as lgbm


def train_lgbm(train_features, cfg):
    """
    Train a lgbm model and save the artifacts.

    :param train_features: pd.DataFrame
    :param cfg: Dict of parameters
    :return:
        model: the trained models
        results: the path of result files
    """

    target_col = "is_AWin"
    weight_col = "Weights"

    X = train_features.drop([target_col, "Weights"], axis=1)
    y = train_features[target_col]
    w = train_features[weight_col]

    cv = get_cv(cfg['cv']['cv_num'])

    models = []
    for train_idx, valid_idx in cv:
        train_X, valid_X = X.loc[train_idx], X.loc[valid_idx]
        train_y, valid_y = y.loc[train_idx], y.loc[valid_idx]
        train_w, valid_w = w.loc[train_idx], w.loc[valid_idx]

        model = lgbm.LGBMClassifier(objective='binary')
        model.fit(
            X=train_X,
            y=train_y,
            sample_weight=train_w,
            eval_set=(valid_X, valid_y),
            eval_sample_weight=valid_w
        )

        models.append(model)

    return models

