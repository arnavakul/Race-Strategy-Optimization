import random

WEATHER_STATES = [
    "DRY",
    "MIXED",
    "WET"
]

WEATHER_PROBABILITIES = {
    "DRY": 0.7,
    "MIXED": 0.2,
    "WET": 0.1
}

WEATHER_TYRE_EFFECTS = {
    
}

def generate_weather_state():
    weather_state = random.choices(
        WEATHER_STATES, 
        weights=[
            WEATHER_PROBABILITIES["DRY"],
            WEATHER_PROBABILITIES["MIXED"],
            WEATHER_PROBABILITIES["WET"]
        ], 
        k=1
    )[0]
    print("Weather State: ",weather_state)
    return weather_state

def generate_weather_timeline(total_laps):
    weather_timeline = []
    
    first_transition = random.randint(
        total_laps // 5,
        total_laps // 2
    )
    second_transition = random.randint(min(first_transition + 2, total_laps),total_laps)
    weather_pattern = random.choices(
        [
            "DRY_ONLY",
            "DRY_TO_MIXED",
            "DRY_TO_WET",
            "MIXED_TO_WET"
        ],

        weights=[
            0.55,
            0.25,
            0.15,
            0.05
        ],

        k=1

    )[0]
    
    for lap in range(1, total_laps + 1):

        if weather_pattern == "DRY_ONLY":
            weather_state = "DRY"
        elif weather_pattern == "DRY_TO_MIXED":
            if lap < first_transition:
                weather_state = "DRY"
            else:
                weather_state = "MIXED"
        elif weather_pattern == "DRY_TO_WET":
            if lap < first_transition:
                weather_state = "DRY"
            elif lap < second_transition:
                weather_state = "MIXED"
            else:
                weather_state = "WET"
        elif weather_pattern == "MIXED_TO_WET":
            if lap < first_transition:
                weather_state = "MIXED"
            else:
                weather_state = "WET"

        weather_timeline.append(
            weather_state
        )
    return weather_timeline

if __name__ == "__main__":

    timeline = generate_weather_timeline(
        57
    )

    for lap, weather in enumerate(
        timeline,
        start=1
    ):

        print(
            f"Lap {lap}: {weather}"
        )
