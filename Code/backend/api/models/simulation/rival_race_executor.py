from api.models.simulation.lap_time_engine import (
    compute_lap_time
)

from api.models.simulation.pitstop_model import (
    get_pitstop_time
)

from api.models.simulation.ml_pace_adapter import (
    get_ml_pace_adjustment
)
import random


def simulate_rival_lap(
    rival,
    track,
    current_lap,
    total_laps
):

    strategy = rival["strategy"]

    current_stint = rival["current_stint"]

    current_compound = rival[
        "current_compound"
    ]

    current_tyre_age = rival[
        "current_tyre_age"
    ]

    stint_length = strategy[
        current_stint
    ][1]

    # PIT STOP

    if (
        current_tyre_age >= stint_length
        and
        current_stint < len(strategy) - 1
    ):

        rival["current_stint"] += 1

        rival["pitstops"] += 1

        rival["current_compound"] = (

            strategy[
                rival["current_stint"]
            ][0]
        )

        rival["current_tyre_age"] = 0

        rival["total_time"] += (
            get_pitstop_time(track) + random.uniform(-0.8,0.8)
        )

        current_compound = rival[
            "current_compound"
        ]

        current_tyre_age = 0

    lap_data = compute_lap_time(

        track=track,

        compound=current_compound,

        tyre_age=current_tyre_age,

        fuel_correction=0.0,

        current_lap=current_lap,

        total_laps=total_laps,

        driver=rival["name"],

        team=rival["team"],

        position=1,

        stint=current_stint + 1,

        race_year=2024
    )

    lap_time = (

        lap_data["lap_time"]

        + rival["pace_offset"]
        
        + random.uniform(-0.15,0.15)
    )

    rival["total_time"] += lap_time

    rival["current_tyre_age"] += 1

    return lap_time