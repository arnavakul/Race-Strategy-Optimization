import os
import fastf1
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

OUTPUT_FOLDER = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\historical_results"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

fastf1.Cache.enable_cache(
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\api\cache"
)


def get_race_results(
    year,
    track
):

    try:

        print(
            f"Loading {track} {year}"
        )

        session = fastf1.get_session(
            year,
            track,
            "R"
        )

        session.load()

        results = session.results

        rows = []

        for _, row in results.iterrows():

            rows.append({

                "Year":
                    year,

                "Track":
                    track,

                "Driver":
                    row["Abbreviation"],

                "Team":
                    row["TeamName"],

                "GridPosition":
                    row["GridPosition"],

                "FinishingPosition":
                    row["Position"],

                "Points":
                    row["Points"],

                "ClassifiedPosition":
                    row["ClassifiedPosition"]
            })

        return rows

    except Exception as e:

        print(
            f"Failed {track} {year}"
        )

        print(e)

        return []


def build_results_database():

    all_rows = []

    for track in TRACKS:

        for year in YEARS:

            all_rows.extend(
                get_race_results(
                    year,
                    track
                )
            )

    results_df = pd.DataFrame(
        all_rows
    )

    save_file = os.path.join(
        OUTPUT_FOLDER,
        "race_results.parquet"
    )

    results_df.to_parquet(
        save_file,
        index=False
    )

    results_df.to_csv(
        save_file.replace(
            ".parquet",
            ".csv"
        ),
        index=False
    )

    print(
        "\nSaved:"
    )

    print(
        save_file
    )

    print(
        results_df.head()
    )

    print(
        results_df.shape
    )


if __name__ == "__main__":

    build_results_database()