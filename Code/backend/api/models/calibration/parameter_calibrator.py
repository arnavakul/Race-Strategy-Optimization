#what this model does : 

# 1. Load telemetry stint
# 2. Run simulator
# 3. Compute MAE
# 4. Modify parameters
# 5. Re-run simulation
# 6. Keep best parameters

from api.models.evaluation.validate_stint import(
    validate_stint
)

from api.models.simulation.track_model import(
    TRACK_CHARACTERISTICS
)

def calibrate_soft_degradation():
    best_mae = float("inf")
    
    best_deg = None
    
    track_key = "bahrain_2024"
    
    original_deg = (
        TRACK_CHARACTERISTICS[track_key]["compound_deg"]["SOFT"]
    )
    
    test_values = [

        -0.01,
        -0.02,
        -0.03,
        -0.04,
        -0.05,
        -0.06,
        -0.07
    ]
    
    for deg in test_values: 
        TRACK_CHARACTERISTICS[track_key]["compound_deg"]["SOFT"] = deg
        
        result = validate_stint(
            track="bahrain",
            year = 2024,
            driver="VER",
            compound="SOFT",
            start_lap=1,
            end_lap=15
        )
        
        mae = result["mae"]
        
        print(
            f"Deg:{deg:.4f}|"
            f"MAE: {mae:.4f}"            
        )
        
        if mae < best_mae:
            best_mae =  mae
            best_deg = deg
        
    TRACK_CHARACTERISTICS[track_key]["compound_deg"]["SOFT"] = original_deg
    
    print("\n Best Parameters\n")
    print(f"Best MAE: {best_mae}")
    print(f"Best DEG: {best_deg}")

if __name__ == "__main__":
    calibrate_soft_degradation()