import os
import random
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy

def get_playlist(clientID, clientSECRET, emotion):
    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    """
    Input an emotion and the Spotify API will output a random public playlist accordingly
    """
    emotions = {'neutral' : ['neutral', 'popular', 'hits', 'dance', 'hot', 'top'],
                'joy' : ['happiness', 'happy', 'cheerful', 'summer', 'upbeat', 'party'],
                'anger' : ['angry', 'anger', 'rage', 'upset'],
                'sorrow' : ['sad', 'sadness', 'emo', 'winter'],
                'surprise' : ['shock', 'surprise'],
                'fear' : ['calm', 'calming', 'relax']}

    keyword = random.choice(emotions[emotion])
    random_int = random.randint(0, 75)
    playlist_list = sp.search(keyword, limit=10, offset=random_int, type='playlist', market='US')['playlists']['items']

    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']