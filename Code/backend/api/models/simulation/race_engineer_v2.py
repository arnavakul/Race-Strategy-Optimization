def generate_race_engineer_report(
    race_state,recommendation
):
    
    action = recommendation[
        "recommended_action"
    ]

    expected_finish = recommendation[
        "expected_finish"
    ]

    confidence = recommendation[
        "confidence"
    ]
    
    strategy_reason = recommendation[
        "reason"
    ]
    
    podium_probability = recommendation[
        "podium_probability"
    ]
    
    win_probability = recommendation[
        "win_probability"
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

    elif weather == "WET":

        weather_comment = (
            "Wet conditions expected."
        )

    else:

        weather_comment = (
            "Weather forecast unavailable."
        )

    return {

        "strategy_call":
            action_text,

        "expected_finish":
            expected_finish,

        "podium_probability":
            podium_probability,

        "win_probability":
            win_probability,

        "confidence":
            confidence,

        "strategy_reason":
            strategy_reason,

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

    print(
        "\n================================="
    )

    print(
        "RACE ENGINEER STRATEGY REPORT"
    )

    print(
        "=================================\n"
    )

    print(
        f"STRATEGY CALL : "
        f"{report['strategy_call']}"
    )

    print(
        f"EXPECTED FINISH : "
        f"P{report['expected_finish']}"
    )

    print(
        f"PODIUM CHANCE : "
        f"{report['podium_probability']}%"
    )

    print(
        f"WIN CHANCE : "
        f"{report['win_probability']}%"
    )

    print(
        f"CONFIDENCE : "
        f"{report['confidence']}"
    )

    print(
        f"\nREASON : "
        f"{report['strategy_reason']}"
    )

    print(
        f"\nTYRES : "
        f"{report['tyre_analysis']}"
    )

    print(
        f"\nPOSITION : "
        f"{report['position_analysis']}"
    )

    print(
        f"\nWEATHER : "
        f"{report['weather_analysis']}"
    )