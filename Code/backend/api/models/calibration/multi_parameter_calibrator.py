from itertools import product
from api.models.evaluation.validate_stint import (
    validate_stint
)
from api.models.simulation.track_model import (
    TRACK_CHARACTERISTICS
)

def calibrate():
    track_key = "bahrain_2024"
    
    best_mae = float("inf")
    best_params =  None
    
    deg_values = [
        -0.03,
        -0.05,
        -0.07
    ]
    
    cliff_values = [
        0.08,
        0.10,
        0.12
    ]
    
    for deg,cliff in product(
        deg_values,
        cliff_values
    ):
        TRACK_CHARACTERISTICS[
            track_key
        ]["compound_deg"]["SOFT"] = deg
        
        TRACK_CHARACTERISTICS[
            track_key
        ]["cliff_multiplier"]["SOFT"] = cliff
        
        result = validate_stint(
            track="bahrain",
            year=2024,
            driver="VER",
            compound="SOFT",
            start_lap=1,
            end_lap=15
        )
        
        mae = result["mae"]
        
        print(
            f"Deg: {deg:.3f} | "
            f"Cliff: {cliff:.3f} | "
            f"MAE: {mae:.4f}"
        )
        
        if mae < best_mae:
            best_mae = mae
            
            best_params = {
                "deg": deg,
                "cliff": cliff
            }
    
    print("\nBEST PARAMETERS\n")

    print(best_params)

    print(f"\nBest MAE: {best_mae}")
    

if __name__ == "__main__":

    calibrate()