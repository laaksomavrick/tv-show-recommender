from tv_show_recommender.data import (
    download_imdb_title_basics,
    download_imdb_title_ratings,
    unzip_imdb_title_basics,
    unzip_imdb_title_ratings,
)


def start():
    download_imdb_title_basics()
    download_imdb_title_ratings()
    unzip_imdb_title_basics()
    unzip_imdb_title_ratings()
