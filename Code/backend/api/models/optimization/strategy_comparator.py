from api.models.optimization.race_variability_monte_carlo import (
    run_strategy_monte_carlo
)


def compare_strategies(
    strategies,
    track,
    simulations=20
):

    results = []

    for strategy in strategies:

        mc_result = run_strategy_monte_carlo(

            strategy=strategy,

            track=track,

            simulations=simulations
        )

        results.append({

            "strategy": strategy,

            "average_time":
                mc_result["average_time"],

            "std_dev":
                mc_result["std_dev"],

            "p5":
                mc_result["p5"],

            "p95":
                mc_result["p95"],

            "best_case":
                mc_result["best_case"],

            "worst_case":
                mc_result["worst_case"]
        })

    # Sort by fastest average race time

    results.sort(

        key=lambda x: x["average_time"]
    )

    # Assign ranks

    for rank, result in enumerate(

        results,

        start=1
    ):

        result["rank"] = rank

    return results


if __name__ == "__main__":

    strategies = [

        [
            ("SOFT", 20),
            ("HARD", 37)
        ],

        [
            ("MEDIUM", 21),
            ("HARD", 36)
        ],

        [
            ("HARD", 38),
            ("SOFT", 19)
        ]
    ]

    results = compare_strategies(

        strategies=strategies,

        track="monza_2022",

        simulations=20
    )

    print("\nSTRATEGY COMPARISON\n")

    for result in results:

        print(
            f"\nRank {result['rank']}"
        )

        print(
            f"Strategy: "
            f"{result['strategy']}"
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
            f"P5: "
            f"{result['p5']:.3f}"
        )

        print(
            f"P95: "
            f"{result['p95']:.3f}"
        )

        print(
            f"Best Case: "
            f"{result['best_case']:.3f}"
        )

        print(
            f"Worst Case: "
            f"{result['worst_case']:.3f}"
        )

        print("-" * 50)