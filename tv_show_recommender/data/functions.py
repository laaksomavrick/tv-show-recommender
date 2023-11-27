import os

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


def stratified_shuffle(data, column):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(data, data[column]):
        strat_train_set = data.loc[train_index]
        strat_test_set = data.loc[test_index]

    return strat_train_set, strat_test_set


def get_split_data(test_ratio):
    data = _get_ratings_data()
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


def get_all_data():
    return _get_ratings_data()


def _get_ratings_data():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(os.path.join(project_root, "data/pristine_ratings.csv"))
