## Project structure
- Note: Before running these scripts, you must create `data` directory and put raw datasets as shown below.

```
    ~/py/kaggle/basket_2022 ❯ tree -h                                                                          zaccey@zaccey-dev   08:47:42
.
|-- [4.0K]  data
|   |-- [4.0K]  external
|   |-- [4.0K]  interim
|   |-- [4.0K]  processed
|   `-- [4.0K]  raw
|       |-- [4.0K]  MDataFiles_Stage1
|       |   |-- [8.7K]  Cities.csv
|       |   |-- [1.6K]  Conferences.csv
|       |   |-- [144K]  MConferenceTourneyGames.csv
|       |   |-- [2.1M]  MGameCities.csv
|       |   |-- [ 95M]  MMasseyOrdinals.csv
|       |   |-- [ 68K]  MNCAATourneyCompactResults.csv
|       |   |-- [115K]  MNCAATourneyDetailedResults.csv
|       |   |-- [ 14K]  MNCAATourneySeedRoundSlots.csv
|       |   |-- [ 35K]  MNCAATourneySeeds.csv
|       |   |-- [ 45K]  MNCAATourneySlots.csv
|       |   |-- [4.9M]  MRegularSeasonCompactResults.csv
|       |   |-- [9.5M]  MRegularSeasonDetailedResults.csv
|       |   |-- [222K]  MSampleSubmissionStage1.csv
|       |   |-- [2.0K]  MSeasons.csv
|       |   |-- [ 55K]  MSecondaryTourneyCompactResults.csv
|       |   |-- [ 24K]  MSecondaryTourneyTeams.csv
|       |   |-- [362K]  MTeamCoaches.csv
|       |   |-- [207K]  MTeamConferences.csv
|       |   |-- [9.6K]  MTeams.csv
|       |   `-- [ 22K]  MTeamSpellings.csv
|       `-- [ 23M]  mens-march-mania-2022.zip
|-- [ 165]  Dockerfile
|-- [4.0K]  mlflow_docker
|   |-- [ 263]  docker-compose.yaml
|   |-- [ 135]  Dockerfile
|   |-- [  65]  Readme.md
|   `-- [   6]  requirements.txt
|-- [4.0K]  mlruns
|-- [4.0K]  models
|-- [4.0K]  notebooks
|   |-- [381K]  initial_submission.csv
|   `-- [5.1K]  initial_submission.ipynb
|-- [2.4K]  README.md
|-- [4.0K]  references
|-- [4.0K]  reports
|   `-- [4.0K]  raw_pdp_outputs
|       |-- [4.0K]  mncaa_tourney_detailed_results
|       |-- [554K]  raw_Cities.html
|       |-- [430K]  raw_Conferences.html
|       |-- [1.4M]  raw_MConferenceTourneyGames.html
|       |-- [2.0M]  raw_MGameCities.html
|       |-- [2.6M]  raw_MNCAATourneyCompactResults.html
|       |-- [ 48M]  raw_MNCAATourneyDetailedResults.html
|       |-- [1.4M]  raw_MNCAATourneySeedRoundSlots.html
|       |-- [739K]  raw_MNCAATourneySeeds.html
|       |-- [608K]  raw_MNCAATourneySlots.html
|       |-- [431K]  raw_MSampleSubmissionStage1.html
|       |-- [772K]  raw_MSeasons.html
|       |-- [2.7M]  raw_MSecondaryTourneyCompactResults.html
|       |-- [755K]  raw_MSecondaryTourneyTeams.html
|       |-- [1.5M]  raw_MTeamCoaches.html
|       |-- [749K]  raw_MTeamConferences.html
|       |-- [1.1M]  raw_MTeams.html
|       `-- [ 48M]  test.html
|-- [ 115]  requirements.txt
`-- [4.0K]  src
    |-- [4.0K]  config
    |   `-- [ 453]  001.yaml
    |-- [4.0K]  data
    |   |-- [   0]  __init__.py
    |   |-- [1.4K]  make_dataset.py
    |   `-- [ 261]  unzip_raw_data.py
    |-- [4.0K]  features
    |   |-- [   0]  base.py
    |   |-- [   0]  build_features.py
    |   |-- [   0]  manage_memo.py
    |   `-- [4.0K]  mncaa_tourney_detailed_results
    |-- [   0]  __init__.py
    |-- [ 857]  main.py
    |-- [4.0K]  models
    |   `-- [   0]  __init__.py
    `-- [4.0K]  utils
        |-- [  98]  cfg_yaml.py
        |-- [   0]  __init__.py
        |-- [ 587]  make_pdp_report.py
        |-- [1.0K]  mlflow.py
        |-- [4.0K]  __pycache__
        |   `-- [ 308]  yaml.cpython-38.pyc
        `-- [  98]  yaml.py

22 directories, 63 files
```