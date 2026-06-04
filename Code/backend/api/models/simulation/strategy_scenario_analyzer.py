def generate_scenarios(race_state):

    scenarios = [

        "PIT_NOW",

        "PIT_PLUS_3",

        "PIT_PLUS_5",

        "STAY_OUT",

        "SAFETY_CAR_NEXT_5",

        "VSC_NEXT_5",

        "RAIN_IN_10"
    ]

    return scenarios


def analyze_scenario(
    race_state,
    scenario
):

    predicted_finish = (
        race_state["position"]
    )

    if scenario == "PIT_NOW":

        predicted_finish -= 1

    elif scenario == "PIT_PLUS_3":

        predicted_finish += 0

    elif scenario == "PIT_PLUS_5":

        predicted_finish += 1

    elif scenario == "STAY_OUT":

        predicted_finish += 1

    elif scenario == "SAFETY_CAR_NEXT_5":

        predicted_finish -= 2

    elif scenario == "VSC_NEXT_5":

        predicted_finish -= 1

    elif scenario == "RAIN_IN_10":

        predicted_finish += 1

    predicted_finish = max(
        1,
        predicted_finish
    )

    return {

        "scenario": scenario,

        "expected_finish":
            predicted_finish
    }


def run_scenario_analysis(
    race_state
):

    scenarios = generate_scenarios(
        race_state
    )

    results = []

    for scenario in scenarios:

        result = analyze_scenario(
            race_state,
            scenario
        )

        results.append(
            result
        )

    return results


if __name__ == "__main__":

    race_state = {

        "current_lap": 34,

        "position": 4,

        "compound": "MEDIUM",

        "tyre_age": 17,

        "weather": "DRY"
    }

    results = run_scenario_analysis(
        race_state
    )

    for result in results:

        print(result)