import pickle
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "saved_models",
    "track_characteristics.pkl"
)

with open(MODEL_PATH, "rb") as f:
    TRACK_CHARACTERISTICS = pickle.load(f)


DEFAULT_TRACK = {

    "compound_pace_delta": {
        "SOFT": 0.0,
        "MEDIUM": 0.7,
        "HARD": 1.5
    },

    "compound_deg": {
        "SOFT": -0.03,
        "MEDIUM": -0.015,
        "HARD": -0.008
    },

    "cliff_age": {
        "SOFT": 12,
        "MEDIUM": 20,
        "HARD": 30
    },

    "cliff_multiplier": {
        "SOFT": 0.08,
        "MEDIUM": 0.05,
        "HARD": 0.03
    },

    "warmup_penalty": {
        "SOFT": 0.2,
        "MEDIUM": 0.5,
        "HARD": 0.8
    }
}


def get_track_parameters(track):

    if track in TRACK_CHARACTERISTICS:
        return TRACK_CHARACTERISTICS[track]

    print(
        f"\nWARNING:"
        f" Using default parameters for {track}\n"
    )

    return DEFAULT_TRACK