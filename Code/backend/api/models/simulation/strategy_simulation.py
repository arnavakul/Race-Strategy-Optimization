strategy = [
    ("SOFT", 12),
    ("MEDIUM", 20),
    ("HARD", 25)
]

from stint_simulator import simulate_stint
from pitstop_model import get_pitstop_time


def simulate_strategy(track, strategy):

    total_race_time = 0
    all_laps = []
    pit_count = 0

    for i, (compound, laps) in enumerate(strategy):

        stint_result = simulate_stint(
            track=track,
            compound=compound,
            total_laps=laps
        )

        total_race_time += stint_result["total_time"]

        all_laps.extend(stint_result["laps"])

        is_final_stint = i == len(strategy) - 1

        if not is_final_stint:

            pit_loss = get_pitstop_time(track)

            total_race_time += pit_loss

            pit_count += 1

    return {
        "strategy": strategy,
        "total_time": total_race_time,
        "pit_stops": pit_count,
        "laps": all_laps
    }
if __name__ == "__main__":

    result = simulate_strategy(
        track="bahrain_2022",
        strategy=strategy
    )

    print("Total Race Time:", result["total_time"])
    print("Pit Stops:", result["pit_stops"])
    print("Total Laps:", len(result["laps"]))