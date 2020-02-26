import pandas as pd
import load


# ALTERNATIVE FOR DATA CONTAINING AUDIO FEATURES OF ALL SONGS INVIDUALLY


def go_and_request_for_individual_songs(artist_name, album_name, feature_list):
    """Combine most of the different function and request the audio
    features for an album from the Spotify API. Create a list of
    DataFrames.

    Args:
        artist_name (str): Name of the artist
        album_name (str): Name of the album
        feature_list (list): List of strings containing the names
            of the audio features to be returned, passed from
            create_album_data function

    Returns:
        pd.Series: Mean of audio features for the entire album
    """
    album_uri = load.get_album_uri(artist_name, album_name)
    tracklist = load.get_album_tracklist(album_uri)
    audio_features = load.get_audio_features(tracklist, feature_list)

    return audio_features


def create_songs_data(collection, feature_list):
    """For every album in collection request the Spotify audio features (values
    of all the individual songs per album) and return them as new DataFrame.

    Args:
        collection (DataFrame): Collection DataFrame, output of
            'load collection' function
        feature_list (list): List of strings containing the names of the audio
            features to be returned, filters the relevant ones

    Returns:
        pd.DataFrame: New dataframe containing the relevant audio features for
            every song in the requested albums.
    """

    data_list = []
    for album in collection.itertuples():
        try:
            audio_features = go_and_request_for_individual_songs(album[1],
                                                                 album[2],
                                                                 feature_list)
            audio_features['Artist'] = album[1]
            audio_features['Album'] = album[2]
            data_list.append(audio_features)
        except IndexError:
            print(f"{album[1]} - {album[2]} NOT FOUND on Spotify")

    data_df = pd.concat(data_list, ignore_index=True)
    data_df.columns = ['Artist', 'Album'] + feature_list

    return data_df
