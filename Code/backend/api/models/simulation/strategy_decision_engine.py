# This file is responisble for deciding to :
# stay out?
# pit?
# which tyre?
# extend stint?
# react to weather?
# react to degradation?

from api.models.simulation.track_model import (get_track_parameters)
from api.models.simulation.pit_window_model import(evaluate_pit_window)
import random
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
    
    print(
        f"Tyre: {compound} | "
        f"Age: {tyre_age} | "
        f"Cliff: {cliff_age} | "
        f"Window: {pit_window}"
    )
    
    correct_tyre = (
        is_correct_tyre_for_weather(
            compound,
            weather_state
        )
    )
    
    if not correct_tyre:
        return{
            "pit":True,
            "reason" : "WEATHER_MISMATCH"
        }
    
    if pit_window == "FORCE_PIT":
        return{
            "pit":True,
            "reason" : "FORCE_PIT"
        }
    
    elif pit_window == "TOO_EARLY":

        return {
            "pit": False,
            "reason": "TOO_EARLY"
        }
    
    elif pit_window == "UNDERCUT_WINDOW":
        if random.random()<0.35:
            return{
            "pit":True,
            "reason" : "UNDERCUT"
        }
        return {
        "pit": False,
        "reason": "STAY_OUT"
        }   
    
  
    elif pit_window == "EXTEND_WINDOW":
        if random.random() < 0.15:
            return {
                "pit": True,
                "reason": "EXTEND_COMPLETE"
            }

        return {
            "pit": False,
            "reason": "STAY_OUT"
        }
    
    return {
        "pit": False,
        "reason": "STAY_OUT"
    }

if __name__ == "__main__":

    result = should_pit(

        track="bahrain_2022",

        compound="SOFT",

        tyre_age=13,

        weather_state="DRY"
    )

    print(result)