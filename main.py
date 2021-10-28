import requests
import sys
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
from bs4 import BeautifulSoup
from secrets import *


opt = ["yes", "y"]
scope = 'playlist-modify-public'
token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager = token)

def main():
    print("Starting...")
    fetch_songs()


def fetch_songs(): 
    url = input("Enter playlist: ")
    a = requests.get(url)
    soup = BeautifulSoup(a.text, features="html.parser")
    print("--------------------")
    print("FETCHING SONGS")
    print("--------------------")

    try:
        songs = soup.findAll('div', {'class':'songs-list-row__song-name'})

        song = [song.get_text() for song in songs if song]
        count = 0

        #printing out into a text file named "playlist.txt"
        original_stdout = sys.stdout
        with open('playlist.txt', 'w') as f:
            sys.stdout = f
            for idx in range(len(song)):
                print(f'{song[idx]}')
                count += 1 
            sys.stdout = original_stdout
        print("Songs collected")
        print("Songs in playlist:", count)

        one_request(count)
    except:
        print("Something went wrong fetching songs")




def one_request(count):
    option = input("Do you want to customise your playlist? (y/n): ")

    if option.lower() in opt:
        name = input("Playlist name: ")
        desc = input("Playlist description: ")
    
    else:
        name = "Converted playlist"
        desc = "Playlist converted from Apple Music"
        
    spotifyObject.user_playlist_create(user=username,name=name,public=True,description=desc)
    
    print(" ")
    print("'"+name+ "'" + " created")
    print(" ")


    list_of_songs = []
    problems = []
    added = 0
    
    with open("playlist.txt", "r") as f:
        for item in f:
            try:
                result = spotifyObject.search(q=item)
                list_of_songs.append(result['tracks']['items'][0]['uri'])
                added += 1
                print(added,"."," Added", item)
            except:
                print("Couldn't add", item)
                problems.append(item)


    if problems:
        print("The following songs could not be added: ")
        for i in problems:
            print(i)

    print("Successfully added",added,"out of",count)
    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']

    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)


main()
