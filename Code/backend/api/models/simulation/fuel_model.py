import pickle

from api.config.paths import (
    SAVED_MODELS_PATH
)

MODEL_PATH = (
    SAVED_MODELS_PATH
    / "fuel_model.pkl"
)

with open(MODEL_PATH, "rb") as f:

    FUEL_MODEL = pickle.load(f)


def get_fuel_effect_per_kg():

    return FUEL_MODEL[
        "fuel_effect_per_kg"
    ]