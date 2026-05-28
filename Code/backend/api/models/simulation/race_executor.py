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

from api.models.simulation.pit_window_model import (
    evaluate_pit_window
)

from api.models.simulation.safety_car_model import (
    check_safety_car,
    get_safety_car_multiplier,
    generate_safety_car_duration
)

from api.models.simulation.vsc_model import (
    check_virtual_safety_Car,
    generate_vsc_duration,
    get_vsc_multiplier
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

    # Safety car state
    safety_car_active = False

    safety_car_remaining = 0

    safety_car_deployments = 0

    sc_cooldown = 0

    # VSC state
    vsc_active = False

    vsc_remaining = 0

    vsc_deployments = 0

    vsc_cooldown = 0

    # Simulate full race
    for lap in range(total_laps):

        # Human-readable lap number
        current_lap = lap + 1

        # Reduce cooldowns
        if sc_cooldown > 0:

            sc_cooldown -= 1

        if vsc_cooldown > 0:

            vsc_cooldown -= 1

        # Current weather
        weather_state = weather_timeline[
            lap
        ]

        # Random SC deployment
        if (
            not safety_car_active
            and
            not vsc_active
            and
            sc_cooldown == 0
        ):

            if check_safety_car():

                safety_car_active = True

                safety_car_remaining = (
                    generate_safety_car_duration()
                )

                safety_car_deployments += 1

                race_state.log_event(
                    f"Lap {current_lap}: "
                    f"SAFETY CAR DEPLOYED"
                )

        # Random VSC deployment
        if (
            not safety_car_active
            and
            not vsc_active
            and
            vsc_cooldown == 0
        ):

            if check_virtual_safety_Car():

                vsc_active = True

                vsc_remaining = (
                    generate_vsc_duration()
                )

                vsc_deployments += 1

                race_state.log_event(
                    f"Lap {current_lap}: "
                    f"VIRTUAL SAFETY CAR DEPLOYED"
                )

        # Handle active safety car
        if safety_car_active:

            safety_car_remaining -= 1

            if safety_car_remaining <= 0:

                safety_car_active = False

                sc_cooldown = 5

                race_state.log_event(
                    f"Lap {current_lap}: "
                    f"SAFETY CAR ENDED"
                )

        # Handle active VSC
        if vsc_active:

            vsc_remaining -= 1

            if vsc_remaining <= 0:

                vsc_active = False

                vsc_cooldown = 3

                race_state.log_event(
                    f"Lap {current_lap}: "
                    f"VIRTUAL SAFETY CAR ENDED"
                )

        # Strategy pit decision
        pit_decision = should_pit(

            track=track,

            compound=race_state.current_compound,

            tyre_age=race_state.current_tyre_age,

            weather_state=weather_state,

            strategy_profile="BALANCED",

            safety_car_active=safety_car_active,

            vsc_active=vsc_active
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

            # Avoid useless same tyre stop
            if (
                new_compound == race_state.current_compound
                and
                pit_window != "FORCE_PIT"
            ):

                pit_now = False

            # Execute valid pitstop
            if pit_now:

                # Register tyre switch
                race_state.register_compound_usage(
                    new_compound
                )

                # Register pitstop
                race_state.register_pitstop()

                # Base pitloss
                pit_loss = get_pitstop_time(
                    track
                )

                # Reduced pitloss under SC
                if safety_car_active:

                    pit_loss *= 0.65

                # Reduced pitloss under VSC
                elif vsc_active:

                    pit_loss *= 0.82

                # Add pitloss
                total_race_time += pit_loss

                # Store event
                race_state.log_event(
                    f"Lap {current_lap}: "
                    f"{pit_reason} -> "
                    f"{new_compound}"
                )

        # Increase tyre age
        race_state.increment_tyre_age()

        # Update tyre usage
        race_state.current_tyre_set[
            "used_laps"
        ] += 1

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
            ),

            current_lap=current_lap,

            total_laps=total_laps,

            driver_profile="BALANCED",

            tyre_set=(
                race_state.current_tyre_set
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

        # Apply SC slowdown
        if safety_car_active:

            corrected_lap_time *= (
                get_safety_car_multiplier()
            )

        # Apply VSC slowdown
        elif vsc_active:

            corrected_lap_time *= (
                get_vsc_multiplier()
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

            "safety_car": (
                safety_car_active
            ),

            "virtual_safety_car": (
                vsc_active
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

        "safety_car_deployments": (
            safety_car_deployments
        ),

        "vsc_deployments": (
            vsc_deployments
        ),

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
        "Safety Car Deployments:",
        result["safety_car_deployments"]
    )

    print(
        "VSC Deployments:",
        result["vsc_deployments"]
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