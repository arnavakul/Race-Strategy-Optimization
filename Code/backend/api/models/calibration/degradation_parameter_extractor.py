import os
import glob
import numpy as np
import pandas as pd

from api.config.paths import FULL_LAPS_PATH

all_files = glob.glob(
    str(FULL_LAPS_PATH / "*.parquet")
)

results = []

for file_path in all_files:

    file_name = os.path.basename(file_path)

    parts = file_name.replace(
        ".parquet",
        ""
    ).split("_")

    track = parts[0]

    year = int(parts[1])

    track_key = f"{track}_{year}"

    print(f"\nProcessing: {track_key}")

    df = pd.read_parquet(file_path)

    drivers = df["Driver"].unique()

    for driver in drivers:

        driver_df = df[
            df["Driver"] == driver
        ].sort_values("LapNumber")

        current_compound = None

        stint_rows = []

        for _, row in driver_df.iterrows():

            compound = row["Compound"]

            if current_compound is None:

                current_compound = compound

            if compound != current_compound:

                if len(stint_rows) >= 5:

                    stint_df = pd.DataFrame(
                        stint_rows
                    )

                    lap_numbers = stint_df[
                        "LapNumber"
                    ].values

                    lap_times = stint_df[
                        "LapTimeSeconds"
                    ].values

                    slope, intercept = np.polyfit(
                        lap_numbers,
                        lap_times,
                        1
                    )

                    results.append({

                        "track": track_key,

                        "compound": current_compound,

                        "driver": driver,

                        "deg_per_lap": slope
                    })

                stint_rows = []

                current_compound = compound

            stint_rows.append(row)

        # FINAL STINT PROCESSING

        if len(stint_rows) >= 5:

            stint_df = pd.DataFrame(
                stint_rows
            )

            lap_numbers = stint_df[
                "LapNumber"
            ].values

            lap_times = stint_df[
                "LapTimeSeconds"
            ].values

            slope, intercept = np.polyfit(
                lap_numbers,
                lap_times,
                1
            )

            results.append({

                "track": track_key,

                "compound": current_compound,

                "driver": driver,

                "deg_per_lap": slope
            })

results_df = pd.DataFrame(results)

print("\nFULL RESULTS\n")

print(results_df)

print("\nAVERAGE DEGRADATION\n")

print(
    results_df.groupby(
        ["track", "compound"]
    )["deg_per_lap"].mean()
)