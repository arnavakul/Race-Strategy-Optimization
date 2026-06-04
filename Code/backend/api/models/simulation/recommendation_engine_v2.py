from api.models.simulation.strategy_scenario_analyzer import (
    generate_scenarios
)

# from api.models.simulation.scenario_forecaster import (
#     forecast_scenario
# )

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
        
    return {

        "recommended_action":
            best_scenario["scenario"],

        "average_finish":
            best_scenario["average_finish"],

        "podium_probability":
            best_scenario[
                "podium_probability"
            ],

        "win_probability":
            best_scenario[
                "win_probability"
            ],

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

    print(recommendation)