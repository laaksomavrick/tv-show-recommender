from pandas import read_table, concat

from data.data import (
    download_imdb_title_basics,
    download_imdb_title_ratings,
    unzip_imdb_title_basics,
    unzip_imdb_title_ratings,
    needs_retrieving,
    OUTPUT_DIR,
    TITLE_BASICS_FILE_NAME,
    TITLE_RATINGS_FILE_NAME,
)
from os.path import join


# Create a script:
# Generate list of ids every title that:
# - is a tvSeries
# - has numVotes > 10

# For each title_id
# Scrape all reviews { user_id, title_id, review_num } ...?


def start():
    if needs_retrieving():
        print("Downloading and unzipping files...")
        download_imdb_title_basics()
        download_imdb_title_ratings()
        unzip_imdb_title_basics()
        unzip_imdb_title_ratings()

    basics_file_path = join(OUTPUT_DIR, TITLE_BASICS_FILE_NAME)
    ratings_file_path = join(OUTPUT_DIR, TITLE_RATINGS_FILE_NAME)

    basics_df = read_table(basics_file_path)
    ratings_df = read_table(ratings_file_path)

    tv_series_df = basics_df[basics_df["titleType"] == "tvSeries"]
    tv_with_ratings = concat(
        [tv_series_df.set_index("tconst"), ratings_df.set_index("tconst")],
        axis=1,
        join="inner",
    )
    tv_with_enough_votes = tv_with_ratings[
        (tv_with_ratings["numVotes"] > 700)
        & (tv_with_ratings["primaryTitle"].notnull())
    ]

    sorted_tv_shows = tv_with_enough_votes.sort_values("numVotes", ascending=False)

    sorted_tv_shows = sorted_tv_shows.index.to_frame(name="id").join(sorted_tv_shows)
    sorted_tv_shows.to_csv(join(OUTPUT_DIR, "shows.csv"))
