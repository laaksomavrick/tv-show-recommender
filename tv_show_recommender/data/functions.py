import os

import pandas as pd


def get_training_data():
    # TODO: split up
    return None


def get_test_data():
    # TODO: split up
    return None


def get_all_data():
    return _get_ratings_data()


def _get_ratings_data():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(os.path.join(project_root, "data/pristine_ratings.csv"))
