
import numpy as np
import pandas as pd

from project import go_now


collection = pd.read_excel("data/dm_records_20-02-17.xlsx",
                           encoding='utf-8')

# albums_list = list(zip(collection["Artist"], collection['Titel']))

album_df = (collection[["Artist", "Titel"]].
            loc[collection["Genre"] == "Death Metal"])

album_df = album_df.iloc[8:12]
print(album_df)


def create_albums_df(album_df):
    data_list = []
    keys = []
    for album in album_df.itertuples():
        try:
            audio_features = go_now(album[1], album[2])
            data_list.append(audio_features)
            if len(keys) == 0:
                keys = audio_features.index
        except:
            print(f"{album[2]} not found on Spotify")
            data_list.append(pd.Series(np.zeros(len(keys))))

    data_df = pd.concat(data_list, axis=1, keys=keys)
    return data_df


album_data = create_albums_df(album_df)
print(album_data)
