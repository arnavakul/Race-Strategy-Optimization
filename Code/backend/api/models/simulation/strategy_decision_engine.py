# This file is responisble for deciding to :
# stay out?
# pit?
# which tyre?
# extend stint?
# react to weather?
# react to degradation?

from api.models.simulation.track_model import (get_track_parameters)
from api.models.simulation.pit_window_model import(evaluate_pit_window)
from api.models.simulation.strategy_profile import (STRATEGY_PROFILES)
from api.models.simulation.safety_car_model import (get_safety_car_multiplier,generate_safety_car_duration,check_safety_car)
from api.models.simulation.rival_startegy_model import(generate_rival_gap,should_attempt_overcut,should_attempt_undercut)
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


def should_pit(track, tyre_age, compound, weather_state, strategy_profile = "BALANCED",safety_car_active = False):
    track_data = get_track_parameters(track)
    profile = STRATEGY_PROFILES[strategy_profile]
    
    undercut_chance = profile[
        "undercut_chance"
    ]
    
    extend_chance = profile[
        "extend_chance"
    ]
    
    #rival strategy state
    rival_gap = generate_rival_gap()
    
    undercut_opportunity = (
        should_attempt_undercut(
            rival_gap
        )
    )
    overcut_opportunity = (
        should_attempt_overcut(
            rival_gap
        )
    )
    
    
    if safety_car_active:
        
        undercut_chance += 0.30
        
        extend_chance -=0.10
        
        undercut_chance = min(undercut_chance,1.0)
        
        extend_chance = max(extend_chance, 0.0)
    
    cliff_age = track_data["cliff_age"][compound]
    
    pit_window = evaluate_pit_window(
        tyre_age,
        cliff_age
    )
    
    print(
        f"Tyre: {compound} | "
        f"Age: {tyre_age} | "
        f"Cliff: {cliff_age} | "
        f"Window: {pit_window} | "
        f"Gap: {rival_gap:.2f} | "
        f"SC: {safety_car_active}"
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
        if (undercut_opportunity and random.random() < undercut_chance):
            return{
            "pit":True,
            "reason" : "UNDERCUT"
        }
        return {
        "pit": False,
        "reason": "STAY_OUT"
        }   
    
  
    elif pit_window == "EXTEND_WINDOW":
        if (
        overcut_opportunity
        and
        random.random() > extend_chance
    ):
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

    print("\nSTRATEGY DECISION TEST\n")

    for lap in range(1, 20):

        result = should_pit(

            track="bahrain_2022",

            compound="SOFT",

            tyre_age=lap,

            weather_state="DRY",

            strategy_profile="AGGRESSIVE",

            safety_car_active=False
        )

        print(

            f"Lap Age: {lap} | "

            f"Pit: {result['pit']} | "

            f"Reason: {result['reason']}"
        )