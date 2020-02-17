import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import pandas as pd

# Import credentials and instantiate client with authorization
SPOTIPY_CLIENT_ID = credentials.client_id
SPOTIPY_CLIENT_SECRET = credentials.client_secret

ccm = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                               client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=ccm)

album_name = "Nexus of Teeth"
artist_name = "Hyperdontia"


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
        album_uri (string): Album URI

    Returns:
        list: list of track URI
    """
    tracklist = []
    album = sp.album(album_uri)
    for track in album['tracks']['items']:
        tracklist.append(track['uri'])
    return tracklist


def get_audio_features(tracklist):
    """Get a list of audio analyses for the tracks in the tracklist.
    Each analysis is a dict containing audio features and other information
    about the individual tracks.

    Documentation here:
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/

    Args:
        tracklist (list): Comma-separated list of track URI

    Returns:
        list of dictionaries: Audio-analysis dictionaries for the tracks
    """
    audio_features = sp.audio_features(tracklist)
    return audio_features


def build_audio_feature_df(audio_features):
    """Build a DataFrame containing the relevant features from the
    audio analyis. Tracks are represented row-wise.

    Args:
        audio_features (list): List of dictionaries

    Returns:
        DataFrame: Row-wise representation of relevant audio features.
    """
    audio_features_df = pd.DataFrame(audio_features)
    audio_features_df.drop(['speechiness',
                            'acousticness',
                            'liveness',
                            'type',
                            'id',
                            'uri',
                            'track_href',
                            'analysis_url',
                            'time_signature',
                            ],
                           axis=1,
                           inplace=True
                           )
    return audio_features_df


def calculate_mean_values(audio_features_df):
    """Calculate the mean of the track feature values for the entire album.

    Args:
        audio_features_df (DataFrame): Rowwise representation of relevant audio features

    Returns:
        pd.Series: Mean of audio features for the entire album
    """
    album_features = audio_features_df.mean(axis=0)
    return album_features


def go_now(artist_name, album_name):
    album_uri = get_album_uri(artist_name, album_name)
    tracklist = get_album_tracklist(album_uri)
    audio_features = get_audio_features(tracklist)
    audio_features_df = build_audio_feature_df(audio_features)
    album_features = calculate_mean_values(audio_features_df)
    print(audio_features_df)
    print(album_features)


go_now(artist_name, album_name)
