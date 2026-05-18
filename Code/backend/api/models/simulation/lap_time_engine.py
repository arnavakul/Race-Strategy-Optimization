import os
import pickle
import random

from models.simulation.fuel_state import FuelState

from models.simulation.track_model import (
    get_track_parameters
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

    return track_base_pace[track]


# Tyre degradation

def get_degradation(
    track,
    compound,
    tyre_age
):

    track_data = get_track_parameters(track)

    compound_deg = (
        track_data["compound_deg"]
    )

    cliff_age = (
        track_data["cliff_age"]
    )

    safe_age = max(1, tyre_age)

    base_deg = (
        safe_age
        * compound_deg[compound]
    )

    cliff_multiplier = {
        "SOFT": 0.40,
        "MEDIUM": 0.25,
        "HARD": 0.15
    }

    if safe_age > cliff_age[compound]:

        cliff_penalty = (
            safe_age
            - cliff_age[compound]
        ) * cliff_multiplier[compound]

        base_deg += cliff_penalty

    noise = random.uniform(0, 0.01)

    degradation = base_deg + noise

    return degradation


# Lap time engine

def compute_lap_time(
    track,
    compound,
    tyre_age,
    fuel_correction
):

    track_data = get_track_parameters(track)

    compound_pace_delta = (
        track_data["compound_pace_delta"]
    )

    base_pace = get_base_pace(track)

    degradation = get_degradation(
        track,
        compound,
        tyre_age
    )

    compound_offset = (
        compound_pace_delta[compound]
    )

    lap_time = (
        base_pace
        + compound_offset
        + degradation
        - fuel_correction
    )

    return {
        "lap_time": float(lap_time),
        "base_pace": float(base_pace),
        "compound_offset": float(compound_offset),
        "degradation": float(degradation),
        "fuel_correction": float(fuel_correction)
    }


# Testing

def main():

    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8,
        fuel_effect_per_kg=0.035
    )

    fuel_correction = fuel.getFuelCorrection()

    result = compute_lap_time(
        track="bahrain_2022",
        compound="MEDIUM",
        tyre_age=12,
        fuel_correction=fuel_correction
    )

    print(result)


if __name__ == "__main__":
    main()