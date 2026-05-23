import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from api.models.simulation.race_constraints import (
    validate_strategy
)


def test_valid_strategy():

    strategy = [
        ("SOFT", 15),
        ("HARD", 42)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is True


def test_single_compound_invalid():

    strategy = [
        ("MEDIUM", 57)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is False


def test_invalid_total_laps():

    strategy = [
        ("SOFT", 10),
        ("HARD", 10)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is False


def test_wet_race_allowed():

    strategy = [
        ("INTERMEDIATE", 57)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is True


def test_invalid_compound():

    strategy = [
        ("ULTRASOFT", 57)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is False


def test_negative_laps():

    strategy = [
        ("SOFT", -10),
        ("HARD", 67)
    ]

    result = validate_strategy(
        strategy,
        57
    )

    assert result is False