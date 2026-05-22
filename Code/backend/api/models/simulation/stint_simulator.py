from typing import List, Dict, Any

from api.models.simulation.lap_time_engine import (
    compute_lap_time
)

from api.models.simulation.fuel_state import (
    FuelState
)

from api.models.simulation.track_model import (
    get_track_parameters
)
#Stint Sim

def simulate_stint(
    track: str,
    compound: str,
    total_laps: int
) -> Dict[str, Any]:

    results: List[Dict[str, Any]] = []

    cumulative_time: float = 0.0

    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8,
        fuel_effect_per_kg=0.028
    )

    track_data = get_track_parameters(track)

    warmup_map = track_data["warmup_penalty"]

    for lap in range(total_laps):

        current_lap: int = lap + 1
        tyre_age: int = current_lap

        warmup_penalty: float = 0.0

        if tyre_age <= 2:
            warmup_penalty = float(
                warmup_map[compound]
            )

        fuel_correction: float = (
            fuel.getFuelCorrection()
        )

        lap_data: Dict[str, Any] = compute_lap_time(
            track=track,
            compound=compound,
            tyre_age=tyre_age,
            fuel_correction=fuel_correction
        )

        corrected_lap_time: float = (
            float(lap_data["lap_time"])
            + warmup_penalty
        )

        cumulative_time += corrected_lap_time

        results.append({

            "lap": current_lap,

            "tyre_age": tyre_age,

            "lap_time": corrected_lap_time,

            "warmup_penalty": warmup_penalty,

            "fuel_load": float(
                fuel.current_fuel
            ),

            "fuel_correction": fuel_correction,

            "cumulative_time": cumulative_time
        })

        fuel.burnFuel()

    return {

        "total_time": cumulative_time,

        "laps": results
    }


# =========================
# TESTING
# =========================

# if __name__ == "__main__":

#     result = simulate_stint(
#         track="bahrain_2022",
#         compound="MEDIUM",
#         total_laps=15
#     )

#     print("\nSTINT SIMULATION\n")

#     previous_lap_time = None

#     for lap in result["laps"]:

#         if previous_lap_time is None:
#             delta = 0.0

#         else:
#             delta = (
#                 lap["lap_time"]
#                 - previous_lap_time
#             )

#         print(
#             f"Lap {lap['lap']:>2} | "
#             f"Tyre Age: {lap['tyre_age']:>2} | "
#             f"Fuel: {lap['fuel_load']:.2f} kg | "
#             f"Lap Time: {lap['lap_time']:.3f} | "
#             f"Warmup: {lap['warmup_penalty']:.2f} | "
#             f"Delta: {delta:+.3f} | "
#             f"Cumulative: {lap['cumulative_time']:.3f}"
#         )

#         previous_lap_time = lap["lap_time"]

#     print(
#         f"\nTotal Stint Time: "
#         f"{result['total_time']:.3f}"
#     )