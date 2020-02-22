import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import numpy as np
import pandas as pd

# Import credentials and instantiate client with authorization
SPOTIPY_CLIENT_ID = credentials.client_id
SPOTIPY_CLIENT_SECRET = credentials.client_secret

ccm = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                               client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=ccm)

album_name = ""
artist_name = ""


def get_album_uri(artist_name, album_name):
    """Request the Spotify URI for a specific album.

   Args:
        artist_name (str): Name of the artist
        album_name (str): Name of the album

    Returns:
        str: The URI of the album
    """

    q = f"artist:{artist_name} album:{album_name}"
    results = sp.search(q, type='album')
    items = results['albums']['items']
    album_uri = items[0]['uri']
    return album_uri


def get_album_tracklist(album_uri):
    """Get the list of track URI for all songs in an album.

    Args:
        album_uri (string): Album URI, output of get_album_uri function

    Returns:
        list: list of track URI for an album
    """

    tracklist = []
    album = sp.album(album_uri)
    for track in album['tracks']['items']:
        tracklist.append(track['uri'])
    return tracklist


def get_audio_features(tracklist, feature_list):
    """Get a list of audio analyses for the tracks in the tracklist.
    Each analysis is a dict containing audio features and other information
    about the individual tracks.

    Documentation here:
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/

    Args:
        tracklist (list): List of track URI strings, output of
            get_album_tracklist function
        feature_list (list): List of audio feature names to be
            returned, filters the relevant ones.

    Returns:
        pd.DataFrame: Row-wise representation of relevant audio features
            for every song in the album
    """

    audio_features_list_of_dicts = sp.audio_features(tracklist)
    audio_features = pd.DataFrame(audio_features_list_of_dicts)
    audio_features = audio_features[feature_list]
    return audio_features


def calculate_mean_feature_values(audio_features):
    """Calculate and return the mean values of the different audio features
    for all the tracks, to have one value each representing the entire album.

    Args:
        audio_features_df (DataFrame): Row-wise representation of relevant
            audio features, output of create_audio_features_df

    Returns:
        pd.Series: Mean of audio features for the entire album
    """

    album_features = audio_features.mean(axis=0)
    return album_features


def load_collection(collection_path, collection_cols, collection_genres=None):
    """Load the original collection file which lists all albums.

    Args:
        collection_path (str): Path pointing to the xlsx-file
        collection_cols (list): List of strings containing the column names to be
            included in the returned file
        collection_genres (list): If a list of genre strings is passed then the
            albums returned will be filtered accordingly (default=None)

    Returns:
        pd.DataFrame: DataFrame containing album information from collection file
    """

    collection = pd.read_excel(collection_path, encoding='utf-8')
    if collection_genres:
        collection = (collection[collection_cols].
                      loc[collection["Genre"].isin(collection_genres)])
    else:
        collection = collection[collection_cols]

    return collection


def create_albums_data(collection, feature_cols):
    """For every album in collection request the Spotify audio features (mean of the
    songs) and return them as new columns, added to the the original collection
    DataFrame.

    Args:
        collection (DataFrame): Collection DataFrame, output of
            'load collection' function
        feature_cols (list): List of strings containing the names of the audio
            features to be returned

    Returns:
       pd.DataFrame: Combination of the original collection DataFrame and the
       newly appended audio feature columns
    """

    data_list = []
    for album in album_df.itertuples():
        try:
            audio_features = go_now(album[1], album[2])
            data_list.append(audio_features)
        except IOError:
            print(f"{album[2]} not found on Spotify")
            data_list.append(pd.Series(np.zeros(len(df_cols))))

    data_df = pd.DataFrame(np.vstack(data_list), columns=df_cols)
    data_df = pd.concat([album_df.reset_index(drop=True), data_df], axis=1)
    
    return data_df



def go_now(artist_name, album_name):
    album_uri = get_album_uri(artist_name, album_name)
    tracklist = get_album_tracklist(album_uri)
    audio_features = get_audio_features(tracklist)
    album_features = calculate_mean_feature_values(audio_features)
    return album_features