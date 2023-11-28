from sklearn.base import BaseEstimator, TransformerMixin


class AddIsLikedAttribute(BaseEstimator, TransformerMixin):
    def __init__(self):
        super()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X["is_liked"] = (X["rating"] >= 8).astype(int)
        return X


class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.drop(columns=self.columns_to_drop, errors="ignore")
        return X
