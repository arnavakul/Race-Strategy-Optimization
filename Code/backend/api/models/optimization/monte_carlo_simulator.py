from api.models.simulation.strategy_simulation import (
    simulate_strategy
)

from api.models.simulation.weather_model import(
    generate_weather_state,generate_weather_timeline
)

import random
import statistics


def run_monte_carlo(
    strategy,
    track,
    simulations=100,
    seed=None
):

    race_times = []

    clean_race_times = []

    safety_car_race_times = []

    if seed is not None:

        random.seed(seed)

    safety_car_count = 0
    
    dry_count = 0

    mixed_count = 0

    wet_count = 0

    for sim in range(simulations):
        
        weather_timeline = (generate_weather_timeline(57))   
        
        if weather_timeline == "DRY":
            dry_count +=1 
        elif weather_timeline == "MIXED":
            mixed_count +=1
        elif weather_timeline == "WET":
            wet_count += 1

        results = simulate_strategy(
            track,
            strategy,
            weather_timeline
        )

        total_time = results["total_time"]            
        safety_car = False

        if random.random() < 0.3:

            safety_car = True

            safety_car_count += 1

            sc_effect = random.uniform(
                -15,
                8
            )

            total_time += sc_effect

        race_variation = random.uniform(
            -3,
            3
        )

        total_time += race_variation

        if safety_car:

            safety_car_race_times.append(
                total_time
            )

        else:

            clean_race_times.append(
                total_time
            )

        race_times.append(
            total_time
        )

    if clean_race_times:

        clean_race_average = statistics.mean(
            clean_race_times
        )

    else:

        clean_race_average = None

    if safety_car_race_times:

        safety_car_race_average = statistics.mean(
            safety_car_race_times
        )

    else:

        safety_car_race_average = None

    safety_car_rate = (
        safety_car_count /
        simulations
    )

    average_time = statistics.mean(
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

    return {

        "average_time": average_time,

        "best_case": best_case,

        "worst_case": worst_case,

        "std_dev": std_dev,

        "race_times": race_times,

        "safety_car_count": safety_car_count,

        "safety_car_rate": safety_car_rate,

        "clean_race_average": clean_race_average,

        "safety_car_race_average": (
            safety_car_race_average
        ),
        
        "dry_count": dry_count,

        "mixed_count": mixed_count,

        "wet_count": wet_count,
    }



# DEBUGGING TEST INPUTS

if __name__ == "__main__":

    strategy = [
        ("SOFT", 15),
        ("HARD", 42)
    ]

    results = run_monte_carlo(
        strategy=strategy,
        track="bahrain_2022",
        simulations=10,
        # seed=42
    )

    print("Average Time: ",results["average_time"])

    print("Best Race Time: ",results["best_case"])

    print("Worst Race Time: ",results["worst_case"])

    print("Standard Deviations: ",results["std_dev"])

    print("Safety Car Count: ",results["safety_car_count"])

    print("Rate of Safety Car(Safety car probability): ",results["safety_car_rate"]*100,"%")

    print("Clear Average Race: ",results["clean_race_average"])

    print("Safety Car Average Race: ",results["safety_car_race_average"])
