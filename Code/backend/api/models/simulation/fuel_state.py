import pickle

from api.config.paths import (
    SAVED_MODELS_PATH
)


with open(
    SAVED_MODELS_PATH / "fuel_model.pkl",
    "rb"
) as f:

    fuel_model = pickle.load(f)


FUEL_EFFECT_PER_KG = (
    fuel_model["fuel_effect_per_kg"]
)


class FuelState:

    def __init__(
        self,
        starting_fuel,
        fuel_burn_per_lap
    ):

        self.current_fuel = starting_fuel

        self.fuel_burn_per_lap = (
            fuel_burn_per_lap
        )

    def getFuelCorrection(self):

        return (

            self.current_fuel
            * FUEL_EFFECT_PER_KG
        )

    def burnFuel(self):

        self.current_fuel -= (
            self.fuel_burn_per_lap
        )

        if self.current_fuel < 0:

            self.current_fuel = 0


if __name__ == "__main__":

    fuel = FuelState(

        starting_fuel=100,

        fuel_burn_per_lap=1.8
    )

    for lap in range(5):

        print(

            f"Lap {lap+1} | "

            f"Fuel: "
            f"{fuel.current_fuel:.2f} kg | "

            f"Correction: "
            f"{fuel.getFuelCorrection():.3f}"
        )

        fuel.burnFuel()