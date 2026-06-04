# scenario_forecaster.py


def forecast_scenario(
    race_state,
    scenario
):

    # CURRENT RACE STATE

    current_position = (
        race_state["position"]
    )

    current_lap = (
        race_state["current_lap"]
    )

    total_laps = (
        race_state["total_laps"]
    )

    tyre_age = (
        race_state["tyre_age"]
    )

    compound = (
        race_state["compound"]
    )

    # LAPS REMAINING

    laps_remaining = (
        total_laps - current_lap
    )

    # BASELINE FORECAST

    predicted_finish = (
        current_position
    )

    predicted_time = (
        laps_remaining * 88
    )

    confidence = 70

    # SCENARIO EFFECTS

    if scenario == "PIT_NOW":

        predicted_finish -= 1

        predicted_time -= 5

    elif scenario == "PIT_PLUS_3":

        predicted_time -= 2

    elif scenario == "PIT_PLUS_5":

        predicted_finish += 1

    elif scenario == "STAY_OUT":

        predicted_finish += 2

    elif scenario == "SAFETY_CAR_NEXT_5":

        predicted_finish -= 2

        predicted_time -= 8

        confidence -= 15

    elif scenario == "VSC_NEXT_5":

        predicted_finish -= 1

        predicted_time -= 4

        confidence -= 10

    elif scenario == "RAIN_IN_10":

        predicted_finish += 1

        confidence -= 20

    # TYRE AGE EFFECT

    if tyre_age > 20:

        predicted_finish += 1

        confidence -= 5

    if tyre_age > 30:

        predicted_finish += 2

        confidence -= 10

    # COMPOUND BONUS

    if compound == "SOFT":

        predicted_finish -= 1

    # SAFETY LIMITS

    predicted_finish = max(
        1,
        int(predicted_finish)
    )

    confidence = max(
        0,
        min(confidence, 100)
    )

    # OUTPUT

    return {

        "scenario": scenario,

        "expected_finish": predicted_finish,

        "expected_race_time": predicted_time,

        "confidence": confidence
    }


# TESTING BLOCK

if __name__ == "__main__":

    race_state = {

        "position": 4,

        "current_lap": 34,

        "total_laps": 57,

        "tyre_age": 18,

        "compound": "MEDIUM"
    }

    scenarios = [

        "PIT_NOW",

        "PIT_PLUS_3",

        "PIT_PLUS_5",

        "STAY_OUT",

        "SAFETY_CAR_NEXT_5",

        "VSC_NEXT_5",

        "RAIN_IN_10"
    ]

    print("\nSCENARIO FORECASTS\n")

    for scenario in scenarios:

        result = forecast_scenario(

            race_state,

            scenario
        )

        print(result)