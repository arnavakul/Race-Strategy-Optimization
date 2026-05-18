from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

# ======================
# DATA PATHS
# ======================

DATA_PATH = (
    PROJECT_ROOT
    / "data"
)

RAW_DATA_PATH = (
    DATA_PATH
    / "raw"
)

PROCESSED_PATH = (
    DATA_PATH
    / "processed"
)

FULL_LAPS_PATH = (
    PROCESSED_PATH
    / "full_laps"
)

CLEAN_LAPS_PATH = (
    PROCESSED_PATH
    / "clean_laps"
)

TELEMETRY_PATH = (
    DATA_PATH
    / "telemetry"
)

WEATHER_DATA_PATH = (
    DATA_PATH
    / "weather"
)

PITSTOP_DATA_PATH = (
    DATA_PATH
    / "pitstop_data"
)

# ======================
# MODEL PATHS
# ======================

MODELS_PATH = (
    PROJECT_ROOT
    / "api"
    / "models"
)

SAVED_MODELS_PATH = (
    MODELS_PATH
    / "saved_models"
)

# ======================
# OUTPUT PATHS
# ======================

OUTPUTS_PATH = (
    PROJECT_ROOT
    / "outputs"
)

SIMULATION_OUTPUTS_PATH = (
    OUTPUTS_PATH
    / "simulations"
)

REPORTS_PATH = (
    OUTPUTS_PATH
    / "reports"
)

VISUALIZATION_PATH = (
    OUTPUTS_PATH
    / "visualizations"
)

# ======================
# CACHE PATHS
# ======================

CACHE_PATH = (
    PROJECT_ROOT
    / "cache"
)

ALL_PATHS = [
    RAW_DATA_PATH,
    PROCESSED_PATH,
    FULL_LAPS_PATH,
    CLEAN_LAPS_PATH,
    TELEMETRY_PATH,
    WEATHER_DATA_PATH,
    PITSTOP_DATA_PATH,
    SAVED_MODELS_PATH,
    OUTPUTS_PATH,
    SIMULATION_OUTPUTS_PATH,
    REPORTS_PATH,
    VISUALIZATION_PATH,
    CACHE_PATH
]

for path in ALL_PATHS:
    path.mkdir(
        parents=True,
        exist_ok=True
    )


from api.config.paths import REPORTS_PATH