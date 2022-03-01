from utils.mlflow import MlflowWriter
from utils.cfg_yaml import load_config


def main():
    cfg = load_config('src/config/001.yaml')
    EXPERIMENT_NAME = 'kaggle_basket_first'
    writer = MlflowWriter(EXPERIMENT_NAME)

    train_base_df = create_train_base_df.main()
    test_base_df = create_test_base_df.main()
    feature_list = [
        'use_feature_1',
        'use_feature_2',
        'use_feature_3'
    ]

    train_features = build_features(train_base_df, feature_list, is_test=False, overwrite=False)
    test_features = build_features(test_base_df, feature_list, is_test=True, overwrite=False)

    model, results = run_cv(train_features, cfg)
    write_mlflow(writer, cfg, model, results)

    make_submission_csv(model, test_features, filename=f'{EXPERIMENT_NAME}.csv')
    writer.set_terminated()


if __name__ == "__main__":
    main()
