# This file is responisble for deciding to :
# stay out?
# pit?
# which tyre?
# extend stint?
# react to weather?
# react to degradation?

from api.models.simulation.track_model import (get_track_parameters)
from api.models.simulation.pit_window_model import(evaluate_pit_window)

import os

def is_correct_tyre_for_weather(
    compound,weather_state
):
    if weather_state == "DRY":
        return compound in [
            "SOFT",
            "MEDIUM",
            "HARD"
        ]
    
    elif weather_state == "MIXED":
        
        return compound == "INTERMEDIATE"
    
    elif weather_state == "WET":
        
        return compound == "WET"
    return False


def should_pit(track, tyre_age, compound, weather_state):
    track_data = get_track_parameters(track)
    
    cliff_age = track_data["cliff_age"][compound]
    
    pit_window = evaluate_pit_window(
        tyre_age,
        cliff_age
    )
    
    correct_tyre = (
        is_correct_tyre_for_weather(
            compound,
            weather_state
        )
    )
    
    if not correct_tyre:

        return True
    
    
    if pit_window == "FORCE_PIT":
        return True
    
    elif pit_window == "TOO_EARLY":

        return False
    
    elif pit_window == "UNDERCUT_WINDOW":
        return False
    
  
    elif pit_window == "EXTEND_WINDOW":
        return False

    
    
    
    return False

if __name__ == "__main__":

    result = should_pit(

        track="bahrain_2022",

        compound="SOFT",

        tyre_age=13,

        weather_state="DRY"
    )

    print(result)