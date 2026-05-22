import pickle
import os


track_characteristics = {
    
    "bahrain_2024": {

        "compound_pace_delta": {
            "SOFT": 0.0,
            "MEDIUM": 0.6,
            "HARD": 1.5
        },

        "compound_deg": {
            "SOFT": -0.04,
            "MEDIUM": -0.03,
            "HARD": -0.02
        },

        "cliff_age": {
            "SOFT": 15,
            "MEDIUM": 22,
            "HARD": 30
        },

        "warmup_penalty": {
            "SOFT": 0.6,
            "MEDIUM": 1.0,
            "HARD": 1.5
        },

        "cliff_multiplier": {
            "SOFT": 0.10,
            "MEDIUM": 0.08,
            "HARD": 0.05
        }
    },

    "bahrain_2022": {

        "compound_pace_delta": {
            "SOFT": 0.0,
            "MEDIUM": 0.6,
            "HARD": 1.5
        },

        "compound_deg": {
            "SOFT": 0.10,
            "MEDIUM": 0.07,
            "HARD": 0.03
        },

        "cliff_age": {
            "SOFT": 15,
            "MEDIUM": 22,
            "HARD": 30
        },

        "warmup_penalty": {
            "SOFT": 0.6,
            "MEDIUM": 1.0,
            "HARD": 1.5
        },
        "cliff_multiplier": {
            "SOFT": 0.10,
            "MEDIUM": 0.08,
            "HARD": 0.05
        }
    },

    "monza_2022": {

        "compound_pace_delta": {
            "SOFT": 0.0,
            "MEDIUM": 0.4,
            "HARD": 1.0
        },

        "compound_deg": {
            "SOFT": 0.06,
            "MEDIUM": 0.04,
            "HARD": 0.02
        },

        "cliff_age": {
            "SOFT": 20,
            "MEDIUM": 28,
            "HARD": 40
        },

        "warmup_penalty": {
            "SOFT": 0.3,
            "MEDIUM": 0.6,
            "HARD": 1.0
        },
        
        "cliff_multiplier": {
            "SOFT": 0.10,
            "MEDIUM": 0.08,
            "HARD": 0.05
        }
        
    }
}

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

SAVE_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "track_characteristics.pkl"
)

with open(SAVE_PATH, "wb") as f:
    pickle.dump(track_characteristics, f)

print("Track characteristics saved.")