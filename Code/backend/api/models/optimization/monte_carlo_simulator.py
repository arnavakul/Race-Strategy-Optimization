import random
import statistics

from api.models.simulation.race_executor import (
    execute_race
)


def run_monte_carlo(
    track,
    starting_compound,
    total_laps,
    simulations=100,
    seed=None
):

    if seed is not None:

        random.seed(seed)

    race_times = []

    safety_car_deployments = []

    vsc_deployments = []

    legal_races = 0

    for sim in range(simulations):

        result = execute_race(

            track=track,

            starting_compound=starting_compound,

            total_laps=total_laps
        )

        race_times.append(
            result["total_time"]
        )

        safety_car_deployments.append(

            result[
                "safety_car_deployments"
            ]
        )

        vsc_deployments.append(

            result[
                "vsc_deployments"
            ]
        )

        if result["legal_race"]:

            legal_races += 1

    race_times.sort()

    average_time = statistics.mean(
        race_times
    )

    median_time = statistics.median(
        race_times
    )

    best_case = min(
        race_times
    )

    worst_case = max(
        race_times
    )

    std_dev = statistics.stdev(
        race_times
    )

    p5 = race_times[
        int(
            len(race_times) * 0.05
        )
    ]

    p95 = race_times[
        int(
            len(race_times) * 0.95
        )
    ]

    average_sc = statistics.mean(
        safety_car_deployments
    )

    average_vsc = statistics.mean(
        vsc_deployments
    )

    legality_rate = (
        legal_races
        / simulations
    )

    return {

        "simulations": simulations,

        "average_time": average_time,

        "median_time": median_time,

        "best_case": best_case,

        "worst_case": worst_case,

        "std_dev": std_dev,

        "p5": p5,

        "p95": p95,

        "average_sc": average_sc,

        "average_vsc": average_vsc,

        "legality_rate": legality_rate,

        "race_times": race_times
    }

# TESTING

if __name__ == "__main__":

    results = run_monte_carlo(

        track="bahrain_2022",

        starting_compound="SOFT",

        total_laps=57,

        simulations=100
    )

    print("\nMONTE CARLO RESULTS\n")

    print(
        "Simulations:",
        results["simulations"]
    )

    print(
        "Average Time:",
        round(
            results["average_time"],
            3
        )
    )

    print(
        "Median Time:",
        round(
            results["median_time"],
            3
        )
    )

    print(
        "Best Case:",
        round(
            results["best_case"],
            3
        )
    )

    print(
        "Worst Case:",
        round(
            results["worst_case"],
            3
        )
    )

    print(
        "Std Dev:",
        round(
            results["std_dev"],
            3
        )
    )

    print(
        "P5:",
        round(
            results["p5"],
            3
        )
    )

    print(
        "P95:",
        round(
            results["p95"],
            3
        )
    )

    print(
        "Average SC Deployments:",
        round(
            results["average_sc"],
            2
        )
    )

    print(
        "Average VSC Deployments:",
        round(
            results["average_vsc"],
            2
        )
    )

    print(
        "Legality Rate:",
        round(
            results["legality_rate"] * 100,
            2
        ),
        "%"
    )