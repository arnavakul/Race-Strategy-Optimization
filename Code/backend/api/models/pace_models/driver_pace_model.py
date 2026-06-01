import os
import pandas as pd
import joblib

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error,

    r2_score
)

from sklearn.preprocessing import (
    LabelEncoder
)

from sklearn.model_selection import (
    train_test_split
)

from sklearn.ensemble import (
    RandomForestRegressor
)

# Load every parquet file from:
# data/processed/clean_laps/
# Merge into one dataframe
# Remove null value
# Return dataframe
def load_training_data():

    data_folder = (
        "data/processed/clean_laps"
    )

    all_dataframes = []

    for file in os.listdir(
        data_folder
    ):

        if file.endswith(
            ".parquet"
        ):

            path = os.path.join(
                data_folder,
                file
            )

            df = pd.read_parquet(
                path
            )

            all_dataframes.append(
                df
            )

    if len(all_dataframes) == 0:

        raise ValueError(
            "No parquet files found in clean_laps folder."
        )

    combined_df = pd.concat(

        all_dataframes,

        ignore_index=True
    )

    combined_df = combined_df.dropna(

        subset=[

            "Driver",

            "Team",

            "LapNumber",

            "Position",

            "Compound",

            "TyreLife",

            "Stint",

            "TrackStatus",

            "RaceYear",

            "Track",

            "NormalizedLapTime"
        ]
    )

    combined_df = (
        combined_df.reset_index(
            drop=True
        )
    )

    return combined_df


def encode_features(df):

    encoders = {}

    #Driver Encoder

    driver_encoder = LabelEncoder()

    df["Driver"] = (

        driver_encoder.fit_transform(
            df["Driver"]
        )
    )

    encoders["Driver"] = (
        driver_encoder
    )

    #Team Encoder

    team_encoder = LabelEncoder()

    df["Team"] = (

        team_encoder.fit_transform(
            df["Team"]
        )
    )

    encoders["Team"] = (
        team_encoder
    )

    #Track Encoder

    track_encoder = LabelEncoder()

    df["Track"] = (

        track_encoder.fit_transform(
            df["Track"]
        )
    )

    encoders["Track"] = (
        track_encoder
    )
    
    #Compound Encoder

    compound_encoder = LabelEncoder()

    df["Compound"] = (

        compound_encoder.fit_transform(
            df["Compound"]
        )
    )

    encoders["Compound"] = (
        compound_encoder
    )

    FEATURES = [

        "Driver",

        "Team",

        "Track",

        "Compound",

        "TyreLife",

        "Stint",

        "RaceYear"
    ]

    TARGET = (
        "NormalizedLapTime"
    )

    X = df[FEATURES]

    y = df[TARGET]

    return (

        X,

        y,

        encoders
    )


def train_driver_pace_model():

    df = load_training_data()

    print(
        f"\nRows Loaded: {len(df)}"
    )

    print(
        f"Columns Loaded: {len(df.columns)}"
    )

    print(
        "\nDriver Count:"
    )

    print(
        df["Driver"].nunique()
    )

    print(
        "\nTrack Count:"
    )

    print(
        df["Track"].nunique()
    )

    print(
        "\nCompound Distribution:"
    )

    print(
        df["Compound"].value_counts()
    )

    print(
        "\nTrack Status Distribution:"
    )

    print(
        df["TrackStatus"].value_counts()
    )

    X, y, encoders = (
        encode_features(df)
    )

    X_train,\
    X_test,\
    y_train,\
    y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42
    )

    model = RandomForestRegressor(

        n_estimators=200,  # MORE STABLE MORE SLOWER No of trees

        max_depth=15,      # not making the tree infinitely complex

        random_state=42,

        n_jobs=-1          # use all cpu cores
    )

    print(
        "\nTraining Model...\n"
    )

    model.fit(

        X_train,

        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = (
        mean_squared_error(
            y_test,
            predictions
        )
    ) ** 0.5

    r2 = r2_score(

        y_test,

        predictions
    )

    print(
        "\nMODEL RESULTS\n"
    )

    print(
        f"MAE: {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"R²: {r2:.4f}"
    )

    feature_importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": model.feature_importances_
    })

    feature_importance = (
        feature_importance.sort_values(

            by="Importance",

            ascending=False
        )
    )

    print(
        "\nFEATURE IMPORTANCE"
    )

    print(
        feature_importance
    )

    os.makedirs(

        "outputs/model_reports",

        exist_ok=True
    )

    feature_importance.to_csv(

        "outputs/model_reports/driver_pace_feature_importance.csv",

        index=False
    )

    os.makedirs(

        "saved_models",

        exist_ok=True
    )

    #Saving the model

    joblib.dump(

        model,

        "saved_models/driver_pace_model_v1.pkl"
    )

    #Saving the encoders

    joblib.dump(

        encoders,

        "saved_models/driver_pace_encoders.pkl"
    )

    print(
        "\nModel Saved Successfully\n"
    )

    return {

        "mae": mae,

        "rmse": rmse,

        "r2": r2
    }


if __name__ == "__main__":

    print(
        "\nTRAINING DRIVER PACE MODEL\n"
    )

    train_driver_pace_model()
    
    