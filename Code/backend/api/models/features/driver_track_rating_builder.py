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

YEARS = [
    2022,
    2023,
    2024,
    2025
]

processed_path = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\processed"
)

historical_results_file = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\historical_results"
    r"\race_results.parquet"
)

output_path = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\driver_ratings"
)

os.makedirs(
    output_path,
    exist_ok=True
)


def load_session(
    track,
    year,
    session_type="Q"
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
        return None

    return pd.read_parquet(
        file_path
    )


def get_quali_classification(
    q_df
):

    classification = (
        q_df
        .groupby(
            ["Driver", "Team"],
            observed=True
        )["LapTimeSeconds"]
        .min()
        .reset_index()
    )

    classification = (
        classification
        .sort_values(
            "LapTimeSeconds"
        )
        .reset_index(
            drop=True
        )
    )

    classification[
        "QualiPosition"
    ] = range(
        1,
        len(classification) + 1
    )

    return classification


def load_historical_results():

    return pd.read_parquet(
        historical_results_file
    )


def calculate_teammate_rating(
    driver,
    track,
    results_df
):

    driver_results = results_df[
        (results_df["Driver"] == driver)
        &
        (results_df["Track"] == track)
    ]

    wins = 0
    total = 0

    for _, race in driver_results.iterrows():

        team = race["Team"]
        year = race["Year"]

        same_team = results_df[
            (results_df["Track"] == track)
            &
            (results_df["Year"] == year)
            &
            (results_df["Team"] == team)
        ]

        if len(same_team) != 2:
            continue

        my_finish = race[
            "FinishingPosition"
        ]

        teammate_finish = (
            same_team[
                same_team["Driver"] != driver
            ][
                "FinishingPosition"
            ]
            .iloc[0]
        )

        total += 1

        if my_finish < teammate_finish:
            wins += 1

    if total == 0:
        return 50.0

    return (
        wins / total
    ) * 100


def build_track_ratings():

    historical_results = (
        load_historical_results()
    )

    rows = []

    for track in TRACKS:

        print(
            f"\nProcessing {track}"
        )

        quali_positions = {}

        for year in YEARS:

            q_df = load_session(
                track,
                year,
                "Q"
            )

            if q_df is None:
                continue

            classification = (
                get_quali_classification(
                    q_df
                )
            )

            for _, row in (
                classification.iterrows()
            ):

                driver = row["Driver"]

                if driver not in quali_positions:

                    quali_positions[
                        driver
                    ] = []

                quali_positions[
                    driver
                ].append(
                    row[
                        "QualiPosition"
                    ]
                )

        track_results = (
            historical_results[
                historical_results[
                    "Track"
                ] == track
            ]
        )

        all_drivers = set(
            list(
                quali_positions.keys()
            )
            +
            list(
                track_results[
                    "Driver"
                ].unique()
            )
        )

        for driver in all_drivers:

            if driver not in quali_positions:
                continue

            avg_quali_pos = (
                sum(
                    quali_positions[
                        driver
                    ]
                )
                /
                len(
                    quali_positions[
                        driver
                    ]
                )
            )

            quali_rating = (
                (
                    21
                    -
                    avg_quali_pos
                )
                /
                20
            ) * 100

            driver_races = (
                track_results[
                    track_results[
                        "Driver"
                    ] == driver
                ]
            )

            if driver_races.empty:
                continue

            avg_finish = (
                driver_races[
                    "FinishingPosition"
                ]
                .mean()
            )

            avg_points = (
                driver_races[
                    "Points"
                ]
                .mean()
            )

            finish_score = (
                (
                    21
                    -
                    avg_finish
                )
                /
                20
            ) * 100

            points_score = (
                avg_points
                /
                25
            ) * 100

            race_rating = (
                finish_score
                * 0.6
                +
                points_score
                * 0.4
            )

            teammate_rating = (
                calculate_teammate_rating(
                    driver,
                    track,
                    historical_results
                )
            )

            combined_rating = (
                quali_rating * 0.45
                +
                race_rating * 0.45
                +
                teammate_rating * 0.10
            )

            rows.append({

                "Driver":
                    driver,

                "Track":
                    track,

                "QualiRating":
                    round(
                        quali_rating,
                        2
                    ),

                "RaceRating":
                    round(
                        race_rating,
                        2
                    ),

                "TeammateRating":
                    round(
                        teammate_rating,
                        2
                    ),

                "CombinedRating":
                    round(
                        combined_rating,
                        2
                    )
            })

    ratings_df = pd.DataFrame(
        rows
    )

    return ratings_df


if __name__ == "__main__":

    ratings_df = (
        build_track_ratings()
    )

    ratings_df = (
        ratings_df.sort_values(
            [
                "Track",
                "CombinedRating"
            ],
            ascending=[
                True,
                False
            ]
        )
    )

    save_file = os.path.join(
        output_path,
        "driver_track_ratings.parquet"
    )

    ratings_df.to_parquet(
        save_file,
        index=False
    )

    ratings_df.to_csv(
        save_file.replace(
            ".parquet",
            ".csv"
        ),
        index=False
    )

    print(
        "\nDRIVER TRACK RATINGS\n"
    )

    print(
        ratings_df.head(50)
    )

    print(
        f"\nSaved -> {save_file}"
    )
    
    print(
    ratings_df[
        ratings_df["Track"] == "Monaco"
    ][
        ["Driver"]
    ].value_counts()
)