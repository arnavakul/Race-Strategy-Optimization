# strategy_evaluator.py

from api.models.simulation.pit_window_model import (
    evaluate_pit_window
)

from api.models.simulation.traffic_model import (
    in_traffic
)

from api.models.simulation.overtake_model import (
    calculate_overtake_probability
)


def generate_candidate_actions(
    current_lap,
    total_laps
):

    actions = []

    actions.append({
        "action": "PIT_NOW",
        "pit_lap": current_lap
    })

    actions.append({
        "action": "PIT_PLUS_2",
        "pit_lap": current_lap + 2
    })

    actions.append({
        "action": "PIT_PLUS_5",
        "pit_lap": current_lap + 5
    })

    actions.append({
        "action": "STAY_OUT",
        "pit_lap": None
    })

    return actions


def score_action(
    action,
    race_state
):

    score = 50

    risk = 0

    current_lap = race_state["current_lap"]

    total_laps = race_state["total_laps"]

    position = race_state["position"]

    tyre_age = race_state["tyre_age"]

    gap_ahead = race_state["gap_ahead"]

    gap_behind = race_state["gap_behind"]

    weather = race_state["weather"]

    laps_remaining = (
        total_laps
        - current_lap
    )

    # MODEL INTEGRATIONS

    pit_window = evaluate_pit_window(
        tyre_age,
        25
    )

    traffic = in_traffic(
        gap_ahead
    )

    overtake_probability = (
        calculate_overtake_probability(
            tyre_advantage=1,
            pace_advantage=1
        )
    )

    # OVERTAKE PROBABILITY

    if overtake_probability > 0.5:

        score -= 10

    # TRAFFIC

    if traffic:

        score += 15

    # TYRE CONDITION

    if pit_window == "OPTIMAL":

        score += 30

    elif pit_window == "EARLY":

        score -= 10

    elif pit_window == "LATE":

        score += 40

    # ATTACK OPPORTUNITY

    if (
        gap_ahead is not None
        and gap_ahead < 2
    ):

        score += 15

    # DEFEND UNDERCUT

    if (
        gap_behind is not None
        and gap_behind < 2
    ):

        score += 10

    # WEATHER UNCERTAINTY

    if weather != "DRY":

        score -= 20

        risk += 25

    # RACE POSITION

    if position == 1:

        score -= 15

    if position >= 4:

        score += 10

    # LATE RACE

    if laps_remaining < 8:

        score -= 50

    # RISK MODEL

    if tyre_age > 25:

        risk += 20

    if (
        gap_behind is not None
        and gap_behind < 1
    ):

        risk += 15

    # ACTION SPECIFIC


    if action["action"] == "PIT_NOW":

        score += 10

    elif action["action"] == "PIT_PLUS_2":

        score += 5

    elif action["action"] == "PIT_PLUS_5":

        score -= 5

    elif action["action"] == "STAY_OUT":

        score -= 10

    return {

        "action": action["action"],

        "pit_lap": action["pit_lap"],

        "score": score,

        "risk": risk
    }


def evaluate_strategy_options(
    race_state
):

    actions = generate_candidate_actions(

        race_state["current_lap"],

        race_state["total_laps"]
    )

    results = []

    for action in actions:

        result = score_action(
            action,
            race_state
        )

        results.append(
            result
        )

    best_action = max(

        results,

        key=lambda x: x["score"]
    )

    return {

        "recommended_action":
            best_action,

        "all_options":
            results
    }


if __name__ == "__main__":

    race_state = {

        "current_lap": 35,

        "total_laps": 57,

        "position": 4,

        "tyre_age": 18,

        "gap_ahead": 1.5,

        "gap_behind": 2.0,

        "weather": "DRY"
    }

    result = evaluate_strategy_options(
        race_state
    )

    print("\nRECOMMENDATION\n")

    print(
        result["recommended_action"]
    )

    print("\nALL OPTIONS\n")

    for option in result["all_options"]:

        print(option)