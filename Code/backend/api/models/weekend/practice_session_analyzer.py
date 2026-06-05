import pandas as pd
from scipy.stats import linregress


def load_practice_data(file_path):

    return pd.read_parquet(
        file_path
    )


def get_best_lap(
    session_df,
    driver
):

    driver_laps = session_df[
        session_df["Driver"] == driver
    ]

    if driver_laps.empty:
        return None

    return driver_laps[
        "LapTimeSeconds"
    ].min()


def calculate_representative_pace(
    session_df,
    driver
):

    driver_laps = session_df[
        session_df["Driver"] == driver
    ]

    valid_laps = driver_laps[
        (driver_laps["TrackStatus"] == "1")
        &
        (driver_laps["IsAccurate"] == True)
    ].copy()

    if valid_laps.empty:
        return None

    q1 = valid_laps[
        "FuelCorrectedLapTime"
    ].quantile(0.25)

    q3 = valid_laps[
        "FuelCorrectedLapTime"
    ].quantile(0.75)

    iqr = q3 - q1

    valid_laps = valid_laps[
        (
            valid_laps[
                "FuelCorrectedLapTime"
            ]
            >= q1 - 1.5 * iqr
        )
        &
        (
            valid_laps[
                "FuelCorrectedLapTime"
            ]
            <= q3 + 1.5 * iqr
        )
    ]
    
    valid_laps = valid_laps[
        valid_laps[
            "FuelCorrectedLapTime"
        ]
        <
        (
            valid_laps[
                "FuelCorrectedLapTime"
            ].median()
            + 5
        )
    ]

    if valid_laps.empty:
        return None

    best_run = valid_laps.nsmallest(
        min(10, len(valid_laps)),
        "FuelCorrectedLapTime"
    )

    return best_run[
        "FuelCorrectedLapTime"
    ].mean()

def calculate_degradation_rate(
    session_df,
    driver
):

    driver_laps = session_df[
        session_df["Driver"] == driver
    ]

    driver_laps = driver_laps[
        (driver_laps["TrackStatus"] == "1")
        &
        (driver_laps["IsAccurate"] == True)
    ]

    if driver_laps.empty:
        return None

    degradation_values = []

    for _, stint_df in driver_laps.groupby(
        "Stint"
    ):

        if len(stint_df) < 2:
            continue

        stint_df = stint_df.sort_values(
            "LapNumber"
        )

        first_lap = stint_df[
            "FuelCorrectedLapTime"
        ].iloc[0]

        last_lap = stint_df[
            "FuelCorrectedLapTime"
        ].iloc[-1]

        slope, _, _, _, _ = linregress(
                stint_df["TyreLife"],
                stint_df["FuelCorrectedLapTime"]
            )

        degradation_values.append(
                slope
            )

    if len(
        degradation_values
    ) == 0:

        return None

    return sum(
        degradation_values
    ) / len(
        degradation_values
    )


def calculate_consistency(
    session_df,
    driver
):

    driver_laps = session_df[
        session_df["Driver"] == driver
    ]

    filtered_laps = driver_laps[
        (driver_laps["TyreLife"] >= 5)
        &
        (driver_laps["TrackStatus"] == "1")
    ]

    if filtered_laps.empty:
        return None

    laps = filtered_laps[
        "FuelCorrectedLapTime"
    ]

    q1 = laps.quantile(0.25)

    q3 = laps.quantile(0.75)

    iqr = q3 - q1

    laps = laps[
        (laps >= q1 - 1.5 * iqr)
        &
        (laps <= q3 + 1.5 * iqr)
    ]

    if len(laps) < 2:
        return None

    return laps.std()


def generate_practice_report(
    session_df,
    driver
):

    best_lap = get_best_lap(
        session_df,
        driver
    )

    long_run_pace = (
        calculate_representative_pace(
            session_df,
            driver
        )
    )

    degradation = (
        calculate_degradation_rate(
            session_df,
            driver
        )
    )

    consistency = (
        calculate_consistency(
            session_df,
            driver
        )
    )

    return {

        "driver":
            driver,

        "best_lap":
            None
            if best_lap is None
            else round(
                float(best_lap),
                3
            ),

        "long_run_pace":
            None
            if long_run_pace is None
            else round(
                float(long_run_pace),
                3
            ),

        "degradation_rate":
            None
            if degradation is None
            else round(
                float(degradation),
                3
            ),

        "consistency":
            None
            if consistency is None
            else round(
                float(consistency),
                3
            )
    }


def analyze_all_drivers(
    session_df
):

    reports = []

    drivers = sorted(
        session_df[
            "Driver"
        ].unique()
    )

    for driver in drivers:

        report = (
            generate_practice_report(
                session_df,
                driver
            )
        )

        reports.append(
            report
        )

    rankings = pd.DataFrame(
        reports
    )

    quali_rankings = rankings.sort_values(
        by="best_lap",
        ascending=True
    )

    race_rankings = rankings.sort_values(
        by="long_run_pace",
        ascending=True
    )

    return quali_rankings, race_rankings

if __name__ == "__main__":

    file_path = (
        r"C:\DevProjects\Race Strategy Optimization"
        r"\Code\backend\data\processed"
        r"\FP1\clean_laps"
        r"\monaco_2026_FP1_clean.parquet"
    )

    df = load_practice_data(
        file_path
    )
    
    print(
        df.groupby(
            "Driver",
            observed=False
        )[
            "LapTimeSeconds"
        ].min().sort_values()
    )
    
    quali_rankings, race_rankings = (
        analyze_all_drivers(df)
    )

    print(
        "\nQUALIFYING PACE RANKINGS\n"
    )

    print(
        quali_rankings
    )

    print(
        "\nTOP 10 LONG RUN PACE\n"
    )

    print(
        race_rankings.head(10)
    )