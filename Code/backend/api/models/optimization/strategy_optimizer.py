from api.models.optimization.strategy_generator import (
    generate_strategies
)

from api.models.simulation.strategy_simulation import (
    simulate_strategy
)

from api.models.optimization.monte_carlo_simulator import(
    run_monte_carlo
)

def strategy_optimizer(track, total_laps,risk_factor):
    
    risk_factor = 1.0 

    strategies = generate_strategies(total_laps)

    results = []

    for strategy in strategies:
        
        mc_result = run_monte_carlo(
            strategy=strategy,
            track = track,
            simulations = 100
        )
        
        average_time = mc_result["average_time"]
        
        std_dev = mc_result["std_dev"]
        
        risk_penalty = risk_factor * std_dev
        
        strategy_score = ( average_time + risk_penalty )

        simulation = simulate_strategy(
            track=track,
            strategy=strategy
        )

        average_lap = (
            simulation["total_time"]
            / total_laps
        )

        compounds_used = list(
            set(
                compound
                for compound, _ in strategy
            )
        )

        strategy_type = (
            f"{len(strategy)-1}-stop"
        )

        results.append({
            
            "average_time": average_time,
            
            "std_dev": std_dev,
            
            "strategy_score": strategy_score,

            "strategy": strategy,

            "strategy_type": strategy_type,

            "total_time": simulation["total_time"],

            "average_lap_time": average_lap,

            "pitstops": simulation["pitstops"],

            "stint_count": len(strategy),

            "compounds_used": compounds_used,

            "total_laps": total_laps
        })

    sorted_results = sorted(
        results,
        key=lambda x: x["strategy_score"]
    )

    unique_strategies = {}

    for result in sorted_results:

        strategy_key = tuple(result["strategy"])

        if strategy_key not in unique_strategies:

            unique_strategies[strategy_key] = result

    return list(
        unique_strategies.values()
    )[:20]


if __name__ == "__main__":

    best = strategy_optimizer(
        track="monza_2022",
        total_laps=57,
        risk_factor=0.2 #convervative risk factor
    )

    print("\nTOP STRATEGIES\n")

    for i, result in enumerate(best, start=1):

        print(f"{i}.")

        print(
            f"Strategy: "
            f"{result['strategy']}"
        )

        print(
            f"Strategy Type: "
            f"{result['strategy_type']}"
        )

        print(
            f"Total Time: "
            f"{result['total_time']:.3f}"
        )

        print(
            f"Average Lap: "
            f"{result['average_lap_time']:.3f}"
        )

        print(
            f"Pit Stops: "
            f"{result['pitstops']}"
        )

        print(
            f"Compounds Used: "
            f"{result['compounds_used']}"
        )

        print(
            f"Stint Count: "
            f"{result['stint_count']}"
        )

        print(
            f"Total Laps: "
            f"{result['total_laps']}"
        )
               
        print(
            f"Average Time: "
            f"{result['average_time']:.3f}"
        )

        print(
            f"Std Dev: "
            f"{result['std_dev']:.3f}"
        )

        print(
            f"Strategy Score: "
            f"{result['strategy_score']:.3f}"
        )
        
        print("-" * 40)