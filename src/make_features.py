import features

def main():
    # base_df (シーズン、チームAID、チームBIDの DataFrame )を読み込み
    train_base_df = features.read_base_df.read_train()
    test_base_df = features.read_base_df.read_test()

    # 学習に使用する特徴量を列挙
    feature_list = [
        features.seed.seed_num.SeedNumBlock(),
        features.results.regular_win_rate.RegularWinRate(),
    ]

    features.build_features(
        train_base_df,
        feature_list,
        is_test=False,
        is_create=True,
        is_overwrite=True
    )
    features.build_features(
        test_base_df,
        feature_list,
        is_test=True,
        is_create=True,
        is_overwrite=True
    )


if __name__ == "__main__":
    main()