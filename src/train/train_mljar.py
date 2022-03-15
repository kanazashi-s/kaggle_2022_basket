from supervised.automl import AutoML
from .cv import get_cv


def train_mljar(train_features, cfg):
    """
    Train a mljar model and save the artifacts.

    :param train_features: pd.DataFrame
    :param cfg: Dict of parameters
    :return:
        model: the trained model
        results: the path of result files
    """

    task = "regression" if cfg["main"]["is_reg"] else "binary_classification"
    automl = AutoML(
        ml_task=task,
        **cfg['mljar_params']
    )

    target_col = "PointsDiff" if cfg["main"]["is_reg"] else "is_AWin"

    X = train_features.drop([target_col, "Weights"], axis=1)
    y = train_features[target_col]
    weights = train_features["Weights"]

    cv = get_cv(cfg['cv']['cv_num'])
    automl.fit(X=X, y=y, sample_weight=weights, cv=cv,)

    return automl