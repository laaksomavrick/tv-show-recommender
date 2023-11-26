import os

import pandas as pd


def start():
    dfs = []
    ratings_directory = "data/files/ratings"
    ratings_files = os.listdir(ratings_directory)

    for file_name in ratings_files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(ratings_directory, file_name)
            df = pd.read_csv(file_path)
            dfs.append(df)

    combined_ratings = pd.concat(dfs, ignore_index=True)
    combined_ratings.to_csv(os.path.join(ratings_directory, "ratings.csv"), index=False)
