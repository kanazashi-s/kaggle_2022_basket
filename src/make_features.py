import features


def main():
    # base_df (シーズン、チームAID、チームBIDの DataFrame )を読み込み
    train_base_df = features.read_base_df.read_train()
    test_base_df = features.read_base_df.read_test()

    feature_list = [
        features.meta.train_weights.TrainWeights(
            tourney_weight=1,
            year_weight_rate=0.05,
            year_weight_base=1.5
        ),  # do not remove
        # features.ranking.massey_avg.MasseyAvg(),
        # features.ranking.rate_538.Rate538(),
        features.seed.seed_num.SeedNum(),
        features.results.regular_win_rate.RegularWinRate(),
        features.results.regular_point_avg.RegularPointAvg(),
        features.ratings.elo_rating.EloRating(),
        features.actions.regular_actions_avg.RegularActionsAvg(),
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