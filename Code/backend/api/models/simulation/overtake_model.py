import random


def can_attempt_overtake(gap_ahead):
    """
    Determine whether the player is close enough
    to attempt an overtake.
    """

    if gap_ahead is None:
        return False

    return gap_ahead <= 1.2


def calculate_overtake_probability(
    tyre_advantage,
    pace_advantage
):
    """
    Calculate probability of completing an overtake.

    tyre_advantage:
        0 = none
        1 = fresher tyres
        2 = much fresher tyres

    pace_advantage:
        0 = equal pace
        1 = faster
        2 = significantly faster
    """

    probability = 0.20

    probability += (
        tyre_advantage * 0.15
    )

    probability += (
        pace_advantage * 0.20
    )

    probability = max(
        0.05,
        min(probability, 0.90)
    )

    return probability


def attempt_overtake(
    probability
):
    """
    Execute random overtake outcome.
    """

    return (
        random.random()
        < probability
    )


def evaluate_overtake(
    gap_ahead,
    tyre_advantage,
    pace_advantage
):
    """
    Full overtake evaluation pipeline.

    Returns:

    {
        "attempted": bool,
        "success": bool,
        "probability": float
    }
    """

    if not can_attempt_overtake(
        gap_ahead
    ):
        return {
            "attempted": False,
            "success": False,
            "probability": 0.0
        }

    probability = (
        calculate_overtake_probability(
            tyre_advantage,
            pace_advantage
        )
    )

    success = (
        attempt_overtake(
            probability
        )
    )

    return {
        "attempted": True,
        "success": success,
        "probability": probability
    }


if __name__ == "__main__":

    for i in range(10):

        result = evaluate_overtake(
            gap_ahead=0.8,
            tyre_advantage=1,
            pace_advantage=1
        )

        print(result)