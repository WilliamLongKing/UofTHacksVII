import requests

SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search'
SPOTIFY_SONG_FEATURES_URL = 'https://api.spotify.com/v1/audio-features/'
HEADER = {"Authorization" : "Bearer BQAOirxJpMBTNTAKQOHjUBLaYae4B7_g4CR5gNAo8pLt60Mp8ZTMCXvbaLqSYa8uqz111m7Gc7bNL_TpWC3rboi1sZqTgFqFeaRAPvYMwJFnc7XnsuhkfxpkzuOONK1jNoSLnlMlORY"}

def spotify_info(artist, song):
    # song = song.replace(' ', '%20')
    # artist = artist.replace(' ', '%20')
    query = 'track:'+song+' artist:'+artist
    PARAMS = {'q' : query, 'type':'track'}

    r = requests.get(url=SPOTIFY_SEARCH_URL, params=PARAMS, headers=HEADER)
    data = r.json()

    print(data)

    song_id = data["tracks"]["items"][0]["id"]
    print(song_id)
    r = requests.get(url=SPOTIFY_SONG_FEATURES_URL+song_id, headers=HEADER)
    data = r.json()

    

    return(data)

    # danceability = data["danceability"] #how suitable for dancing the track is
    # energy = data["energy"] #measure of intensity and activity
    # key = data["key"]       # overall key of the track
    # loudness = data["loudness"] # overall loudness in dB, typically from -60 to 0
    # mode = data["mode"]     # major = 1, minor = 0
    # speechiness = data["speechiness"]   #presence of spoken words in a track
    # acousticness = data["acousticness"] # confidence measure of whether track is acoustic
    # instrumentalness = data["instrumentalness"] #predicts whether a trackc contains no vocals
    # liveness = data["liveness"] # detects presence of an audience in recording
    # valence = data["valence"]   # musical positiveness conveyed (1.0 being highest)
    # tempo = data["tempo"]       
    # time_signature = data["time_signature"]
    # duration = data["duration_ms"]

# spotify_info("mac miller", "hurt feelings")