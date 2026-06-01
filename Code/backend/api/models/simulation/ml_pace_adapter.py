# 1. Load trained model

# 2. Load encoders

# 3. Convert race state
#    into ML features

# 4. Predict normalized pace

# 5. Return prediction

import joblib
import os
import pandas as pd

MODEL = joblib.load(
    "saved_models/driver_pace_model_v1.pkl"
)

ENCODERS = joblib.load(
    "saved_models/driver_pace_encoders.pkl"
)

def encode_value(encoder,value):
    try:
        return(
            encoder.transform(
                [value]
            )[0]
        )
    except:
        return 0

def predict_driver_pace(
    driver,team,track,compound,tyre_life,position,stint,race_year
):
    #Driver Encoded
    driver_encoded = (
        encode_value(
            ENCODERS["Driver"],driver
        )
    )
    
    #Team Encoded
    team_encoded = (
        encode_value(
            ENCODERS["Team"],team
        )
    )
    
    #Track Encoded
    track_encoded = (
        encode_value(
            ENCODERS["Track"],track
        )
    )
    
    #Compound Encoded
    compound_encoded = (
        encode_value(
            ENCODERS["Compound"],compound
        )
    )
    
    features = pd.DataFrame([{
        "Driver":driver_encoded,
        "Team":team_encoded,
        "Track":track_encoded,
        "Compound":compound_encoded,
        "TyreLife":tyre_life,
        "Position":position,
        "Stint":stint,
        "RaceYear":race_year
    }])
    
    prediction = MODEL.predict(
        features
    )[0]
    
    return prediction

if __name__ == "__main__":

    scenarios = [

        ("VER","Red Bull","bahrain","SOFT",2,1,1,2024),

        ("VER","Red Bull","bahrain","MEDIUM",10,1,1,2024),

        ("VER","Red Bull","bahrain","HARD",25,1,2,2024),

        ("NOR","McLaren","bahrain","MEDIUM",12,2,1,2024),

        ("LEC","Ferrari","bahrain","HARD",30,5,2,2024)
    ]

    for scenario in scenarios:

        prediction = predict_driver_pace(
            *scenario
        )

        print(
            scenario,
            prediction
        )

def get_ml_pace_adjustment(
    driver,team,track,compound,tyre_life,position,stint,race_year
):
    
    prediction = predict_driver_pace(
        driver=driver,
        team=team,
        track=track,
        compound=compound,
        tyre_life=tyre_life,
        position=position,
        stint=stint,
        race_year=race_year
    )
    
    baseline = 4.0
    
    scale = 0.10
    
    adjustment = (
        prediction - baseline
    )*scale
    
    return adjustment