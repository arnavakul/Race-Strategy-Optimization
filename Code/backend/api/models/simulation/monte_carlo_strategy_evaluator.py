from api.models.simulation.scenario_forecaster import (
    forecast_scenario
)

import random

def run_strategy_monte_carlo(
    race_state, scenario, simulations=100
):
    
    finishes = []
    
    times = []
    
    for _ in range(simulations):
        
        result = forecast_scenario(
            race_state,scenario
        )
        
        finish_noise = random.choice(
            [-1,0,1]
        )
        
        time_noise = random.uniform(
            -3,3
        )
        
        sim_finish = (
            result["expected_finish"] + finish_noise
        )
        
        sim_finish = max(1,sim_finish)
        
        sim_time = (
            result["expected_race_time"] + time_noise
        )
        
        finishes.append(sim_finish)
        
        times.append(sim_time)
    
    average_finish = (
        sum(finishes) / len(finishes)
    )
    
    average_time = (
        sum(times) / len(times)
    )
    
    best_finish = min(finishes)
    
    worst_finish = max(finishes)
    
    podiums = len(
        [
            f 
            for f in finishes
            if f <= 3
        ]
    )
    
    podium_probability = (
        podiums / simulations * 100
    )
    
    wins = len(
        [
            f
            for f in finishes
            if f==1
        ]
    )
    
    win_probability = (
        wins / simulations * 100
    )
    
    return {

        "scenario": scenario,

        "average_finish":
            round(
                average_finish,
                2
            ),

        "average_time":
            round(
                average_time,
                2
            ),

        "best_finish":
            best_finish,

        "worst_finish":
            worst_finish,

        "podium_probability":
            round(
                podium_probability,
                2
            ),

        "win_probability":
            round(
                win_probability,
                2
            )
    }