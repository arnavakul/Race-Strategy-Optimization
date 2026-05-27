from typing import List, Dict, Any
import random

from api.models.simulation.lap_time_engine import (
    compute_lap_time
)

from api.models.simulation.fuel_state import (
    FuelState
)

from api.models.simulation.track_model import (
    get_track_parameters
)

from api.models.simulation.crossover_logic import(
    get_recommended_compound
)

from api.models.simulation.pitstop_model import(
    get_pitstop_time
)

from api.models.simulation.strategy_decision_engine import (
    should_pit
)

# =========================================
# STINT SIMULATOR
# =========================================

def simulate_stint(
    track: str,
    compound: str,
    total_laps: int,
    weather_timeline
) -> Dict[str, Any]:

    # store all lap data
    results: List[Dict[str, Any]] = []

    # total stint time
    cumulative_time: float = 0.0

    # initialize fuel model
    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8,
    )

    # get track-specific parameters
    track_data = get_track_parameters(track)

    # warmup penalties for tyres
    warmup_map = track_data["warmup_penalty"]
    
    current_compound = compound
    current_tyre_age = 0

    # simulate every lap
    for lap in range(total_laps):

        # current weather for this lap
        weather_state = weather_timeline[lap]
        
        pit_for_weather = should_pit(track=track, compound=current_compound, tyre_age=current_tyre_age,weather_state=weather_state)
        
        pit_loss = 0
        
        if pit_for_weather:
            laps_remaining = (total_laps-current_lap)
            new_compound = get_recommended_compound(weather_state,laps_remaining)
            current_compound = new_compound
            pit_loss = get_pitstop_time(track)
            cumulative_time += pit_loss
            current_tyre_age = 0

        # lap numbering starts from 1
        current_lap: int = lap + 1
        
        current_tyre_age += 1

        # default warmup penalty
        warmup_penalty: float = 0.0

        # apply warmup penalty for first 2 laps
        if current_tyre_age <= 2:

            warmup_penalty = float(
                warmup_map[current_compound]
            )

        # fuel correction effect
        fuel_correction: float = (
            fuel.getFuelCorrection()
        )

        # compute base lap physics
        lap_data: Dict[str, Any] = compute_lap_time(
            track=track,
            compound=current_compound,
            tyre_age=current_tyre_age,
            fuel_correction=fuel_correction
        )

        # final lap time after warmup
        corrected_lap_time: float = (
            float(lap_data["lap_time"])
            + warmup_penalty
        )

        # mixed weather slows lap slightly
        if weather_state == "MIXED":

            corrected_lap_time += random.uniform(
                0.5,
                1.5
            )

        # wet weather causes large slowdown
        elif weather_state == "WET":

            corrected_lap_time += random.uniform(
                2,
                5
            )

        # update cumulative stint time
        cumulative_time += corrected_lap_time

        # store lap telemetry
        results.append({

            "lap": current_lap,

            "tyre_age": current_tyre_age,

            "lap_time": corrected_lap_time,

            "warmup_penalty": warmup_penalty,

            "fuel_load": float(
                fuel.current_fuel
            ),

            "fuel_correction": fuel_correction,

            "cumulative_time": cumulative_time,

            "weather_state": weather_state,
            
            "compound": current_compound,

            "pit_for_weather": pit_for_weather,
            
            "pit_loss": pit_loss
            
        })

        # burn fuel after lap
        fuel.burnFuel()

    # final stint output
    return {

        "total_time": cumulative_time,

        "laps": results
    }

# TESTING


if __name__ == "__main__":

    # dynamic weather scenario
    weather_timeline = [

        "DRY",
        "DRY",
        "DRY",
        "DRY",
        "DRY",

        "MIXED",
        "MIXED",
        "MIXED",

        "WET",
        "WET",
        "WET",

        "DRY",
        "DRY",
        "DRY",
        "DRY",

        "DRY",
        "DRY",
        "DRY",
        "DRY",
        "DRY",

        "DRY",
        "DRY",
        "DRY",
        "DRY",
        "DRY"
    ]

    result = simulate_stint(

        track="bahrain_2024",

        compound="MEDIUM",

        total_laps=25,

        weather_timeline=weather_timeline
    )

    print("\nSTINT SIMULATION\n")

    previous_lap_time = None

    for lap in result["laps"]:

        if previous_lap_time is None:

            delta = 0.0

        else:

            delta = (

                lap["lap_time"]

                - previous_lap_time
            )

        # highlight pitstop
        if lap["pit_for_weather"]:

            print(
                f"\n=== PITSTOP ON LAP "
                f"{lap['lap']} ===\n"
            )

        print(

            f"Lap {lap['lap']:>2} | "

            f"Weather: {lap['weather_state']:<7} | "

            f"Compound: {lap['compound']:<13} | "

            f"Tyre Age: {lap['tyre_age']:>2} | "

            f"Fuel: {lap['fuel_load']:.2f} kg | "

            f"Lap Time: {lap['lap_time']:.3f} | "

            f"Warmup: {lap['warmup_penalty']:.2f} | "

            f"Pit: {lap['pit_for_weather']} | "

            f"Pit Loss: {lap['pit_loss']:<5} | "

            f"Delta: {delta:+.3f} | "

            f"Cumulative: {lap['cumulative_time']:.3f}"
        )

        previous_lap_time = lap["lap_time"]

    print(

        f"\nTotal Stint Time: "

        f"{result['total_time']:.3f}"
    )