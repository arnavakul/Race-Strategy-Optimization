from api.models.simulation.stint_simulator import (
    simulate_stint
)

from api.models.simulation.pitstop_model import (
    get_pitstop_time
)



def simulate_strategy(track, strategy,weather_timeline):

    total_race_time = 0
    all_laps = []
    pit_count = 0

    for i, (compound, laps) in enumerate(strategy):

        # simulate stint

        stint_result = simulate_stint(
            track=track,
            compound=compound,
            total_laps=laps,
            weather_timeline=weather_timeline
        )

        # add stint race time

        total_race_time += stint_result["total_time"]

        # store lap-by-lap data

        all_laps.extend(
            stint_result["laps"]
        )

        # check if current stint
        # is NOT the final stint

        is_final_stint = (
            i == len(strategy) - 1
        )

        # add pitstop time
        # after every stint except final

        if not is_final_stint:

            pit_loss = get_pitstop_time(track)

            total_race_time += pit_loss

            pit_count += 1
            print(stint_result["laps"][:5])
            

    return {
        "strategy": strategy,
        "total_time": total_race_time,
        "pitstops": pit_count,
        "laps": all_laps
    }


if __name__ == "__main__":

    strategy = [
        ("SOFT", 12),
        ("MEDIUM", 20),
        ("HARD", 25)
    ]

    result = simulate_strategy(
        track="bahrain_2022",
        strategy=strategy,
        weather_timeline="MIXED"
    )

    print("\nSTRATEGY SIMULATION\n")

    print("Strategy:", result["strategy"])
    print("Total Race Time:", result["total_time"])
    print("Pit Stops:", result["pitstops"])
    print("Total Laps:", len(result["laps"]))
    print("Weather :", (result["weather"]))
