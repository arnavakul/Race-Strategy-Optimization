from api.models.simulation.pitstop_model import (get_pitstop_time)

def forecast_scenario(race_state, scenario):
    
    return {
        "scenario": "PIT_NOW",

        "expected_finish": 3,

        "expected_race_time": 5284.3,

        "risk_score": 0.22,

        "recommended_compound": "HARD",

        "reason": "Avoid tyre cliff"
    }

def get_recommended_compound(
    current_compound
):

    if current_compound == "SOFT":

        return "MEDIUM"

    elif current_compound == "MEDIUM":

        return "HARD"

    return "HARD"

def apply_scenario(
    race_state,
    scenario
):

    compound = race_state["compound"]

    tyre_age = race_state["tyre_age"]

    track = race_state["track"]

    pit_loss = 0

    laps_before_pit = 0

    if scenario == "PIT_NOW":

        compound = (
            get_recommended_compound(
                compound
            )
        )

        tyre_age = 0

        pit_loss = (
            get_pitstop_time(track)
        )

    elif scenario == "PIT_PLUS_3":

        laps_before_pit = 3

        compound = (
            get_recommended_compound(
                compound
            )
        )

        tyre_age = 0

        pit_loss = (
            get_pitstop_time(track)
        )

    elif scenario == "PIT_PLUS_5":

        laps_before_pit = 5

        compound = (
            get_recommended_compound(
                compound
            )
        )

        tyre_age = 0

        pit_loss = (
            get_pitstop_time(track)
        )

    elif scenario == "STAY_OUT":

        pit_loss = 0

    return {

        "compound": compound,

        "tyre_age": tyre_age,

        "pit_loss": pit_loss,

        "laps_before_pit": laps_before_pit
    }

from api.models.simulation.lap_time_engine import (get_degradation)
def estimate_remaining_degradation(
    track,
    compound,
    tyre_age,
    laps_remaining
):
    total_degradation_loss = 0
    
    for lap in range(laps_remaining):
        
        future_tyre_age = (
            tyre_age + lap
        )
        
        degradation = (
            get_degradation(
                track,
                compound,
                future_tyre_age
            )
        )
        
        total_degradation_loss += (degradation)
        
    return total_degradation_loss

#estimating pit benefit meaning if we pit now are we gonna get some benefit or not 
def estimate_pit_benefit(
    track,
    current_compound,
    current_tyre_age,
    new_compound,
    laps_remaining
):
    
    stay_out_loss = (
        estimate_remaining_degradation(
            track,
            current_compound,
            current_tyre_age,
            laps_remaining
        )
    )
    
    fresh_tyre_loss = (
        estimate_remaining_degradation(
            track,
            new_compound,
            0,
            laps_remaining
        )
    )
    
    tyre_gain = (
        stay_out_loss - fresh_tyre_loss
    )
    
    return {

    "stay_out_loss":
        stay_out_loss,

    "fresh_tyre_loss":
        fresh_tyre_loss,

    "tyre_gain":
        tyre_gain
}

#to check if the pitting is actually valuable or not : 
def estimate_net_strategy_gain(
    track,
    current_compound,
    current_tyre_age,
    new_compound,
    laps_remaining,
    pit_loss
):
    
    pit_benefit = (
        estimate_pit_benefit(
            track=track,
            current_compound=current_compound,
            current_tyre_age=current_tyre_age,
            new_compound=new_compound,
            laps_remaining=laps_remaining
        )
    )
    
    tyre_gain = (
        pit_benefit["tyre_gain"]
    )
    
    net_gain = (
        tyre_gain - pit_loss
    )
    
    
    return {

        "tyre_gain": tyre_gain,

        "pit_loss": pit_loss,

        "net_gain": net_gain
    }


def estimate_position_impact(
    current_position,
    gap_ahead,
    gap_behind,
    net_gain
):

    expected_position = current_position

    if net_gain > gap_ahead:

        expected_position -= 1

    if net_gain > (gap_ahead * 2):

        expected_position -= 1

    if (
        net_gain < 0
        and
        abs(net_gain) > gap_behind
    ):

        expected_position += 1

    return max(
        1,
        expected_position
    )

#risk function 
def calculate_risk_score(
    tyre_age
):

    risk = 0

    if tyre_age >= 15:

        risk += 0.3

    if tyre_age >= 20:

        risk += 0.3

    if tyre_age >= 25:

        risk += 0.4

    return min(
        risk,
        1.0
    )

# Now this is the final forecast scenerio: 
def forecast_scenario(
    race_state,
    scenario
):
    
    scenario_state = (
        apply_scenario(
            race_state,
            scenario
        )
    )
    
    strategy_result = (
        estimate_net_strategy_gain(
            track=race_state["track"],
            
            current_compound=race_state["compound"],
            
            current_tyre_age=race_state["tyre_age"],
            
            new_compound=scenario_state["compound"],
            
            laps_remaining= race_state["laps_remaining"],
            
            pit_loss = scenario_state["pit_loss"],
        )
    )
    degradation_loss = (
        estimate_remaining_degradation(
            track=race_state["track"],

            compound=scenario_state["compound"],

            tyre_age=scenario_state["tyre_age"],

            laps_remaining=
                race_state["laps_remaining"]
        )
    )
    
    # expected_race_time = (
    #     estimate_race_time(

    #         laps_remaining=
    #             race_state["laps_remaining"],

    #         degradation_loss=
    #             degradation_loss,

    #         pit_loss=
    #             scenario_state["pit_loss"]
    #     )
    # )
    
    reason = (
        generate_reason(
            race_state,
            strategy_result
        )
    )
    expected_position = (
        estimate_position_impact(

            current_position=
                race_state["position"],

            gap_ahead=
                race_state["gap_ahead"],

            gap_behind=
                race_state["gap_behind"],

            net_gain=
                strategy_result["net_gain"]
        )
    )
    
    risk_score = (
        calculate_risk_score(
            race_state["tyre_age"]
        )
    )
    return {

        "scenario":
            scenario,

        "expected_position":
            expected_position,

        # "expected_race_time":
        #     round(
        #         expected_race_time,
        #         3
        #     ),

        "net_gain":
            round(
                strategy_result[
                    "net_gain"
                ],
                3
            ),

        "risk_score":
            round(
                risk_score,
                3
            ),

        "recommended_compound":
            scenario_state[
                "compound"
            ],

        "reason":
            reason
    }

def generate_reason(
    race_state,
    strategy_result
):

    tyre_age = race_state["tyre_age"]

    net_gain = strategy_result["net_gain"]

    if tyre_age >= 20:

        return "Tyres approaching cliff"

    if net_gain > 5:

        return "Fresh tyre advantage available"

    if net_gain < 0:

        return "Pit stop cost outweighs tyre gain"

    return "Maintain current strategy"

if __name__ == "__main__":

    race_state = {

    "position": 4,

    "compound": "MEDIUM",

    "tyre_age": 18,

    "track": "monza_2022",

    "gap_ahead": 1.2,

    "gap_behind": 2.5,

    "laps_remaining": 10
}

result = forecast_scenario(

    race_state,

    "PIT_NOW"
)

print(result)