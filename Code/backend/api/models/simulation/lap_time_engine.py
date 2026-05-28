import os
import pickle
import random

from api.models.simulation.fuel_state import FuelState

from api.models.simulation.track_model import (
    get_track_parameters
)

from api.models.simulation.track_evolution_model import (
    get_track_grip
)

from api.models.simulation.driver_behavior_model import (
    DRIVER_PROFILES
)

from api.models.simulation.tyre_set_model import (
    get_freshness_penalty
)

# Paths

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

base_pace_path = os.path.join(
    BASE_DIR,
    "models",
    "saved_models",
    "track_base_pace.pkl"
)

deg_model_path = os.path.join(
    BASE_DIR,
    "models",
    "saved_models",
    "all_tracks_degradation.pkl"
)

# Load models

with open(base_pace_path, "rb") as f:

    track_base_pace = pickle.load(f)

with open(deg_model_path, "rb") as f:

    degradation_models = pickle.load(f)

# Base pace

def get_base_pace(track):

    return track_base_pace[track] + 4.5

# Tyre degradation

def get_degradation(
    track,
    compound,
    tyre_age
):

    track_data = get_track_parameters(track)

    deg = (
        track_data["compound_deg"][compound]
    )

    cliff_age = (
        track_data["cliff_age"][compound]
    )

    cliff_multiplier = (
        track_data["cliff_multiplier"][compound]
    )

    # Fresh tyre gain
    if tyre_age <= 3:

        degradation = (
            -0.05 * tyre_age
        )

    # Normal degradation phase
    elif tyre_age <= 10:

        base_phase = -0.15

        degradation = (

            base_phase

            + (tyre_age - 3)

            * abs(deg)

            * 0.30
        )

    # High degradation phase
    elif tyre_age <= cliff_age:

        base_phase = (

            -0.15

            + (7 * abs(deg) * 0.30)
        )

        degradation = (

            base_phase

            + (tyre_age - 10)

            * abs(deg)

            * 0.45
        )

    # Tyre cliff
    else:

        base_phase = (

            -0.15

            + (7 * abs(deg) * 0.30)

            + ((cliff_age - 10)

            * abs(deg)

            * 0.45)
        )

        degradation = (

            base_phase

            + (tyre_age - cliff_age)

            * cliff_multiplier
        )

    return degradation

# Lap time engine

def compute_lap_time(
    track,
    compound,
    tyre_age,
    fuel_correction,
    current_lap,
    total_laps,
    driver_profile = "BALANCED",
    tyre_set = None
):

    track_data = get_track_parameters(track)
    
    # Driver behavior profile
    driver_data = DRIVER_PROFILES[
        driver_profile
    ]

    pace_gain = driver_data[
        "pace_gain"
    ]

    deg_multiplier = driver_data[
        "deg_multiplier"
    ]

    # Track evolution grip
    track_grip = get_track_grip(
        current_lap,
        total_laps
    )

    compound_pace_delta = (
        track_data["compound_pace_delta"]
    )

    base_pace = get_base_pace(track)

    degradation = (
        get_degradation(
            track,
            compound,
            tyre_age
        )
        * deg_multiplier
    )

    compound_offset = (
        compound_pace_delta[compound]
    )

    # Core lap time model
    lap_time = (

        base_pace

        + compound_offset

        + degradation

        - fuel_correction

        - pace_gain
    )   
    
    # Tyre freshness penalty

    freshness_penalty = 0

    if tyre_set is not None:

        freshness_penalty = (
            get_freshness_penalty(
                tyre_set
            )
        )

    lap_time += freshness_penalty

    # Apply track evolution
    lap_time = (
        lap_time / track_grip
    )

    # Optional micro-randomness
    lap_time += random.uniform(
        -0.08,
        0.08
    )
    
    return {

        "lap_time": float(lap_time),

        "base_pace": float(base_pace),

        "compound_offset": float(compound_offset),

        "degradation": float(degradation),

        "fuel_correction": float(fuel_correction),

        "track_grip": float(track_grip),
        
        "freshness_penalty": (
            float(freshness_penalty)
        ),
    }

# Testing

from api.models.simulation.tyre_set_model import (
    create_tyre_set
)

test_tyre = create_tyre_set(

    compound="MEDIUM",

    freshness=0.82,

    heat_cycles=2,

    used_laps=6
)

def main():

    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8
    )

    for lap in range(1, 21):

        fuel_correction = (
            fuel.getFuelCorrection()
        )

        result = compute_lap_time(

            track="bahrain_2022",

            compound="MEDIUM",

            tyre_age=lap,

            fuel_correction=fuel_correction,

            current_lap=lap,

            total_laps=57,

            driver_profile="AGGRESSIVE",
            
            tyre_set=test_tyre
            
        )

        print(

            f"Lap {lap:>2} | "

            f"Lap Time: {result['lap_time']:.3f} | "

            f"Grip: {result['track_grip']:.3f} | "

            f"Deg: {result['degradation']:.3f}"
            
            f"Freshness Penalty: "
            
            f"{result['freshness_penalty']:.3f}"
        )

        fuel.burnFuel()

if __name__ == "__main__":

    main()