import glob

import pandas as pd
import pandas_profiling as pdp


if __name__ == "__main__":

    raw_csv_list = glob.glob('data/raw/MDataFiles_Stage1/*.csv')

    error_list = []
    for raw_csv in raw_csv_list:
        csv_name = raw_csv.split('/')[-1][:-4]
        print(csv_name)

        try:
            df = pd.read_csv(raw_csv)
            minimal = True if len(df) > 100000 else False
            profile = pdp.ProfileReport(df, minimal=minimal)

            profile.to_file(f"reports/raw_pdp_outputs/raw_{csv_name}.html")
        except:
            error_list.append(csv_name)