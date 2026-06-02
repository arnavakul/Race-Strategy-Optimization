from api.models.simulation.lap_time_engine import (
    compute_lap_time
)

from api.models.simulation.pitstop_model import (
    get_pitstop_time
)

from api.models.simulation.fuel_state import (
    FUEL_EFFECT_PER_KG
)

from api.models.simulation.safety_car_model import (
    get_safety_car_multiplier
)

import random


def get_weather_compound(
    weather_state
):

    if weather_state == "MIXED":

        return "INTERMEDIATE"

    elif weather_state == "WET":

        return "WET"

    return None


def simulate_rival_lap(
    rival,
    track,
    current_lap,
    total_laps,
    weather_state,
    safety_car_active=False,
    vsc_active=False
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

    # =====================================
    # WEATHER REACTION
    # =====================================

    weather_compound = (
        get_weather_compound(
            weather_state
        )
    )

    if (
        weather_compound is not None
        and
        current_compound != weather_compound
    ):

        rival["pitstops"] += 1

        rival["total_time"] += (
            get_pitstop_time(track)
            + random.uniform(-0.8, 0.8)
        )

        rival["current_compound"] = (
            weather_compound
        )

        rival["current_tyre_age"] = 0

        current_compound = (
            weather_compound
        )

        current_tyre_age = 0

        print(
            f"{rival['name']} WEATHER PIT -> "
            f"{weather_compound}"
        )

    elif (
        weather_state == "DRY"
        and
        current_compound in [
            "INTERMEDIATE",
            "WET"
        ]
    ):

        rival["pitstops"] += 1

        rival["total_time"] += (
            get_pitstop_time(track)
            + random.uniform(-0.8, 0.8)
        )

        dry_compound = (
            strategy[
                current_stint
            ][0]
        )

        rival["current_compound"] = (
            dry_compound
        )

        rival["current_tyre_age"] = 0

        current_compound = (
            dry_compound
        )

        current_tyre_age = 0

        print(
            f"{rival['name']} DRY PIT -> "
            f"{dry_compound}"
        )

    # =====================================
    # NORMAL STRATEGY PITSTOP
    # =====================================

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
            get_pitstop_time(track)
            + random.uniform(-0.8, 0.8)
        )

        current_compound = rival[
            "current_compound"
        ]

        current_tyre_age = 0

        current_stint = rival[
            "current_stint"
        ]

    # =====================================
    # FUEL
    # =====================================

    fuel_correction = (

        rival["fuel_load"]

        * FUEL_EFFECT_PER_KG
    )

    lap_data = compute_lap_time(

        track=track,

        compound=current_compound,

        tyre_age=current_tyre_age,

        fuel_correction=fuel_correction,

        current_lap=current_lap,

        total_laps=total_laps,

        driver=rival["name"],

        team=rival["team"],

        position=1,

        stint=current_stint + 1,

        race_year=2024
    )

    rival["fuel_load"] -= 1.8

    rival["fuel_load"] = max(
        rival["fuel_load"],
        0
    )

    lap_time = (

        lap_data["lap_time"]

        + rival["pace_offset"]

        + random.uniform(
            -0.15,
            0.15
        )
    )

    # =====================================
    # SC / VSC
    # =====================================

    if safety_car_active:

        lap_time *= (
            get_safety_car_multiplier()
        )

    elif vsc_active:

        lap_time *= 1.25

    rival["total_time"] += (
        lap_time
    )

    rival["current_tyre_age"] += 1

    return {

        "lap_time": lap_time,

        "fuel_correction":
            lap_data[
                "fuel_correction"
            ],

        "degradation":
            lap_data[
                "degradation"
            ],

        "base_pace":
            lap_data[
                "base_pace"
            ],

        "ml_adjustment":
            lap_data[
                "ml_adjustment"
            ]
    }