from api.models.simulation.stint_simulator import (
    simulate_stint
)

from api.models.simulation.pitstop_model import (
    get_pitstop_time
)

from api.models.simulation.race_state import (
    RaceState
)

from api.models.simulation.weather_model import (
    generate_weather_timeline
)


def simulate_strategy(
    track,
    strategy
):

    # Create race memory
    race_state = RaceState()

    # Calculate total race laps
    total_race_laps = sum(
        laps for _, laps in strategy
    )

    # Generate dynamic weather
    weather_timeline = generate_weather_timeline(
        total_race_laps
    )

    total_race_time = 0

    all_laps = []
    
    race_lap_cursor = 0
    
    for i, (compound, laps) in enumerate(strategy):

        # Register compound usage
        race_state.register_compound_usage(
            compound
        )

        # Simulate current stint
        stint_result = simulate_stint(
            track=track,
            total_laps=laps,
            weather_timeline=weather_timeline,
            race_state=race_state,
            starting_lap=race_lap_cursor
        )
        
        race_lap_cursor += laps

        # Add stint race time
        total_race_time += (
            stint_result["total_time"]
        )

        # Store telemetry
        all_laps.extend(
            stint_result["laps"]
        )

        # Store stint history
        race_state.add_stint_record(
            compound=compound,
            laps=laps
        )

        # Check final stint
        is_final_stint = (
            i == len(strategy) - 1
        )

        # Add pitstop
        if not is_final_stint:

            pit_loss = get_pitstop_time(
                track
            )

            total_race_time += pit_loss

            # Register pitstop state
            race_state.register_pitstop()

            # Log strategic event
            race_state.log_event(
                f"Pitstop after stint {i + 1}"
            )

    # Validate FIA legality
    race_state.validate_fia_legality()

    return {

        "strategy": strategy,

        "total_time": total_race_time,

        "pitstops": race_state.pitstop_count,

        "laps": all_laps,

        "stints": race_state.stint_history,

        "events": race_state.strategy_events,

        "legal_race": race_state.is_legal_race,

        "weather": weather_timeline
    }


if __name__ == "__main__":

    strategy = [

        ("SOFT", 12),

        ("MEDIUM", 20),

        ("HARD", 25)
    ]

    result = simulate_strategy(

        track="bahrain_2022",

        strategy=strategy
    )

    print("\nSTRATEGY SIMULATION\n")

    print(
        "Strategy:",
        result["strategy"]
    )

    print(
        "Total Race Time:",
        result["total_time"]
    )

    print(
        "Pit Stops:",
        result["pitstops"]
    )

    print(
        "Total Laps:",
        len(result["laps"])
    )

    print(
        "Legal Race:",
        result["legal_race"]
    )

    print(
        "Stints:",
        result["stints"]
    )

    print(
        "Events:",
        result["events"]
    )

    print(
        "Weather Timeline:"
    )

    print(
        result["weather"]
    )