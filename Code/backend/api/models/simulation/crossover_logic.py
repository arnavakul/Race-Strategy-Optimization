SLICK_COMPOUNDS = [
    "SOFT",
    "MEDIUM",
    "HARD"
]
WET_COMPOUNDS = [
    "INTERMEDIATE",
    "WET"
]

def should_pit_for_weather(current_compound, current_weather):
    
    if current_weather == "MIXED":
        if current_compound in SLICK_COMPOUNDS:
            return True
    
    elif current_weather == "WET":
        if current_compound not in WET_COMPOUNDS:
            return True
    elif current_weather == "DRY":
        if current_compound in WET_COMPOUNDS:
            return True
    return False

def get_recommended_compound(weather_state):
    if weather_state == "DRY":
        return "MEDIUM"
    elif weather_state == "MIXED":
        return "INTERMEDIATE"
    elif weather_state == "WET":
        return "WET"
    return "MEDIUM"

#Testing
if __name__ == "__main__":

    print("\nCROSSOVER LOGIC TESTS\n")

    print(
        "SOFT in WET:",
        should_pit_for_weather(
            "SOFT",
            "WET"
        )
    )

    print(
        "WET in DRY:",
        should_pit_for_weather(
            "WET",
            "DRY"
        )
    )

    print(
        "INTERMEDIATE in MIXED:",
        should_pit_for_weather(
            "INTERMEDIATE",
            "MIXED"
        )
    )

    print(
        "Recommended for DRY:",
        get_recommended_compound(
            "DRY"
        )
    )

    print(
        "Recommended for MIXED:",
        get_recommended_compound(
            "MIXED"
        )
    )

    print(
        "Recommended for WET:",
        get_recommended_compound(
            "WET"
        )
    )