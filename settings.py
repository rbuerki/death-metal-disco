# Loading collection raph
# -----------------------

# Path of collection data file (str, pointing to .xlsx file)
collection_path = "data/dm_records_20-02-17.xlsx"

# Columns from collection file to include in DataFrame (list)
collection_cols = ["Artist", "Titel"]

# Genre(s) to load (list or None, if all albums are to be loaded)
collection_genres = ["Death Metal"]


# Audio features
# --------------

# Audio features to request (list)
feature_list = ['danceability',
                'energy',
                'key',
                'mode',
                'instrumentalness',
                'valence',
                'tempo',
                'loudness',
                'duration_ms',
                ]

#