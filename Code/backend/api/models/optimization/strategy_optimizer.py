from api.models.optimization.strategy_generator import (
    generate_strategies
)

from api.models.simulation.strategy_simulation import (
    simulate_strategy
)


def strategy_optimizer(track, total_laps):

    strategies = generate_strategies(total_laps)

    results = []

    for strategy in strategies:

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
        key=lambda x: x["total_time"]
    )

    unique_strategies = {}

    for result in sorted_results:

        compounds = tuple(
            compound
            for compound, _
            in result["strategy"]
        )

        if compounds not in unique_strategies:

            unique_strategies[compounds] = result

    return list(
        unique_strategies.values()
    )[:20]


if __name__ == "__main__":

    best = strategy_optimizer(
        track="monza_2022",
        total_laps=57
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

        print("-" * 40)