# Loading collection raph
# -----------------------

# Path of collection data file (str, pointing to .xlsx file)
collection_path = "data/raw/dm_records_20-03-02s.xlsx"

# Columns from collection file to include in Album-DataFrame (list)
collection_cols = ["Artist", "Album"]

# Genre(s) to load (list or None, if all albums are to be loaded)
collection_genres = ["Death Metal"]


# Audio features
# --------------

# Audio features to request (list)
feature_list = [
    "danceability",
    "energy",
    "key",
    "mode",
    "instrumentalness",
    "valence",
    "tempo",
    "loudness",
    "duration_ms",
]


# Outlier removal
drop_outliers = True
IQR_dist = 1.5
outlier_thx = 2

args_outliers = [
    drop_outliers,
    IQR_dist,
    outlier_thx,
]
