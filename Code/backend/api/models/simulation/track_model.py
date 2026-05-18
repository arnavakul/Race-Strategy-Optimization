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


def get_track_parameters(track):

    return TRACK_CHARACTERISTICS[track]