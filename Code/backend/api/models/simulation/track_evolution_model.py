# Responsible for:
# - track rubbering
# - grip evolution
# - race pace evolution


def get_track_grip(
    current_lap,
    total_laps
):

    # Race progress percentage
    race_progress = (
        current_lap / total_laps
    )

    # Early race
    if race_progress < 0.20:

        grip_multiplier = 0.996

    # Mid race
    elif race_progress < 0.60:

        grip_multiplier = 1.000

    # Late race
    else:

        grip_multiplier = 1.004

    return grip_multiplier