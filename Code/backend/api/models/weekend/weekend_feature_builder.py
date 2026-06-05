import pandas as pd
from api.models.weekend.practice_session_analyzer import (
    generate_practice_report
)

import os

output_folder = (
    r"C:\DevProjects\Race Strategy Optimization"
    r"\Code\backend\data\weekend_datasets"
    r"\Monaco"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

def load_weekend_data(fp1_file,fp2_file,fp3_file,quali_file):
    fp1 = pd.read_parquet(
        fp1_file
    )
    
    fp2 = pd.read_parquet(
        fp2_file
    )
        
    fp3 = pd.read_parquet(
        fp3_file
    )
    
    qualifying = pd.read_parquet(
        quali_file
    )
    
    return (
        fp1,
        fp2,
        fp3,
        qualifying
    )

def extract_session_features(session_df):
    
    features = {}
    
    drivers = sorted(
        session_df["Driver"].unique()
    )
    
    for driver in drivers:
        
        features[driver] = (
            generate_practice_report(
                session_df,driver
            )
        )

    return features


def build_weekend_dataset(
    fp1_df,
    fp2_df,
    fp3_df,
    quali_df
):
    fp1_features = (
        extract_session_features(
            fp1_df
        )
    )
    
    fp2_features = (
    extract_session_features(
            fp2_df
        )
    )

    fp3_features = (
        extract_session_features(
            fp3_df
        )
    )
    
    rows = []
    
    drivers = sorted(
        quali_df["Driver"].unique()
    )
    
    for driver in drivers:
        
        quali_driver = quali_df[
            quali_df["Driver"] == driver
        ]
        
        if quali_driver.empty:
            continue
        
        target_quali_time = (
            quali_driver[
                "LapTimeSeconds"
            ].min()
        )
        
        if (
            driver not in fp1_features
            or driver not in fp2_features
            or driver not in fp3_features
        ):
            continue
        
        row = {

            "driver": driver,

            "fp1_best_lap":
                fp1_features[driver]["best_lap"],

            "fp2_best_lap":
                fp2_features[driver]["best_lap"],

            "fp3_best_lap":
                fp3_features[driver]["best_lap"],

            "fp1_long_run":
                fp1_features[driver]["long_run_pace"],

            "fp2_long_run":
                fp2_features[driver]["long_run_pace"],

            "fp3_long_run":
                fp3_features[driver]["long_run_pace"],

            "fp1_deg":
                fp1_features[driver]["degradation_rate"],

            "fp2_deg":
                fp2_features[driver]["degradation_rate"],

            "fp3_deg":
                fp3_features[driver]["degradation_rate"],

            "target_quali_time":
                target_quali_time
        }
        
        rows.append(row)
        
        
    weekend_dataset = pd.DataFrame(
        rows
    )
            
    return weekend_dataset


if __name__ == "__main__":

    fp1_file = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\processed"
        r"\FP1\clean_laps"
        r"\monaco_2025_FP1_clean.parquet"
    )

    fp2_file = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\processed"
        r"\FP2\clean_laps"
        r"\monaco_2025_FP2_clean.parquet"
    )

    fp3_file = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\processed"
        r"\FP3\clean_laps"
        r"\monaco_2025_FP3_clean.parquet"
    )

    quali_file = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\processed"
        r"\Q\clean_laps"
        r"\monaco_2025_Q_clean.parquet"
    )

    fp1_df, fp2_df, fp3_df, quali_df = (
        load_weekend_data(
            fp1_file,
            fp2_file,
            fp3_file,
            quali_file
        )
    )

    weekend_dataset = (
        build_weekend_dataset(
            fp1_df,
            fp2_df,
            fp3_df,
            quali_df
        )
    )

    weekend_dataset.to_parquet(
        os.path.join(
            output_folder,
            "monaco_2025_weekend.parquet"
        ),
        index=False
    )

    weekend_dataset.to_csv(
        os.path.join(
            output_folder,
            "monaco_2025_weekend.csv"
        ),
        index=False
    )

    print(
        weekend_dataset.head()
    )

    print(
        weekend_dataset.shape
    )