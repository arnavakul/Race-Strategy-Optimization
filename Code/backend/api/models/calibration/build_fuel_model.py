import pickle
import os
import glob
import numpy as np
import pandas as pd

from api.config.paths import (
    FULL_LAPS_PATH,
    SAVED_MODELS_PATH
)

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

    df = pd.read_parquet(file_path)
    
    print(df["Compound"].unique())

    hard_df = df[
        df["Compound"].astype(str).str.upper()
        == "HARD"
    ]

    drivers = hard_df["Driver"].unique()

    for driver in drivers:

        driver_df = hard_df[
            hard_df["Driver"] == driver
        ].sort_values("LapNumber")

        if len(driver_df) < 15:
            continue

        driver_df = driver_df.dropna(
            subset=[
                "LapNumber",
                "LapTimeSeconds"
            ]
        )

        lap_numbers = driver_df[
            "LapNumber"
        ].values.astype(float)

        lap_times = driver_df[
            "LapTimeSeconds"
        ].values.astype(float)

        slope, intercept = np.polyfit(
            lap_numbers,
            lap_times,
            1
        )
        
        if np.isnan(slope):

            print(
                f"NaN slope detected: "
                f"{track_key} {driver}"
            )

            continue

        fuel_results.append(slope)
        
        print(
            track_key,
            driver,
            len(driver_df)
        )




if len(fuel_results) == 0:

    raise ValueError(
        "No valid fuel samples found."
    )

average_fuel_slope = np.mean(
    fuel_results
)

fuel_effect_per_kg = (
    abs(average_fuel_slope) / 4
)

fuel_model = {

    "fuel_effect_per_kg":
    float(fuel_effect_per_kg)
}

print("\nTOTAL FUEL SAMPLES\n")
print(len(fuel_results))

average_fuel_slope = np.mean(
    fuel_results
)

fuel_effect_per_kg = (
    abs(average_fuel_slope) / 4
)

fuel_model = {

    "fuel_effect_per_kg":
    float(fuel_effect_per_kg)
}

save_path = (
    SAVED_MODELS_PATH
    / "fuel_model.pkl"
)

with open(save_path, "wb") as f:

    pickle.dump(
        fuel_model,
        f
    )

print("\nFUEL MODEL\n")

print(fuel_model)