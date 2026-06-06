#This file is solely responsible for having the team strength based off qualifying, FP2 and FP3. 
# Example Output:

# Team          QualiStrength   RaceStrength   CombinedStrength

# McLaren       100             99             99.6
# Ferrari       98              97             97.6
# Mercedes      95              94             94.6
# Red Bull      93              95             93.8


import os 
import pandas as pd 

TRACKS = [
    "Abu Dhabi",
    "Austria",
    "Bahrain",
    "Barcelona",
    "Brazil",
    "COTA",
    "Hungary",
    "Jeddah",
    "Melbourne",
    "Monaco",
    "Monza",
    "Montreal",
    "Qatar",
    "Silverstone",
    "Singapore",
    "Spa",
    "Suzuka"
]

processed_path = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\processed"
)

def load_session_data(
    track,
    session_type,
    year=2026
):

    file_path = os.path.join(
        processed_path,
        session_type,
        "clean_laps",
        f"{track.lower().replace(' ', '_')}_{year}_{session_type}_clean.parquet"
    )

    if not os.path.exists(
        file_path
    ):
        print(
            f"Missing: {file_path}"
        )
        return None

    return pd.read_parquet(
        file_path
    )


def calculate_quali_strength():

    q_folder = os.path.join(
        processed_path,
        "Q",
        "clean_laps"
    )

    team_gaps = []

    for file_name in os.listdir(q_folder):

        if "_2026_Q_clean.parquet" not in file_name:
            continue

        track = file_name.split("_2026")[0]

        q_df = pd.read_parquet(
            os.path.join(
                q_folder,
                file_name
            )
        )

        fastest_lap = q_df[
            "LapTimeSeconds"
        ].min()

        for team, team_df in q_df.groupby(
            "Team",
            observed=True
        ):

            driver_bests = (
                team_df
                .groupby(
                    "Driver",
                    observed=True
                )["LapTimeSeconds"]
                .min()
            )

            team_best = driver_bests.mean()

            gap = (
                team_best
                - fastest_lap
            ) / fastest_lap

            team_gaps.append({
                "Track": track,
                "Team": team,
                "Gap": gap
            })

    return pd.DataFrame(team_gaps)

def calculate_race_strength():

    fp_sessions = [
        "FP2",
        "FP3"
    ]

    race_gaps = []

    for session_type in fp_sessions:

        session_folder = os.path.join(
            processed_path,
            session_type,
            "clean_laps"
        )

        for file_name in os.listdir(
            session_folder
        ):

            if f"_2026_{session_type}_clean.parquet" not in file_name:
                continue

            track = file_name.split(
                "_2026"
            )[0]

            session_df = pd.read_parquet(
                os.path.join(
                    session_folder,
                    file_name
                )
            )

            if (
                "FuelCorrectedLapTime"
                not in session_df.columns
            ):
                continue

            team_long_runs = []

            for team, team_df in session_df.groupby(
                "Team",
                observed=True
            ):

                driver_paces = (
                    team_df
                    .groupby(
                        "Driver",
                        observed=True
                    )[
                        "FuelCorrectedLapTime"
                    ]
                    .mean()
                )

                team_pace = (
                    driver_paces.mean()
                )

                team_long_runs.append(
                    {
                        "Track": track,
                        "Team": team,
                        "TeamPace": team_pace
                    }
                )

            if len(team_long_runs) == 0:
                continue

            team_long_runs_df = pd.DataFrame(
                team_long_runs
            )

            fastest_team_pace = (
                team_long_runs_df[
                    "TeamPace"
                ].min()
            )

            for _, row in (
                team_long_runs_df.iterrows()
            ):

                gap = (
                    row["TeamPace"]
                    -
                    fastest_team_pace
                ) / fastest_team_pace

                race_gaps.append(
                    {
                        "Track": track,
                        "Team": row["Team"],
                        "Gap": gap
                    }
                )

    return pd.DataFrame(
        race_gaps
    )


def build_quali_rankings(quali_strength_df):
    
    team_strength = (
        quali_strength_df
        .groupby(
            "Team",
            observed = True
        )["Gap"]
        .mean()
        .reset_index()
    )
    
    team_strength = (
        team_strength
        .sort_values(
            by="Gap",
            ascending=True
        )
    )
    
    team_strength.reset_index(
        drop=True,
        inplace=True
    )
    
    team_strength[
        "QualiRank"
    ] = (
        team_strength[
            "Gap"
        ]
        .rank(
            ascending=True
        )
    )
    
    max_rank = (
        team_strength[
            "QualiRank"
        ].max()
    )
    
    team_strength[
        "QualiStrength"
    ] = (
        (
            max_rank
            -
            team_strength[
                "QualiRank"
            ]
        )
        /
        (
            max_rank - 1
        )
    ) * 100
    
    return team_strength

def build_race_rankings(
    race_strength_df
):

    team_strength = (
        race_strength_df
        .groupby(
            "Team",
            observed=True
        )["Gap"]
        .mean()
        .reset_index()
    )

    team_strength = (
        team_strength
        .sort_values(
            by="Gap",
            ascending=True
        )
    )

    team_strength.reset_index(
        drop=True,
        inplace=True
    )

    team_strength[
        "RaceRank"
    ] = (
        team_strength[
            "Gap"
        ]
        .rank(
            ascending=True
        )
    )

    max_rank = (
        team_strength[
            "RaceRank"
        ].max()
    )

    team_strength[
        "RaceStrength"
    ] = (
        (
            max_rank
            -
            team_strength[
                "RaceRank"
            ]
        )
        /
        (
            max_rank - 1
        )
    ) * 100

    return team_strength

def build_combined_strength(
    quali_rankings,
    race_rankings
):

    combined_df = (
        quali_rankings[
            [
                "Team",
                "QualiStrength"
            ]
        ]
        .merge(
            race_rankings[
                [
                    "Team",
                    "RaceStrength"
                ]
            ],
            on="Team"
        )
    )

    combined_df[
        "CombinedStrength"
    ] = (
        combined_df[
            "QualiStrength"
        ] * 0.60
        +
        combined_df[
            "RaceStrength"
        ] * 0.40
    )

    combined_df = (
        combined_df
        .sort_values(
            "CombinedStrength",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    return combined_df

if __name__ == "__main__":

    quali_strength_df = (
        calculate_quali_strength()
    )

    race_strength_df = (
        calculate_race_strength()
    )

    quali_rankings = (
        build_quali_rankings(
            quali_strength_df
        )
    )

    race_rankings = (
        build_race_rankings(
            race_strength_df
        )
    )

    combined_strength = (
        build_combined_strength(
            quali_rankings,
            race_rankings
        )
    )

    print(
        "\nTEAM STRENGTH HIERARCHY\n"
    )

    print(
        combined_strength
    )

    save_folder = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\team_strength"
    )

    os.makedirs(
        save_folder,
        exist_ok=True
    )

    combined_strength.to_parquet(
        os.path.join(
            save_folder,
            "team_strength.parquet"
        ),
        index=False
    )

    combined_strength.to_csv(
        os.path.join(
            save_folder,
            "team_strength.csv"
        ),
        index=False
    )

    print(
        "\nSaved team strength file."
    )