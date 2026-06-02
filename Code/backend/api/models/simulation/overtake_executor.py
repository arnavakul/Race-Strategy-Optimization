def execute_overtake(
    player_total_time,
    gap_ahead,
    success
):
    """
    Execute race impact of an overtake.

    Parameters
    ----------
    player_total_time : float

    gap_ahead : float

    success : bool

    Returns
    -------
    {
        "player_total_time": float,
        "position_gain": bool,
        "time_gain": float
    }
    """

    if not success:

        return {
            "player_total_time": player_total_time,
            "position_gain": False,
            "time_gain": 0.0
        }

    # Reward successful overtake
    # Small but meaningful gain

    time_gain = 0.50

    player_total_time -= time_gain

    return {
        "player_total_time": player_total_time,
        "position_gain": True,
        "time_gain": time_gain
    }


if __name__ == "__main__":

    result = execute_overtake(
        player_total_time=5000.0,
        gap_ahead=0.8,
        success=True
    )

    print(result)