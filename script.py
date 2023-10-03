import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

spotipy_client_id = "2a3ad103fcbb4e209b2ab646db90bc83"
spotipy_client_secret = "ada1bf16b531442bb7ef3e11c17cca6d"

with open("songs.txt", "r") as file:
    lines = file.readlines()

playlist_name = input("What do you want to name your playlist?")


spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotipy_client_id,
                                               client_secret=spotipy_client_secret,
                                               redirect_uri='http://localhost:8000/callback',
                                               scope="user-library-read user-top-read playlist-modify-private"))

def get_track_id(name, artist=None):
    search = name
    if artist:
        search += f" artist:{artist}"

    result = spotify.search(q=search, type="track", limit=1)
    if result['tracks']['items']:
        return result['tracks']['items'][0]['uri']
    return None

def get_artist(track_id):
    track_info = spotify.track(track_id)
    artists = [artist['name'] for artist in track_info['artists']]
    return artists

def create_playlist(name):
    user_id = spotify.me()['id']
    playlist = spotify.user_playlist_create(user_id, name, public=False)
    return playlist

playlist = create_playlist(playlist_name)

track_id = []
for line in lines:
    line = line.strip()
    id = ""
    if "-" in line:
        name, artist = line.split("-")
        id = get_track_id(name, artist)
        track_id.append(id)
    else:
        id = get_track_id(line)
        track_id.append(id)

    if id:
        song_artist = get_artist(id)
   

print(track_id)
spotify.playlist_add_items(playlist_id=playlist['id'], items=track_id, position=None)
