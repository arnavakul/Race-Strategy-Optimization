from models.optimization.strategy_generator import (
    generate_strategies
)

from models.simulation.strategy_simulation import (
    simulate_strategy
)

def strategy_optimizer(track,total_laps):
    strategies = generate_strategies(total_laps)
    
    results = []
    
    for strategy in strategies:
        
        simulation = simulate_strategy(
            track=track,
            strategy=strategy
        )
        results.append({
            "strategy": strategy,
            "total_time": simulation["total_time"],
            "pitstops": simulation["pitstops"]
        })
        
    best_strategy = min(
        results,
        key=lambda x:x["total_time"]
    )
    
    return best_strategy

if __name__ == "__main__":

    best = strategy_optimizer(
        track="bahrain_2022",
        total_laps=57
    )

    print("\nBEST STRATEGY:\n")

    print(best)