from utils.mlflow import MlflowWriter
from utils.cfg_yaml import load_config

import data.make_dataset
import features


def main():
    cfg = load_config('src/config/001.yaml')
    EXPERIMENT_NAME = 'kaggle_basket_first'
    writer = MlflowWriter(EXPERIMENT_NAME)

    # データセットの再生成
    if cfg['main']['create_data'] == True:
        data.make_dataset.main()

    # base_df (シーズン、チームAID、チームBIDの DataFrame )を読み込み
    train_base_df = features.read_base_df.read_train()
    test_base_df = features.read_base_df.read_test()

    # 学習に使用する特徴量を列挙
    feature_list = [
        features.seed.tmp.main,
        features.ranking.tmp.main
    ]

    train_features = features.build_features(train_base_df, feature_list, is_test=False, overwrite=False)
    test_features = features.build_features(test_base_df, feature_list, is_test=True, overwrite=False)

    # model, results = run_cv(train_features, cfg)
    # write_mlflow(writer, cfg, model, results)
    #
    # make_submission_csv(model, test_features, filename=f'{EXPERIMENT_NAME}.csv')
    # writer.set_terminated()


if __name__ == "__main__":
    main()
