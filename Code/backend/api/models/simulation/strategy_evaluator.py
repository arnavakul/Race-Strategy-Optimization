# strategy_evaluator.py


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

    # tyre condition

    if tyre_age > 20:
        score += 30

    if tyre_age > 30:
        score += 20

    # attack opportunity

    if (
        gap_ahead is not None
        and gap_ahead < 2
    ):
        score += 15

    # defend undercut

    if (
        gap_behind is not None
        and gap_behind < 2
    ):
        score += 10

    # weather uncertainty

    if weather != "DRY":
        score -= 20

    # race position

    if position == 1:
        score -= 15

    if position >= 4:
        score += 10

    # late race

    if laps_remaining < 8:
        score -= 50

    # action specific

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

        "score": score
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

        results.append(result)

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