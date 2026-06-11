def generate_race_engineer_report(
    race_state,recommendation
):
    
    action = recommendation[
        "recommended_action"
    ]

    expected_position = recommendation[
        "expected_position"
    ]

    confidence = recommendation[
        "confidence"
    ]
    
    if action == "PIT_NOW":

        action_text = (
            "Pit this lap."
        )

    elif action == "PIT_PLUS_3":

        action_text = (
            "Extend stint by 3 laps."
        )

    elif action == "PIT_PLUS_5":

        action_text = (
            "Extend stint by 5 laps."
        )

    else:

        action_text = (
            "Stay out."
        )
    
    tyre_age = race_state["tyre_age"]
    
    if tyre_age > 25:

        tyre_comment = (
            "Tyres are heavily degraded."
        )

    elif tyre_age > 15:

        tyre_comment = (
            "Tyres are approaching the cliff."
        )

    else:

        tyre_comment = (
            "Tyres remain competitive."
        )
        
    position = race_state["position"]
    
    if position <= 3:

        position_comment = (
            "Currently running in podium positions."
        )

    elif position <= 10:

        position_comment = (
            "Currently scoring points."
        )

    else:

        position_comment = (
            "Currently outside points positions."
        )
    
    weather = race_state.get(
        "weather",
        "UNKNOWN"
    )
    
    if weather == "DRY":

        weather_comment = (
            "Dry conditions expected."
        )

    elif weather == "MIXED":

        weather_comment = (
            "Rain threat present."
        )

    else:

        weather_comment = (
            "Wet conditions expected."
        )
    
    return {

        "strategy_call":
            action_text,

        "expected_position":
            expected_position,

        "confidence":
            confidence,

        "tyre_analysis":
            tyre_comment,

        "position_analysis":
            position_comment,

        "weather_analysis":
            weather_comment
    }

if __name__ == "__main__":

    race_state = {

        "position": 4,

        "tyre_age": 18,

        "weather": "DRY"
    }

    recommendation = {

        "recommended_action": "PIT_NOW",

        "expected_position": 3,

        "confidence": 70
    }

    report = generate_race_engineer_report(

        race_state,

        recommendation
    )

    print("\nRACE ENGINEER REPORT\n")

    for key, value in report.items():

        print(f"{key}: {value}")