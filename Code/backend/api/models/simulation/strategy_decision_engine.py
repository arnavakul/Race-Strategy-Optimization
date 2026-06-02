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

from api.models.simulation.rival_startegy_model import(
    should_attempt_overcut,
    should_attempt_undercut
)

import random
import os

DEBUG_STRATEGY = False

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


def should_pit(

    track,

    tyre_age,

    compound,

    weather_state,

    rival_gap,

    current_lap,

    total_laps,

    strategy_profile="BALANCED",

    safety_car_active=False,

    vsc_active=False
):

    track_data = get_track_parameters(track)

    profile = STRATEGY_PROFILES[
        strategy_profile
    ]

    undercut_chance = profile[
        "undercut_chance"
    ]

    extend_chance = profile[
        "extend_chance"
    ]

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

        extend_chance -= 0.10

        undercut_chance = min(
            undercut_chance,
            1.0
        )

        extend_chance = max(
            extend_chance,
            0.0
        )

    cliff_age = track_data[
        "cliff_age"
    ][compound]

    pit_window = evaluate_pit_window(

        tyre_age,

        cliff_age
    )
    
    laps_remaining = (
        total_laps
        - current_lap
    )

    if DEBUG_STRATEGY:

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
    
    if weather_state == "MIXED":
        
        if compound == "INTERMEDIATE":
            
            return {
                "pit":False,
                "reason": "WEATHER_PROTECTION"
            }
    
    if weather_state == "WET":
        
        if compound == 'WET':
            
            return{
                "pit":False,
                "reason":"WEATHER_PROTECTION"
            }

    if not correct_tyre:

        return {

            "pit": True,

            "reason": "WEATHER_MISMATCH"
        }

    if pit_window == "FORCE_PIT":

        if laps_remaining <= 8:

            return {
                "pit": False,
                "reason": "FINISH_STINT"
            }

        return {
            "pit": True,
            "reason": "FORCE_PIT"
        }

    elif pit_window == "TOO_EARLY":

        return {

            "pit": False,

            "reason": "TOO_EARLY"
        }

    elif pit_window == "UNDERCUT_WINDOW":

    # Too late in race to recover pit stop time

        if laps_remaining <= 12:

            return {
                "pit": False,
                "reason": "TOO_LATE_FOR_UNDERCUT"
            }

        if (

            undercut_opportunity

            and

            random.random() < undercut_chance
        ):

            return {

                "pit": True,

                "reason": "UNDERCUT"
            }

        return {

            "pit": False,

            "reason": "STAY_OUT"
        }
    elif pit_window == "EXTEND_WINDOW":

        # Close enough to finish race
        if compound == "HARD" and laps_remaining <= 15:

            return {
                "pit": False,
                "reason": "RUN_TO_FINISH"
            }

        if compound == "MEDIUM" and laps_remaining <= 12:

            return {
                "pit": False,
                "reason": "RUN_TO_FINISH"
            }

        if compound == "SOFT" and laps_remaining <= 8:

            return {
                "pit": False,
                "reason": "RUN_TO_FINISH"
            }

        # Hard tyres are generally extended
        if compound == "HARD":

            return {
                "pit": False,
                "reason": "FINAL_STINT"
            }

        # Attempt overcut strategy
        if (
            overcut_opportunity
            and
            tyre_age >= cliff_age - 2
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
    
    
if __name__ == "__main__":

    print("\nSTRATEGY DECISION TEST\n")

    for lap in range(1, 20):

            result = should_pit(

            track="bahrain_2022",

            compound="SOFT",

            tyre_age=lap,

            weather_state="DRY",

            rival_gap=1.5,

            current_lap=lap,

            total_laps=57,

            strategy_profile="AGGRESSIVE",

            safety_car_active=False
        )

            print(

                f"Lap Age: {lap} | "

                f"Pit: {result['pit']} | "

                f"Reason: {result['reason']}"
            )