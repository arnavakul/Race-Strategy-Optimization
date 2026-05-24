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
    