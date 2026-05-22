import pandas as pd

from typing import List, Dict, Any

from api.config.paths import FULL_LAPS_PATH

from api.models.simulation.stint_simulator import (
    simulate_stint
)

from api.models.evaluation.metrics import (
    mae,
    rmse
)


def validate_stint(
    track: str,
    year: int,
    driver: str,
    compound: str,
    start_lap: int,
    end_lap: int
) -> Dict[str, Any]:

    file_path = (
        FULL_LAPS_PATH
        / f"{track}_{year}_full.parquet"
    )

    df = pd.read_parquet(file_path)

    df = df[
        (df["Driver"] == driver)
        & (df["Compound"] == compound)
        & (df["LapNumber"] >= start_lap)
        & (df["LapNumber"] <= end_lap)
    ]

    print("\nAVAILABLE DRIVER + COMPOUND COMBINATIONS:\n")

    print(
        df[
            ["Driver", "Compound"]
        ].drop_duplicates()
    )

    print(
        f"\nFiltered Laps: {len(df)}"
    )

    if len(df) == 0:

        raise ValueError(
            "No laps found for given filters."
        )

    if "IsAccurate" in df.columns:

        df = df[
            df["IsAccurate"] == True
        ]

    actual_laps: List[float] = (
        df["LapTimeSeconds"]
        .astype(float)
        .tolist()
    )

    track_key = f"{track}_{year}"

    simulated: Dict[str, Any] = simulate_stint(
        track=track_key,
        compound=compound,
        total_laps=len(actual_laps)
    )

    predicted_laps: List[float] = [

        float(lap["lap_time"])

        for lap in simulated["laps"]
    ]
    
    print("\n Real VS Simulated Laps")
    
    for i in range(len(actual_laps)):
            
        delta = (
            predicted_laps[i] - actual_laps[i]
        )

        print(
            f"Lap {i+1:>2} | "
            f"Real: {actual_laps[i]:.3f} | "
            f"Sim: {predicted_laps[i]:.3f} | "
            f"Delta: {delta:+.3f}"
        )
    
    results: Dict[str, Any] = {

        "track": track,

        "year": year,

        "driver": driver,

        "compound": compound,

        "start_lap": start_lap,

        "end_lap": end_lap,

        "mae": mae(
            actual_laps,
            predicted_laps
        ),

        "rmse": rmse(
            actual_laps,
            predicted_laps
        ),

        "actual_laps": actual_laps,

        "predicted_laps": predicted_laps,

        "simulated_total_time": simulated[
            "total_time"
        ]
    }

    return results


if __name__ == "__main__":

    result = validate_stint(

        track="bahrain",

        year=2024,

        driver="VER",

        compound="SOFT",

        start_lap=1,

        end_lap=15
    )

    print("\nSTINT VALIDATION\n")

    print(
        f"Track: {result['track']}"
    )

    print(
        f"Driver: {result['driver']}"
    )

    print(
        f"Compound: {result['compound']}"
    )

    print(
        f"MAE: {result['mae']:.3f}"
    )

    print(
        f"RMSE: {result['rmse']:.3f}"
    )

    print(
        f"Simulated Total Time: "
        f"{result['simulated_total_time']:.3f}"
    )