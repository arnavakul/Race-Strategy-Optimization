import os
import glob
import pandas as pd

from api.config.paths import FULL_LAPS_PATH

from api.models.evaluation.validate_stint import (
    validate_stint
)

all_files = glob.glob(
    str(FULL_LAPS_PATH / "*.parquet")
)

all_results = []

for file_path in all_files:

    file_name = os.path.basename(file_path)

    parts = file_name.replace(
        ".parquet",
        ""
    ).split("_")

    track = parts[0]

    year = int(parts[1])

    df = pd.read_parquet(file_path)

    drivers = df["Driver"].unique()

    for driver in drivers:

        driver_df = df[
            df["Driver"] == driver
        ].sort_values("LapNumber")

        current_compound = None

        stint_start = None

        previous_lap = None

        stints = []

        for _, row in driver_df.iterrows():

            compound = row["Compound"]

            lap_number = int(
                row["LapNumber"]
            )

            if current_compound is None:

                current_compound = compound

                stint_start = lap_number

            elif compound != current_compound:

                stints.append({

                    "compound": current_compound,

                    "start_lap": stint_start,

                    "end_lap": previous_lap
                })

                current_compound = compound

                stint_start = lap_number

            previous_lap = lap_number

        if current_compound is not None:

            stints.append({

                "compound": current_compound,

                "start_lap": stint_start,

                "end_lap": previous_lap
            })

        print(f"\n{track}_{year} | {driver}")

        print(stints)

        for stint in stints:

            compound = stint["compound"]

            start_lap = stint["start_lap"]

            end_lap = stint["end_lap"]

            stint_length = (
                end_lap - start_lap + 1
            )

            if stint_length < 5:
                continue

            result = validate_stint(

                track=track,

                year=year,

                driver=driver,

                compound=compound,

                start_lap=start_lap,

                end_lap=end_lap
            )

            all_results.append(result)

results_df = pd.DataFrame(all_results)

print("\nGLOBAL SUMMARY\n")

print(results_df[[
    "track",
    "driver",
    "compound",
    "mae",
    "rmse"
]])

print("\nAVERAGE METRICS\n")

print(
    "Average MAE:",
    results_df["mae"].mean()
)

print(
    "Average RMSE:",
    results_df["rmse"].mean()
)