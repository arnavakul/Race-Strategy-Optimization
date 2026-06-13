import os
import pickle
import pandas as pd
import json

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

CLEAN_LAPS_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "R",
    "clean_laps"
)

DEG_MODEL_PATH = os.path.join(
    BASE_DIR,
    "api",
    "models",
    "saved_models",
    "all_tracks_degradation.pkl"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "strategy_type_dataset.parquet"
)

#Team Strength Ratigs
TEAM_STRENGTH_PATH = os.path.join(
    BASE_DIR,
    "data",
    "team_strength",
    "team_strength.parquet"
)

#Driver Track Ratings
DRIVER_RATING_PATH = os.path.join(
    BASE_DIR,
    "data",
    "driver_ratings",
    "driver_track_ratings.parquet"
)

def get_strategy_type(driver_df):

    stops = (
        driver_df["Stint"].nunique() - 1
    )

    if stops <= 1:
        return 1

    elif stops == 2:
        return 2

    else:
        return 3

def get_track_year(
    driver_df
):
    
    track = (
        driver_df["Track"].iloc[0]
    )
    
    year = (
        driver_df["RaceYear"].iloc[0]
    )
    
    return track,year

def get_starting_compound(
    driver_df
):

    first_lap = (
        driver_df
        .sort_values(
            "LapNumber"
        )
        .iloc[0]
    )

    return first_lap[
        "Compound"
    ]

def get_laps_completed(
    driver_df
):
    
    return int(
        driver_df[
            "LapNumber"
        ].max()
    )

def load_team_strength():

    df = pd.read_parquet(
        TEAM_STRENGTH_PATH
    )

    lookup = {}

    for _, row in df.iterrows():

        lookup[
            row["Team"]
        ] = {

            "QualiStrength":
                row["QualiStrength"],

            "RaceStrength":
                row["RaceStrength"],

            "CombinedStrength":
                row["CombinedStrength"]
        }

    return lookup


team_strength_lookup = (
        load_team_strength()
    )

# print(
#     team_strength_lookup[
#         "Red Bull Racing"
#     ]
# )

def load_driver_ratings():

    df = pd.read_parquet(
        DRIVER_RATING_PATH
    )

    lookup = {}

    for _, row in df.iterrows():

        key = (
            row["Driver"],
            row["Track"]
        )

        lookup[key] = {

            "QualiRating":
                row["QualiRating"],

            "RaceRating":
                row["RaceRating"],

            "TeammateRating":
                row["TeammateRating"],

            "CombinedRating":
                row["CombinedRating"]
        }

    return lookup

def get_driver_track_rating(
    driver,
    track
):

    return driver_rating_lookup.get(
        (driver, track),
        {
            "QualiRating": 50,
            "RaceRating": 50,
            "TeammateRating": 50,
            "CombinedRating": 50
        }
    )

driver_rating_lookup = (
    load_driver_ratings()
)

def build_driver_row(
    driver_df
):
    
    driver = (
        driver_df["Driver"].iloc[0]
    )
    
    team = (
        driver_df["Team"].iloc[0]
    )
    
        
    team_features = (
        team_strength_lookup.get(
            team,
            {}
        )
    )
    
    track, year = (
        get_track_year(
            driver_df
        )
    )
    
    driver_ratings = (
        get_driver_track_rating(
            driver,
            track
        )
    )
    
    strategy_type = (
        get_strategy_type(
            driver_df
        )
    )
    
    starting_compound = (
        get_starting_compound(
            driver_df
        )
    )
    
    laps_completed = (
        get_laps_completed(
            driver_df
        )
    )
    
    row = {

            "Driver":
                driver,
                        
            "DriverQualiRating":
                driver_ratings[
                    "QualiRating"
                ],

            "DriverRaceRating":
                driver_ratings[
                    "RaceRating"
                ],

            "DriverTeammateRating":
                driver_ratings[
                    "TeammateRating"
                ],

            "DriverCombinedRating":
                driver_ratings[
                    "CombinedRating"
                ],
                
            "Team": 
                team,
                
            "TeamQualiStrength":
                team_features.get(
                    "QualiStrength",
                    50
                ),

            "TeamRaceStrength":
                team_features.get(
                    "RaceStrength",
                    50
                ),

            "TeamCombinedStrength":
                team_features.get(
                    "CombinedStrength",
                    50
                ),

            "Track":
                track,

            "RaceYear":
                year,

            "StartingCompound":
                starting_compound,

            "LapsCompleted":
                laps_completed,

            "StrategyType":
                strategy_type
        }

    return row

def build_strategy_dataset():
    
    rows = []

    files = sorted(
        os.listdir(
            CLEAN_LAPS_DIR
        )
    )
    
    print(
        f"\nFound {len(files)} race files\n"
    )
    
    for file_name in files:
        
        print(
            f"Processing: {file_name}"
        )
        
        file_path = os.path.join(
            CLEAN_LAPS_DIR,
            file_name
        )
        
        race_df = pd.read_parquet(
            file_path
        )
        
        drivers = (
            race_df["Driver"]
            .dropna()
            .unique()
        )
        
        for driver in drivers:
            
            driver_df = race_df[
                race_df["Driver"] == driver
            ]
            
            row = build_driver_row(
                driver_df
            )
            
            rows.append(
                row
            )
    
    dataset = pd.DataFrame(
        rows
    )
    
    return dataset


if __name__ == "__main__":

    dataset = (
        build_strategy_dataset()
    )

    print(
        "\n========== DATASET SUMMARY ==========\n"
    )

    print(
        f"Rows: {len(dataset)}"
    )

    print(
        f"Columns: {len(dataset.columns)}"
    )

    print("\nHEAD:\n")

    print(
        dataset.head()
    )
    
    print(
        "\nStrategy Distribution:\n"
    )

    print(
        dataset[
            "StrategyType"
        ].value_counts()
    )

    dataset.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved Dataset:\n"
        f"{OUTPUT_PATH}"
    )