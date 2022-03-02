from pathlib import Path
import pandas as pd


def make_train():
    input_path = Path("data", "raw", "MDataFiles_Stage1")
    output_path = Path("data", "processed")
    cols = ['Season', 'DayNum', 'WTeamID', 'LTeamID']

    use_csv_dict = {
        'tourney_cr': 'MNCAATourneyCompactResults.csv',
        'secondary_tourney_cr': 'MSecondaryTourneyCompactResults.csv',
        'regular': 'MRegularSeasonCompactResults.csv',
    }

    ret_df = pd.DataFrame()

    for name, file in use_csv_dict.items():
        file_path = input_path / file
        _df = pd.read_csv(file_path)[cols]
        _df['data_from'] = name

        _df1 = _df.rename({
            'WTeamID': 'ATeamID',
            'LTeamID': 'BTeamID',
        })
        _df1['is_AWin'] = 1

        _df2 = _df.rename({
            'WTeamID': 'BTeamID',
            'LTeamID': 'ATeamID',
        })
        _df2['is_AWin'] = 0

        base_df = pd.concat([_df1, _df2])
        ret_df = pd.concat([ret_df, base_df])

    ret_df.to_csv(output_path / "train_base.csv", index=False)


def make_test():
    input_path = Path("data", "raw", "MDataFiles_Stage1")
    output_path = Path("data", "processed")
    s_sub_df = pd.read_csv(input_path / "MSampleSubmissionStage1.csv")
    sub_df = s_sub_df['ID'].str.split(pat='_', expand=True).astype(int)
    sub_df.columns = ['Season', 'ATeamID', 'BTeamID']

    sub_df.to_csv(output_path / "test_base.csv", index=False)


if __name__ == "__main__":
    make_train()
    make_test()
