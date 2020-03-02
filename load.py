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


def _get_album_uri(artist_name, album_name):
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


def _get_album_tracklist(album_uri):
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


def _get_audio_features(tracklist, feature_list):
    """Get a list of audio analyses for the tracks in the tracklist.
    Each analysis is a dict containing audio features and other information
    about the individual tracks.

    Documentation here:
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/

    Args:
        tracklist (list): List of track URI strings, output of
            get_album_tracklist function
        feature_list (list): List of strings containing the audio feature
            names to be returned (passed from create_album_data function)

    Returns:
        pd.DataFrame: Row-wise representation of relevant audio features
            for every song in the album
    """

    audio_features_list_of_dicts = sp.audio_features(tracklist)
    audio_features = pd.DataFrame(audio_features_list_of_dicts)
    audio_features = audio_features[feature_list]

    return audio_features


def _drop_outliers_IQR_method(df, drop_outliers=True, IQR_dist=1.5, threshold=2):
    """Drop songs with an outlier count that reaches the defined threshold.
    All numeric columns (--> audio features) are checked, NaN values are ignored.
    This step is optional and can be disabled.

    Args:
        df (pd.DataFrame): Audio features for the different songs, output of
            get_audio_features function.
        drop_oultiers (bool, optional): Controls if outlier removal is applied
            or not. Enables or disables this function. Defaults to True.
        IQR_dist (float, optional): Definition of cut-off distance from quartiles
            that defines outliers. Defaults to 1.5.
        threshold (int, optional): Songs with equal or more outlier values will
            be dropped. Defaults to 2.

    Returns:
        pd.DataFrame: Audio features dataframe with "outlier songs" removed.
    """
    if drop_outliers:
        outlier_cols = list(df.select_dtypes(include=["float64", "int64"]).columns)
        other_cols = [x for x in df.columns if x not in outlier_cols]
        temp_df = df[other_cols].copy()

        for col in outlier_cols:
            q25, q75 = np.nanpercentile(df[col], 25), np.nanpercentile(df[col], 75)
            iqr = q75 - q25
            # calculate the outlier cut-off
            cut_off = iqr * IQR_dist
            lower, upper = q25 - cut_off, q75 + cut_off
            # identify outliers
            outliers = (df[col] < lower) | (df[col] > upper)
            outliers = pd.DataFrame(outliers, columns=[col])
            temp_df = pd.concat([temp_df, outliers], axis=1, sort=False)

        df["sum"] = temp_df.sum(axis=1)
        df_red = df.loc[df["sum"] < threshold].copy()
        df_red.drop(["sum"], inplace=True, axis=1)

        return df_red
    else:
        return df


def _calculate_mean_feature_values(audio_features):
    """Calculate and return the mean values of the different audio features
    for all the tracks, to have one value each representing the entire album.

    Args:
        audio_features_df (DataFrame): Row-wise representation of relevant
            audio features, output of drop_outliers function

    Returns:
        pd.Series: Mean of audio features for the entire album
    """

    album_features = audio_features.mean(axis=0)

    return album_features


def go_and_request(artist_name, album_name, feature_list, args_outliers):
    """Combine all the different functions and request the audio
    features for an album from the Spotify API, calculate and
    return the mean values.

    Args:
        artist_name (str): Name of the artist
        album_name (str): Name of the album
        feature_list (list): List of strings containing the names
            of the audio features to be returned, passed from
            create_album_data function

    Returns:
        pd.Series: Mean of audio features for the entire album
    """
    album_uri = _get_album_uri(artist_name, album_name)
    tracklist = _get_album_tracklist(album_uri)
    audio_features = _get_audio_features(tracklist, feature_list)
    audio_features_red = _drop_outliers_IQR_method(audio_features, *args_outliers)
    album_features = _calculate_mean_feature_values(audio_features_red)

    return album_features


def load_collection(collection_path, collection_cols, collection_genres=None):
    """Load the original collection file which lists all albums.

    Args:
        collection_path (str): Path pointing to the xlsx-file
        collection_cols (list): List of strings containing the column names to be
            included in the returned file, first two have to be "Artist" and "Album"
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

    assert (collection.columns[0] == "Artist") & (collection.columns[1] == "Album"), \
        "The 1st and 2nd columns of the DataFrame must be 'Artist' and 'Album'."

    return collection


def create_albums_data(collection, feature_list, args_outliers):
    """Combine loading and requesting functions: For every album in the
    collection data request the Spotify audio features per song, calculate their
    mean values (optionally removing the outliers) and add these features as new
    columns to the the original collection DataFrame.

    Args:
        collection (DataFrame): Collection DataFrame, output of
            'load collection' function
        feature_list (list): List of strings containing the names of the audio
            features to be returned, filters the relevant ones

    Returns:
       pd.DataFrame: Combination of the original collection DataFrame and the
       newly appended audio feature columns
    """

    data_list = []
    for album in collection.itertuples():
        try:
            audio_features = go_and_request(album[1],
                                            album[2],
                                            feature_list,
                                            args_outliers)
            data_list.append(audio_features)
        except IndexError:
            print(f"{album[1]} - {album[2]} NOT FOUND on Spotify")
            data_list.append(pd.Series(np.zeros(len(feature_list))))

    data_df = pd.DataFrame(np.vstack(data_list), columns=feature_list)
    data_df = pd.concat([collection.reset_index(drop=True), data_df], axis=1)

    return data_df
