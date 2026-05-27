# This file is responisble for deciding to :
# stay out?
# pit?
# which tyre?
# extend stint?
# react to weather?
# react to degradation?

from api.models.simulation.crossover_logic import (should_pit_for_weather)
from api.models.simulation.track_model import (get_track_parameters)

import os

def should_pit(track, tyre_age, compound, weather_state):
    track_data = get_track_parameters(track)
    
    cliff_age = track_data["cliff_age"][compound]
    
    weather_pit = should_pit_for_weather(compound, weather_state)
    
    if weather_pit:
        return True
    
    if tyre_age >= cliff_age:
        return True
    
    return False

if __name__ == "__main__":

    result = should_pit(

        track="bahrain_2022",

        compound="SOFT",

        tyre_age=13,

        weather_state="DRY"
    )

    print(result)