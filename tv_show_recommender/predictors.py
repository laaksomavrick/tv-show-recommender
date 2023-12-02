import pandas as pd


def predict_nearest_neighbor(show_ids, model=None, df=pd.DataFrame(data={})):
    if model is None:
        raise "Model must be set"
    if (len(df)) == 0:
        return []
    if len(show_ids) == 0:
        return []

    liked_shows_indices = []

    for show_id in show_ids:
        show_index = df.columns.get_loc(show_id)
        liked_shows_indices.append(show_index)

    liked_shows_subset = df[show_ids]
    liked_shows_subset_transposed = liked_shows_subset.T

    distances, indices = model.kneighbors(liked_shows_subset_transposed, n_neighbors=3)

    # Rank based on distance
    similar_shows_indices = indices.flatten().tolist()
    similar_show_ids = df.columns[similar_shows_indices]
    similar_distances = distances.flatten()

    similar_shows_with_distances = dict(zip(similar_show_ids, similar_distances))
    sorted_similar_shows = sorted(
        similar_shows_with_distances.items(), key=lambda x: x[1]
    )

    sorted_show_ids = [show[0] for show in sorted_similar_shows]

    # Filter shows included in provided show_ids
    sorted_show_ids = [x for x in sorted_show_ids if x not in show_ids]

    return sorted_show_ids
