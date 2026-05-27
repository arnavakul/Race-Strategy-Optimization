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

    # tyre pace offsets
    "compound_pace_delta": {

        "SOFT": 0.0,

        "MEDIUM": 0.7,

        "HARD": 1.5,

        "INTERMEDIATE": 4.0,

        "WET": 7.0
    },

    # tyre degradation
    "compound_deg": {

        "SOFT": 0.12,

        "MEDIUM": 0.08,

        "HARD": 0.05,

        "INTERMEDIATE": 0.09,

        "WET": 0.11
    },

    # tyre cliff age
    "cliff_age": {

        "SOFT": 12,

        "MEDIUM": 20,

        "HARD": 30,

        "INTERMEDIATE": 18,

        "WET": 15
    },

    # cliff severity
    "cliff_multiplier": {

        "SOFT": 0.08,

        "MEDIUM": 0.05,

        "HARD": 0.03,

        "INTERMEDIATE": 0.06,

        "WET": 0.09
    },

    # warmup penalties
    "warmup_penalty": {

        "SOFT": 0.2,

        "MEDIUM": 0.5,

        "HARD": 0.8,

        "INTERMEDIATE": 0.7,

        "WET": 1.2
    }
}


def get_track_parameters(track):

    track_data = DEFAULT_TRACK.copy()

    if track in TRACK_CHARACTERISTICS:

        loaded_data = TRACK_CHARACTERISTICS[track]

        for key, value in loaded_data.items():

            # merge nested dicts safely
            if (
                isinstance(value, dict)
                and key in track_data
            ):

                merged = track_data[key].copy()

                merged.update(value)

                track_data[key] = merged

            else:

                track_data[key] = value

    return track_data