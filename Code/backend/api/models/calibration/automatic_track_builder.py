import os
import glob
import pickle
import numpy as np
import pandas as pd

from api.config.paths import (
    FULL_LAPS_PATH,
    SAVED_MODELS_PATH
)

all_files = glob.glob(
    str(FULL_LAPS_PATH / "*.parquet")
)

track_characteristics = {}

for file_path in all_files:

    file_name = os.path.basename(file_path)

    parts = file_name.replace(
        ".parquet",
        ""
    ).split("_")

    track = parts[0]

    year = int(parts[1])

    track_key = f"{track}_{year}"

    print(f"\nProcessing {track_key}")

    df = pd.read_parquet(file_path)

    compounds = [
        "SOFT",
        "MEDIUM",
        "HARD"
    ]

    compound_deg = {}

    compound_pace = {}

    for compound in compounds:

        compound_df = df[
            df["Compound"]
            .astype(str)
            .str.upper()
            == compound
        ]

        if len(compound_df) < 10:

            continue

        lap_numbers = compound_df[
            "LapNumber"
        ].values.astype(float)

        lap_times = compound_df[
            "LapTimeSeconds"
        ].values.astype(float)

        slope, intercept = np.polyfit(
            lap_numbers,
            lap_times,
            1
        )

        compound_deg[compound] = (
            float(slope)
        )

        compound_pace[compound] = (
            float(lap_times.mean())
        )

    if len(compound_pace) == 0:

        continue

    fastest_compound = min(
        compound_pace.values()
    )

    compound_pace_delta = {}

    for compound, avg_pace in compound_pace.items():

        compound_pace_delta[
            compound
        ] = (
            avg_pace
            - fastest_compound
        )

    track_characteristics[
        track_key
    ] = {

        "compound_deg":
        compound_deg,

        "compound_pace_delta":
        compound_pace_delta,

        "warmup_penalty": {

            "SOFT": 0.5,

            "MEDIUM": 0.8,

            "HARD": 1.2
        },

        "cliff_age": {

            "SOFT": 12,

            "MEDIUM": 22,

            "HARD": 30
        }
    }

save_path = (
    SAVED_MODELS_PATH
    / "track_characteristics.pkl"
)

with open(save_path, "wb") as f:

    pickle.dump(
        track_characteristics,
        f
    )

print("\nTRACK MODEL BUILT\n")

print(track_characteristics)