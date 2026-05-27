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

    # simulate every lap
    for lap in range(total_laps):

        # current weather for this lap
        weather_state = weather_timeline[lap]

        # lap numbering starts from 1
        current_lap: int = lap + 1

        # tyre age increases every lap
        tyre_age: int = current_lap

        # default warmup penalty
        warmup_penalty: float = 0.0

        # apply warmup penalty for first 2 laps
        if tyre_age <= 2:

            warmup_penalty = float(
                warmup_map[compound]
            )

        # fuel correction effect
        fuel_correction: float = (
            fuel.getFuelCorrection()
        )

        # compute base lap physics
        lap_data: Dict[str, Any] = compute_lap_time(
            track=track,
            compound=compound,
            tyre_age=tyre_age,
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

            "tyre_age": tyre_age,

            "lap_time": corrected_lap_time,

            "warmup_penalty": warmup_penalty,

            "fuel_load": float(
                fuel.current_fuel
            ),

            "fuel_correction": fuel_correction,

            "cumulative_time": cumulative_time,

            "weather_state": weather_state
        })

        # burn fuel after lap
        fuel.burnFuel()

    # final stint output
    return {

        "total_time": cumulative_time,

        "laps": results
    }


# =========================================
# TESTING
# =========================================

if __name__ == "__main__":

    from api.models.simulation.weather_model import (
        generate_weather_timeline
    )

    weather_timeline = generate_weather_timeline(
        15
    )

    result = simulate_stint(
        track="bahrain_2022",
        compound="MEDIUM",
        total_laps=15,
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

        print(

            f"Lap {lap['lap']:>2} | "

            f"Weather: {lap['weather_state']:<7} | "

            f"Tyre Age: {lap['tyre_age']:>2} | "

            f"Fuel: {lap['fuel_load']:.2f} kg | "

            f"Lap Time: {lap['lap_time']:.3f} | "

            f"Warmup: {lap['warmup_penalty']:.2f} | "

            f"Delta: {delta:+.3f} | "

            f"Cumulative: {lap['cumulative_time']:.3f}"
        )

        previous_lap_time = lap["lap_time"]

    print(
        f"\nTotal Stint Time: "
        f"{result['total_time']:.3f}"
    )