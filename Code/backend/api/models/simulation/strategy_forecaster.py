def forecast_strategy(
    race_state,
    strategy_action
):

    current_lap = race_state["current_lap"]

    total_laps = race_state["total_laps"]

    position = race_state["position"]

    tyre_age = race_state["tyre_age"]

    laps_remaining = (
        total_laps - current_lap
    )

    predicted_finish = position

    action_name = (
        strategy_action["action"]
    )

    fresh_tyre_bonus = 0

    if action_name == "PIT_NOW":

        fresh_tyre_bonus = 2

    elif action_name == "PIT_PLUS_2":

        fresh_tyre_bonus = 1

    elif action_name == "PIT_PLUS_5":

        fresh_tyre_bonus = 0

    elif action_name == "STAY_OUT":

        fresh_tyre_bonus = 0

    if tyre_age > 20:

        predicted_finish += 1

    if tyre_age > 30:

        predicted_finish += 2

    predicted_finish -= fresh_tyre_bonus

    predicted_finish = max(
        1,
        predicted_finish
    )

    predicted_time = (
        laps_remaining * 88
    )

    return {

        "action":
            action_name,

        "expected_finish":
            predicted_finish,

        "predicted_time":
            predicted_time
    }