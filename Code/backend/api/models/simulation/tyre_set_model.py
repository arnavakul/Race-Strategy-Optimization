# Responsible for:
# - tyre set freshness
# - used tyre sets
# - heat cycles


def create_tyre_set(
    compound,
    freshness=1.0,
    heat_cycles=0,
    used_laps=0
):

    return {

        "compound": compound,

        "freshness": freshness,

        "heat_cycles": heat_cycles,

        "used_laps": used_laps
    }

def get_freshness_penalty(
    tyre_set
):

    freshness = tyre_set[
        "freshness"
    ]

    used_laps = tyre_set[
        "used_laps"
    ]

    heat_cycles = tyre_set[
        "heat_cycles"
    ]

    freshness_penalty = (
        (1.0 - freshness)
        * 0.8
    )

    heat_cycle_penalty = (
        heat_cycles
        * 0.12
    )

    scrub_penalty = (
        used_laps
        * 0.015
    )

    total_penalty = (

        freshness_penalty

        + heat_cycle_penalty

        + scrub_penalty
    )

    return total_penalty