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

from api.models.optimization.strategy_generator import (
    generate_strategies
)

from api.models.simulation.race_constraints import (
    validate_strategy
)


def test_all_generated_strategies_are_valid():

    strategies = generate_strategies(57)

    for strategy in strategies:

        assert validate_strategy(
            strategy,
            57
        ) is True