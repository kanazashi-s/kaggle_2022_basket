from pathlib import Path
import os
import pandas as pd


def make_all():
    input_file = Path("data", "raw", "MDataFiles_Stage1", "MMasseyOrdinals.csv")
    output_path = Path("data", "processed", "massey")
    os.makedirs(output_path, exist_ok=True)

    massey_whole_df = pd.read_csv(input_file)
    use_systems_list = get_use_systems(massey_whole_df)

    for system in use_systems_list:
        output_df = massey_whole_df[massey_whole_df["SystemName"] == system]
        output_df.to_csv(output_path / f"{system}.csv", index=False)
        print(f"File {system}.csv was saved.")


def get_use_systems(massey_whole_df):
    system_vc_after2021 = massey_whole_df[massey_whole_df["Season"] >= 2021].value_counts("SystemName")
    use_systems_list = system_vc_after2021[:20].index.tolist()
    return use_systems_list


if __name__ == "__main__":
    make_all()