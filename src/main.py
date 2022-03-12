import os, shutil
import data.make_dataset
import features
from train import train_mljar
from predict import make_submission_csv
from utils.cfg_yaml import load_config
from utils.mlflow import MlflowWriter, write_mlflow


def main():
    cfg = load_config('src/config/001.yaml')
    EXPERIMENT_NAME = cfg["mljar_params"]["results_path"]
    writer = MlflowWriter(EXPERIMENT_NAME)

    if cfg["main"]["debug"] and os.path.exists(EXPERIMENT_NAME):
        shutil.rmtree(EXPERIMENT_NAME)

    # データセットの再生成
    if cfg['main']['create_data'] == True:
        data.make_dataset.main()

    # base_df (シーズン、チームAID、チームBIDの DataFrame )を読み込み
    train_base_df = features.read_base_df.read_train()
    test_base_df = features.read_base_df.read_test()

    # 学習に使用する特徴量を列挙
    feature_list = [
        features.meta.meta_features.MetaFeaturesBlock(),  # do not remove
        features.meta.train_weights.TrainWeights(),  # do not remove
        features.ranking.massey_avg.MasseyAvg(),
        features.ranking.rate_538.Rate538(),
        features.seed.seed_num.SeedNum(),
        features.results.regular_win_rate.RegularWinRate(),
        features.results.regular_point_avg.RegularPointAvg(),
    ]

    train_features = features.build_features(
        train_base_df,
        feature_list,
        is_test=False,
        is_create=cfg["main"]["feature_is_create"],
        is_overwrite=cfg["main"]["feature_is_overwrite"]
    )
    test_features = features.build_features(
        test_base_df,
        feature_list,
        is_test=True,
        is_create=cfg["main"]["feature_is_create"],
        is_overwrite=cfg["main"]["feature_is_overwrite"]
    )

    models = train_mljar(train_features, cfg)
    make_submission_csv(
        models,
        test_features,
        output_path=f'{EXPERIMENT_NAME}/submission.csv'
    )

    if not cfg['main']['debug']:
        write_mlflow(writer, cfg)
    writer.set_terminated()


if __name__ == "__main__":
    main()
