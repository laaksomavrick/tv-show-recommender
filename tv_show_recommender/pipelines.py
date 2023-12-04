from sklearn.pipeline import Pipeline
from tv_show_recommender.transformers import (
    AddIsLikedAttribute,
    DropColumns,
    DropDuplicates,
    PivotShowIds,
    AddGraphPartitionIdAttribute,
)


def get_basic_nn_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_columns = DropColumns(
        columns_to_drop=[
            "rating",
            "primary_title",
            "start_year",
            "end_year",
            "genres",
            "average_rating",
            "num_votes",
        ]
    )

    pipeline = Pipeline(
        [
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
        ]
    )

    return pipeline


def get_cluster_labeled_nn_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_columns = DropColumns(
        columns_to_drop=["rating", "primary_title", "end_year", "genres", "num_votes"]
    )
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])
    add_graph_partition_id_attr = AddGraphPartitionIdAttribute()

    pipeline = Pipeline(
        [
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
            ("drop_duplicates", drop_duplicates),
            ("add_graph_partition_id_attr", add_graph_partition_id_attr),
        ]
    )

    return pipeline
