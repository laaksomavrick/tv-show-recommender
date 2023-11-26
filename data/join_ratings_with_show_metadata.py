import re
from os.path import join

from pandas import concat, read_csv, merge


def snake_case(column_name):
    return column_name.lower().replace(" ", "_")


def start():
    data_directory = "data/files"
    basics_file_path = join(data_directory, "shows.csv")
    ratings_file_path = join(data_directory, "ratings/ratings.csv")

    basics_df = read_csv(basics_file_path)
    basics_df = basics_df.drop(
        columns=["id", "titleType", "originalTitle", "isAdult", "runtimeMinutes"]
    )

    ratings_df = read_csv(ratings_file_path)

    ratings_with_show = merge(
        ratings_df, basics_df, left_on="show_id", right_on="tconst", how="inner"
    ).drop(columns=["tconst"])
    ratings_with_show.columns = [
        re.sub(r"(?<!^)(?=[A-Z])", "_", col).lower()
        for col in ratings_with_show.columns
    ]

    ratings_with_show.to_csv(join(data_directory, "pristine_ratings.csv"), index=False)
