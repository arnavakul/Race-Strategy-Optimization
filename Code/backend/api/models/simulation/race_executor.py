from api.models.simulation.race_state import (
    RaceState
)

from api.models.simulation.lap_time_engine import (
    compute_lap_time
)

from api.models.simulation.weather_model import (
    generate_weather_timeline
)

from api.models.simulation.fuel_state import (
    FuelState
)

from api.models.simulation.strategy_decision_engine import (
    should_pit
)

from api.models.simulation.crossover_logic import (
    get_recommended_compound
)

from api.models.simulation.pitstop_model import (
    get_pitstop_time
)

from api.models.simulation.track_model import (
    get_track_parameters
)

from api.models.simulation.pit_window_model import(
    evaluate_pit_window
)

import random

# RACE EXECUTOR

def execute_race(
    track,
    starting_compound,
    total_laps
):

    # Initialize race memory
    race_state = RaceState()

    # Register starting tyre
    race_state.register_compound_usage(
        starting_compound
    )

    # Generate weather timeline
    weather_timeline = (
        generate_weather_timeline(
            total_laps
        )
    )

    # Get track data
    track_data = get_track_parameters(
        track
    )

    # Warmup penalties
    warmup_map = track_data[
        "warmup_penalty"
    ]

    # Initialize fuel system
    fuel = FuelState(
        starting_fuel=100,
        fuel_burn_per_lap=1.8
    )

    # Store telemetry
    all_laps = []

    # Total race time
    total_race_time = 0

    # Simulate full race
    for lap in range(total_laps):

        # Human-readable lap number
        current_lap = lap + 1

        # Current weather
        weather_state = weather_timeline[
            lap
        ]

        # Strategy pit decision
        pit_decision = should_pit(

            track=track,

            compound=race_state.current_compound,

            tyre_age=race_state.current_tyre_age,

            weather_state=weather_state
        )

        pit_now = pit_decision["pit"]

        pit_reason = pit_decision["reason"]

        pit_loss = 0

        # Execute pitstop
        if pit_now:

            laps_remaining = (
                total_laps - current_lap
            )

            # Choose new tyre
            new_compound = (
                get_recommended_compound(
                    weather_state,
                    laps_remaining
                )
            )
            
            pit_window = evaluate_pit_window(

                race_state.current_tyre_age,

                track_data["cliff_age"][
                    race_state.current_compound
                ]
)
            
            # Avoid useless same-tyre stop
            if (
                new_compound == race_state.current_compound
                and
                pit_window != "FORCE_PIT"
            ):

                pit_now = False

            # Register tyre switch
            race_state.register_compound_usage(
                new_compound
            )

            # Register pitstop
            race_state.register_pitstop()

            # Add pitloss
            pit_loss = get_pitstop_time(
                track
            )

            total_race_time += pit_loss

            # Store event
            race_state.log_event(
                f"Lap {current_lap}: "
                f"{pit_reason} -> "
                f"{new_compound}"
            )

        # Increase tyre age
        race_state.increment_tyre_age()

        # Default warmup
        warmup_penalty = 0

        # Apply warmup penalty
        if race_state.current_tyre_age <= 2:

            warmup_penalty = float(

                warmup_map[
                    race_state.current_compound
                ]
            )

        # Fuel correction
        fuel_correction = (
            fuel.getFuelCorrection()
        )

        # Compute lap physics
        lap_data = compute_lap_time(

            track=track,

            compound=(
                race_state.current_compound
            ),

            tyre_age=(
                race_state.current_tyre_age
            ),

            fuel_correction=(
                fuel_correction
            )
        )

        # Final lap time
        corrected_lap_time = (

            float(lap_data["lap_time"])

            + warmup_penalty
        )

        # Mixed weather slowdown
        if weather_state == "MIXED":

            corrected_lap_time += (
                random.uniform(0.5, 1.5)
            )

        # Wet weather slowdown
        elif weather_state == "WET":

            corrected_lap_time += (
                random.uniform(2, 5)
            )

        # Update total race time
        total_race_time += (
            corrected_lap_time
        )

        # Store telemetry
        all_laps.append({

            "lap": current_lap,

            "compound": (
                race_state.current_compound
            ),

            "tyre_age": (
                race_state.current_tyre_age
            ),

            "weather": weather_state,

            "lap_time": (
                corrected_lap_time
            ),

            "pit": pit_now,

            "pit_loss": pit_loss,

            "fuel_load": (
                fuel.current_fuel
            ),

            "cumulative_time": (
                total_race_time
            )
        })

        # Burn fuel
        fuel.burnFuel()

    # Validate FIA legality
    race_state.validate_fia_legality()

    # Final output
    return {

        "total_time": total_race_time,

        "laps": all_laps,

        "pitstops": (
            race_state.pitstop_count
        ),

        "events": (
            race_state.strategy_events
        ),

        "legal_race": (
            race_state.is_legal_race
        ),

        "weather_timeline": (
            weather_timeline
        )
    }

# TESTING


if __name__ == "__main__":

    result = execute_race(

        track="bahrain_2022",

        starting_compound="SOFT",

        total_laps=57
    )

    print("\nRACE EXECUTION\n")

    print(
        "Total Race Time:",
        result["total_time"]
    )

    print(
        "Pit Stops:",
        result["pitstops"]
    )

    print(
        "Legal Race:",
        result["legal_race"]
    )

    print(
        "Events:"
    )

    for event in result["events"]:

        print(event)

    print(
        "\nFirst 5 Laps:"
    )

    for lap in result["laps"][:5]:

        print(lap)