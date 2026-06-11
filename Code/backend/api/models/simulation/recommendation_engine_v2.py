from api.models.simulation.strategy_scenario_analyzer import (
    generate_scenarios
)



from api.models.simulation.monte_carlo_strategy_evaluator import (
    run_strategy_monte_carlo
)

def generate_recommendation(race_state):
    scenarios = generate_scenarios(race_state)
    
    scenario_results = []
    
    for scenario in scenarios:
        result = run_strategy_monte_carlo(
            race_state,scenario,simulations=100
        )
        
        scenario_results.append(
            result
        )
        
    best_scenario = min(

        scenario_results,

        key=lambda x:(

            x["average_finish"],

            -x["podium_probability"],

            -x["win_probability"]
        )
    )
    
    confidence = "LOW"

    if best_scenario["podium_probability"] >= 70:

        confidence = "HIGH"

    elif best_scenario["podium_probability"] >= 40:

        confidence = "MEDIUM"
        
    reason = (
        f"Highest podium probability "
        f"({best_scenario['podium_probability']}%)"
    )
        
    return {

        "recommended_action":
            best_scenario["scenario"],

        "expected_finish":
            round(
                best_scenario[
                    "average_finish"
                ],
                1
            ),

        "podium_probability":
            best_scenario[
                "podium_probability"
            ],

        "win_probability":
            best_scenario[
                "win_probability"
            ],

        "confidence":
            confidence,

        "reason":
            reason,

        "all_scenarios":
            scenario_results
    }

if __name__ == "__main__":

    race_state = {

        "position": 4,

        "current_lap": 34,

        "total_laps": 57,

        "tyre_age": 18,

        "compound": "MEDIUM"
    }

    recommendation = (

        generate_recommendation(
            race_state
        )
    )

    print(
        "\nBEST STRATEGY\n"
        )

    print("\n========== BEST STRATEGY ==========\n")

    print(
        f"Recommended Action : "
        f"{recommendation['recommended_action']}"
    )

    print(
        f"Expected Finish    : "
        f"P{recommendation['expected_finish']}"
    )

    print(
        f"Podium Probability : "
        f"{recommendation['podium_probability']}%"
    )

    print(
        f"Win Probability    : "
        f"{recommendation['win_probability']}%"
    )

    print(
        f"Confidence         : "
        f"{recommendation['confidence']}"
    )

    print(
        f"Reason             : "
        f"{recommendation['reason']}"
    )
    
    print("\n========== SCENARIO COMPARISON ==========\n")

    for scenario in recommendation[
        "all_scenarios"
    ]:

        print(
            f"{scenario['scenario']:12} | "
            f"Finish: P{scenario['average_finish']:.2f} | "
            f"Podium: {scenario['podium_probability']:>5.1f}% | "
            f"Win: {scenario['win_probability']:>5.1f}%"
        )