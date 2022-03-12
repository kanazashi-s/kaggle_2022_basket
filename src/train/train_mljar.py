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

    automl = AutoML(
        ml_task="binary_classification",
        **cfg['mljar_params']
    )

    X = train_features.drop(["is_AWin", "Weights"], axis=1)
    y = train_features["is_AWin"]
    weights = train_features["Weights"]

    cv = get_cv(cfg['cv']['cv_num'])
    automl.fit(X=X, y=y, sample_weight=weights, cv=cv,)

    return automl