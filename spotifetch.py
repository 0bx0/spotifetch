#!/usr/bin/env python3


#imports 
import os, sys, shutil, threading, webbrowser, requests, spotipy
from flask import Flask, request 
from pkce import generate_pkce_pair

# Stuff for spotipy i actually don't know what these do ;-;
CID = "58fe916446be4e289c9978b2c934567f"
redirect = 'http://127.0.0.1:8888/callback'

# Scope for the app
scopes = 'user-library-read user-top-read user-read-recently-played user-read-currently-playing'


# colors and the logo
GRAY = "\033[90m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"

logo = """⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃
⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀
⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀ """

# stuff for flask (zero idea what 'CODE' is)
app = Flask(__name__)
CODE = None

@app.route('/callback')
def spoti_return():
    global CODE
    CODE = request.args.get('code')
    return "Auth successful, you can return to the terminal now"

def run_flask():
    app.run(port=8888)

import json

TOKEN_CACHE_PATH = os.path.expanduser("~/.spotifetch/token.json")

def load_token():
    if os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH, "r") as f:
            return json.load(f)
    return None

def save_token(token_data):
    os.makedirs(os.path.dirname(TOKEN_CACHE_PATH), exist_ok=True)
    with open(TOKEN_CACHE_PATH, "w") as f:
        json.dump(token_data, f)

def refresh_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CID
    }
    res = requests.post("https://accounts.spotify.com/api/token", data=data)
    res.raise_for_status()
    token_data = res.json()
    token_data['refresh_token'] = token_data.get('refresh_token', refresh_token)
    save_token(token_data)
    return token_data['access_token']

def authenticate_user():
    # If cached token exists, use it
    token_data = load_token()
    if token_data:
        if 'refresh_token' in token_data:
            return refresh_access_token(token_data['refresh_token'])
        return token_data['access_token']

    # Else do full PKCE auth flow
    global CODE
    code_verifier, code_chall = generate_pkce_pair()

    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?client_id={CID}"
        f"&response_type=code"
        f"&redirect_uri={redirect}"
        f"&scope={scopes}"
        f"&code_challenge={code_chall}"
        f"&code_challenge_method=S256"
    )

    threading.Thread(target=run_flask, daemon=True).start()
    webbrowser.open(auth_url)

    while CODE is None:
        pass

    data = {
        'grant_type': 'authorization_code',
        'code': CODE,
        'redirect_uri': redirect,
        'client_id': CID,
        'code_verifier': code_verifier
    }

    res = requests.post("https://accounts.spotify.com/api/token", data=data)
    res.raise_for_status()
    token_data = res.json()
    save_token(token_data)
    return token_data['access_token']

# Scope for neccesary permissions 
scope = 'user-library-read ' \
'user-top-read ' \
'user-read-recently-played ' \
'user-read-currently-playing'

access_token = authenticate_user()
sp = spotipy.Spotify(auth=access_token)


# CMD Args handler
args = sys.argv[1:] 

# AI Generated cause I couldn't figure out how to do this
def display_neofetch_style(left_content, right_content):
    # Split logo into lines
    left_lines = left_content.split('\n')    

    for i in range(max(len(left_lines), len(right_content))):

        if i < len(left_lines): 
            left_line = f"{GREEN}{left_lines[i]}{RESET}"
        else:
            left_line = " " * max(len(line) for line in left_lines)
        if i < len(right_content):
            right_line = right_content[i]
        else:
            right_line = ""

        print(f"{left_line}    {right_line}")

# Fetching part of the code
def fetch_user_information():
    try:
        # Variable to store the user info
        user_information = sp.current_user()
        
        # user, id, followers
        username = user_information['display_name'] # Get username
        user_id = user_information['id']
        user_followers = user_information['followers']['total']

        # playlist information 
        user_playlists = sp.current_user_playlists() # Varaible for playlist entry
        playlist_count = user_playlists['total'] # Get total playlist count
        playlists = [playlist['name'] for playlist in user_playlists['items']] # foreach loop to get all the playlists of the user and store it as a list

        # display the song that's currently playing cause apparently people can't alt tab
        current_song = sp.current_user_playing_track() 
        current_track_name = "Nothing is playing" # default message 
        if current_song and current_song.get('item'):
            current_track_name = current_song['item']['name']
        
        # get number of liked songs
        liked_songs = sp.current_user_saved_tracks(limit=1)
        liked_songs_count = liked_songs['total']
        
        # get recently played tracks and extract artist names
        recently_played = sp.current_user_recently_played(limit=5)
        recent_artists = []

        for item in recently_played['items']:
            artist_names = [artist['name'] for artist in item['track']['artists']]
            for artist in artist_names:
                if artist not in recent_artists:
                    recent_artists.append(artist)
                if len(recent_artists) >= 5:  # Limit to 5 artists
                    break
            if len(recent_artists) >= 5:
                break
        
        # top artists 
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)
        top_artist_names = [artist['name'] for artist in top_artists['items']]

         # format the information to feed into display function
        line = []
        line.append(f"{BOLD}{BLUE}{username}@Spotify{RESET}")
        line.append(f"{BLUE}--------------------{RESET}")
        line.append(f"{BOLD}{BLUE}User:{RESET} {WHITE}{username} (ID: {user_id}){RESET}")
        line.append(f"{BOLD}{BLUE}Followers:{RESET} {WHITE}{user_followers}{RESET}")
        line.append(f"{BOLD}{BLUE}Playlists:{RESET} {WHITE}{playlist_count}{RESET}")
        line.append(f"{BOLD}{BLUE}Liked Songs:{RESET} {WHITE}{liked_songs_count}{RESET}")
        line.append(f"{BOLD}{BLUE}Listening To:{RESET} {WHITE}{current_track_name}{RESET}")
        
        # Display recent artists
        columns, rows = shutil.get_terminal_size()

        recent_artists_str = ", ".join(recent_artists[:5])
        line.append(f"{BOLD}{BLUE}Recently Played Artists:{RESET} {WHITE}{recent_artists_str[0:columns]}...{RESET}")
        
        # Display top artists
        top_artists_str = ", ".join(top_artist_names)
        line.append(f"{BOLD}{BLUE}Top Artists:{RESET} {WHITE}{top_artists_str}{RESET}")
        
        # Display the info next to the logo
        display_neofetch_style(logo, line)
        
        # Handle playlist display separately after the neofetch style display
        if playlist_count >= 4:
            print(f"\n{WHITE}Print all {len(playlists)} playlists?{RESET}")
            user_input = input(f"{BOLD}{BLUE}y/N:{RESET} ")
            if user_input.lower() == 'y':
                print(f"\n{BOLD}{BLUE}Playlists:{RESET}")
                for playlist in playlists:
                    print(f"{WHITE}- {playlist}{RESET}")
            else:
                return
        else:
            # If fewer than 4 playlists, just show them all
            print(f"\n{BOLD}{BLUE}Playlists:{RESET}")
            for playlist in playlists:
                print(f"{WHITE}- {playlist}{RESET}")
    
    except spotipy.SpotifyException as e:
        print(f"{BOLD}{RED}Error:{RESET} {WHITE}Failed to fetch Spotify data: {str(e)}{RESET}")
    except Exception as e:
        print(f"{BOLD}{RED}Error:{RESET} {WHITE}An unexpected error occurred: {str(e)}{RESET}")
        

def fetch_song_details(song_str):
    try:
        results = sp.search(q=song_str, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_artist = ', '.join([artist['name'] for artist in track['artists']])
            
            duration_ms = track['duration_ms']
            duration_min = duration_ms // 60000
            duration_sec = (duration_ms % 60000) // 1000
            duration = f"{duration_min}:{duration_sec:02d}"

            is_liked = sp.current_user_saved_tracks_contains([track['id']])
            track_album = track['album']['name']
            
            line = []
            line.append(f"{BOLD}{BLUE}Song Search:{RESET} {song_str} {RESET}- {track['id'] if track['id'] else ''}")
            line.append(f"{BLUE}--------------------{RESET}")
            
            line.append(f"{BOLD}{BLUE}Track:{RESET} {WHITE}{track_name}{RESET}")
            line.append(f"{BOLD}{BLUE}Artist(s):{RESET} {WHITE}{track_artist}{RESET}")
            line.append(f"{BOLD}{BLUE}Album:{RESET} {WHITE}{track_album}{RESET}")
            line.append(f"{BOLD}{BLUE}Liked:{RESET} {WHITE}{'yes' if is_liked[0] else 'no'}{RESET}")  
            line.append(f"{BOLD}{BLUE}Duration:{RESET} {WHITE}{duration}{RESET}")
            line.append(f"{BOLD}{BLUE}Release Date:{RESET} {WHITE}{track['album']['release_date']}{RESET}")   
            
            display_neofetch_style(logo, line)
            
        else:        
            line = []
            line.append(f"{BOLD}{BLUE}Song Search: {song_str}{RESET}")
            line.append(f"{BLUE}--------------------{RESET}")
            line.append(f"{WHITE}No result {RESET}")
            
            display_neofetch_style(logo, line)
    
    except spotipy.SpotifyException as e:
        print(f"{BOLD}{BLUE}ERROR {RESET} {WHITE}Spotifetch couldn't find: {str(e)}{RESET}")
    except Exception as e:
        print(f"{BOLD}{BLUE}ERROR {RESET} {WHITE}An unexpected error occurred: {str(e)}{RESET}")




if not args:
    fetch_user_information()
else:
    fetch_song_details(' '.join(args))


try:
    import subprocess
    subprocess.run(["deactivate"])

except Exception as e:
    pass