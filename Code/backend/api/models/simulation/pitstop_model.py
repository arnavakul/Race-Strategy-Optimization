import os 
import pickle

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "pitstop_loss.pkl"
)

with open(MODEL_PATH, 'rb')as f:
    PITSTOP_MODEL = pickle.load(f)

def get_pitstop_time(track):
    return PITSTOP_MODEL(track, 22.0)