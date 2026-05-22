#Now we will estimate the fuel usage of the cars 
# how much lap time improves
# as fuel burns off

import os
import glob
import numpy as np
import pandas as pd

from api.config.paths import FULL_LAPS_PATH

all_files = glob.glob(
    str(FULL_LAPS_PATH / "*.parquet")
)

fuel_results = []

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

    hard_df = df[
        df["Compound"] == "HARD"
    ] #used hard becaus eit degrades slowly so it is easy to isolate fuel effect 

    drivers = hard_df["Driver"].unique()

    for driver in drivers:

        driver_df = hard_df[
            hard_df["Driver"] == driver
        ].sort_values("LapNumber")

        if len(driver_df) < 15:
            continue

        lap_numbers = driver_df[
            "LapNumber"
        ].values

        lap_times = driver_df[
            "LapTimeSeconds"
        ].values

        slope, intercept = np.polyfit(
            lap_numbers,
            lap_times,
            1
        )

        fuel_results.append({

            "track": track_key,

            "driver": driver,

            "fuel_slope": slope
        })

fuel_df = pd.DataFrame(
    fuel_results
)

print("\nFUEL RESULTS\n")

print(fuel_df)

print("\nAVERAGE FUEL EFFECT\n")

print(
    fuel_df["fuel_slope"].mean()
)