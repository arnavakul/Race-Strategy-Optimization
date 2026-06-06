# import os 
# import pandas as pd 

# TRACKS = [
#     "Abu Dhabi",
#     "Austria",
#     "Bahrain",
#     "Barcelona",
#     "Brazil",
#     "COTA",
#     "Hungary",
#     "Jeddah",
#     "Melbourne",
#     "Monaco",
#     "Monza",
#     "Montreal",
#     "Qatar",
#     "Silverstone",
#     "Singapore",
#     "Spa",
#     "Suzuka"
# ]

# YEARS = [
#     2022,2023,2024,2025
# ]

# def load_quali_session(track,year):
    
#     file_path = os.path.join(
#         processed_path,
#         "Q",
#         "clean_laps",
#         f"{track.lower().replace(' ','_')}_{year}_Q_clean.parquet"
#     )

# def build_quali_classification(
#     q_df
# ):
    
#     classification = (
#         q_df
#         .groupby(
#             ["Driver","Team"],
#             observed=True
#         )["LapTimeSeconds"]
#         .min()
#         .reset_index()
#     )
    
#     classification = (
#         classification
#         .sort_values(
#             "LapTimeSeconds"
#         )
#     )
    
#     classification[
#         "QualiPosition"
#     ] = range(
#         1,
#         len(classification)+1
#     )
    
#     return classification

# def load_race_session(
#     track,
#     year
# ):


# def build_race_classification(
#     race_df
# ):
    
#     classification = (
#         race_df
#         .groupby(
#             ["Driver","Team"],
#             observed=True
#         )["Position"]
#         .last()
#         .reset_index()
#     )
    
#     classification = (
#         classification
#         .sort_values(
#             "Position"
#         )
#     )

# def build_historical_results():
    
#     rows = []
    
#     for track in TRACKS:

#         for year in YEARS:

import pandas as pd

df = pd.read_parquet(
    r"C:\DevProjects\Race Strategy Optimization\Code\backend\data\processed\R\clean_laps\australia_2026_R_clean.parquet"
)

print(df.columns.tolist())