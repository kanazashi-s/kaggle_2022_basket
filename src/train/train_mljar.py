from supervised.automl import AutoML
from cv import get_cv


def train_mljar(train_features, cfg):
    """
    Train a mljar model and save the artifacts.

    :param train_features: pd.DataFrame
    :param cfg: Dict of parameters
    :return:
        model: the best model
        results: the path of result files
    """

    automl = AutoML(
        results_path="reports",
        ml_task="binary_classification",
        **cfg['mljar_params']
    )

    no_use_cols = [
        "ATeamID",
        "BTeamID",
        "Season",
        "data_from",
        "is_AWin",
    ]
    X = train_features.drop(no_use_cols, axis=1)
    y = train_features["is_AWin"]

    cv = get_cv(cfg['cv']['cv_num'])
    automl.fit(X, y, cv=cv,)

    predictions = automl.predict(test_df)
    print(predictions)