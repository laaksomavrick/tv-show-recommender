from pandas import read_table, concat

from tv_show_recommender.data import (
    download_imdb_title_basics,
    download_imdb_title_ratings,
    unzip_imdb_title_basics,
    unzip_imdb_title_ratings,
    needs_retrieving, OUTPUT_DIR, TITLE_BASICS_FILE_NAME, TITLE_RATINGS_FILE_NAME
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

    tv_series_df = basics_df[basics_df['titleType'] == 'tvSeries']

    tv_with_ratings = concat([tv_series_df.set_index('tconst'), ratings_df.set_index('tconst')],  axis=1, join='inner')

    tv_with_enough_votes = tv_with_ratings[(tv_with_ratings["numVotes"] > 500) & (tv_with_ratings["primaryTitle"].notnull())]

    print(len(tv_with_enough_votes))
    # print(tv_with_enough_votes.sort_values("numVotes", ascending=False).head())

    # For every show:
        # Collect every review { user_id, show_id, rating }
    # https://www.imdb.com/title/tt0944947/reviews/
    # https://www.imdb.com/user/ur59092557/ratings

