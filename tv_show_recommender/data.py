import os
import gzip
from pathlib import Path

import requests

OUTPUT_DIR = "data"
IMDB_URL = "https://datasets.imdbws.com"
TITLE_BASICS_FILE_NAME = "title.basics.tsv.gz"
TITLE_RATINGS_FILE_NAME = "title.ratings.tsv.gz"

# Create a script:
# Generate list of ids every title that:
# - is a tvSeries
# - has numVotes > 10

# For each title_id
# Scrape all reviews { user_id, title_id, review_num } ...?


def download_imdb_title_basics():
    _download(TITLE_BASICS_FILE_NAME)


def download_imdb_title_ratings():
    _download(TITLE_RATINGS_FILE_NAME)


def unzip_imdb_title_basics():
    in_file_path = os.path.join(OUTPUT_DIR, TITLE_BASICS_FILE_NAME)
    out_file_path = os.path.join(OUTPUT_DIR, "title.basics.tsv")
    _decompress(in_file_path, out_file_path)


def unzip_imdb_title_ratings():
    in_file_path = os.path.join(OUTPUT_DIR, TITLE_RATINGS_FILE_NAME)
    out_file_path = os.path.join(OUTPUT_DIR, "title.ratings.tsv")
    _decompress(in_file_path, out_file_path)


def _decompress(infile, tofile):
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def _download(title_file_name):
    out_file_path = os.path.join(OUTPUT_DIR, title_file_name)
    url = f"{IMDB_URL}/{title_file_name}"

    response = requests.get(url, stream=True)

    filename = Path(out_file_path)
    filename.touch(exist_ok=True)

    with open(out_file_path, "wb") as output:
        output.write(response.content)
