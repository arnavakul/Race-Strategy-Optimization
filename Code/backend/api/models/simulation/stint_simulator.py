from models.simulation.lap_time_engine import (
    compute_lap_time
)

from models.simulation.fuel_state import (
    FuelState
)

from models.simulation.track_model import (
    get_track_parameters
)


# Stint simulator

def simulate_stint(
    track,
    compound,
    total_laps
):

    results = []

    cumulative_time = 0

    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8,
        fuel_effect_per_kg=0.035
    )

    track_data = get_track_parameters(track)

    warmup_map = (
        track_data["warmup_penalty"]
    )

    for lap in range(total_laps):

        tyre_age = lap + 1
        current_lap = lap + 1

        warmup_penalty = 0

        if tyre_age <= 2:

            warmup_penalty = (
                warmup_map[compound]
            )

        fuel_correction = (
            fuel.getFuelCorrection()
        )

        lap_data = compute_lap_time(
            track=track,
            compound=compound,
            tyre_age=tyre_age,
            fuel_correction=fuel_correction
        )

        corrected_lap_time = (
            lap_data["lap_time"]
            + warmup_penalty
        )

        cumulative_time += corrected_lap_time

        results.append({

            "lap": current_lap,

            "tyre_age": tyre_age,

            "lap_time": corrected_lap_time,

            "warmup_penalty": warmup_penalty,

            "fuel_load": fuel.current_fuel,

            "fuel_correction": fuel_correction,

            "cumulative_time": cumulative_time
        })

        fuel.burnFuel()

    return {
        "total_time": cumulative_time,
        "laps": results
    }


# Testing

if __name__ == "__main__":

    result = simulate_stint(
        track="bahrain_2022",
        compound="MEDIUM",
        total_laps=15
    )

    print("\nSTINT SIMULATION\n")

    previous_lap_time = None

    for lap in result["laps"]:

        if previous_lap_time is None:
            delta = 0

        else:
            delta = (
                lap["lap_time"]
                - previous_lap_time
            )

        print(
            f"Lap {lap['lap']:>2} | "
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