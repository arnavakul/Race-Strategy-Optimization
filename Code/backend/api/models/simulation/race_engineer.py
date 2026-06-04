def generate_race_engineer_report(race_state, recommendation):
    
    action = recommendation["action"]
    
    expected_finish = recommendation[
        "expected_finish"
    ]
    
    confidence = recommendation[
        "confidence"
    ]
    
    if action == "PIT_NOW":

        recommendation_text = (
            "Pit immediately"
        )

    elif action == "PIT_PLUS_2":

        recommendation_text = (
            "Extend stint by 2 laps"
        )

    elif action == "PIT_PLUS_5":

        recommendation_text = (
            "Extend stint by 5 laps"
        )

    else:

        recommendation_text = (
            "Stay out"
        )
        
    tyre_age = race_state["tyre_age"]
    
    if tyre_age > 25:

        tyre_comment = (
            "Tyres are heavily degraded"
        )

    elif tyre_age > 15:

        tyre_comment = (
            "Tyres are approaching cliff"
        )

    else:

        tyre_comment = (
            "Tyres remain competitive"
        )
    
    position = race_state["position"]
    
    if position <= 3:

        position_comment = (
            "Currently in podium position"
        )

    elif position <= 10:

        position_comment = (
            "Currently in points position"
        )

    else:

        position_comment = (
            "Outside points positions"
        )
    
    weather = race_state["weather"]
    
    if weather == "DRY":

        weather_comment = (
            "Dry conditions"
        )

    elif weather == "MIXED":

        weather_comment = (
            "Rain threat present"
        )

    else:

        weather_comment = (
            "Wet conditions"
        )
    
    compound = race_state["compound"]

    if compound == "SOFT":

        compound_comment = (
            "High pace but high degradation"
        )

    elif compound == "MEDIUM":

        compound_comment = (
            "Balanced tyre strategy"
        )

    elif compound == "HARD":

        compound_comment = (
            "Long stint tyre"
        )

    elif compound == "INTERMEDIATE":

        compound_comment = (
            "Suitable for mixed conditions"
        )

    else:

        compound_comment = (
            "Full wet tyre in use"
        )
    return {

    "recommendation":
        recommendation_text,

    "expected_finish":
        expected_finish,

    "confidence":
        confidence,

    "tyre_analysis":
        tyre_comment,

    "position_analysis":
        position_comment,

    "weather_analysis":
        weather_comment,
    
    "compound_analysis":
        compound_comment,
    }



#TESTING BLOCK

if __name__ == "__main__":

    race_state = {

        "current_lap": 34,

        "position": 4,

        "compound": "MEDIUM",

        "tyre_age": 18,

        "weather": "DRY"
    }

    recommendation = {

        "action": "PIT_NOW",

        "expected_finish": 2,

        "confidence": 74.2
    }

    report = (
        generate_race_engineer_report(
            race_state,
            recommendation
        )
    )

    print(report)