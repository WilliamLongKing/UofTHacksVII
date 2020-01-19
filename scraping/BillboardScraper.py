import sys
sys.path.append("..")
import requests
from bs4 import BeautifulSoup
import time
from backend.common.connect import Database
from SpotifySongInfo import spotify_info


#if year divisible by 4, it's a leap year -> feb + 1
DAYS_IN_MONTH =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEEK = 7

year = 2019
month = 1
day = 8

# {
#     JAN = 31
#     FEB = 28
#     MAR = 31
#     APR = 30
#     MAY = 31
#     JUN = 30
#     JUL = 31
#     AUG = 31
#     SEP = 30
#     OCT = 31
#     NOV = 30
#     DEC = 31
# }

Database.connect()

while year >= 2019:     #adjust this value to extend the history of data retrieval
    date = str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)
    URL = 'https://www.billboard.com/charts/hot-100/'+date 
    print(URL)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='chart-list container')
    #pdb.set_trace()
    chart_elems = results.find_all(class_='chart-list__element display--flex')

    for chart_elem in chart_elems:
        ranking = chart_elem.find('span', class_='chart-element__rank__number').text
        artist = chart_elem.find('span', class_='chart-element__information__artist text--truncate color--secondary').text
        song_title = chart_elem.find('span', class_='chart-element__information__song text--truncate color--primary').text

        # if ranking == '1' :
        print(ranking + ". " + song_title + " - " + artist)

        songID = Database.checkSongExists(song_title, artist)

        if songID == None:
            time.sleep(3)

            try:
                spotifyData = spotify_info(artist, song_title)

                songData ={
                    'danceability' : spotifyData["danceability"],           #how suitable for dancing the track is
                    'energy' : spotifyData["energy"],                       #measure of intensity and activity
                    'key' : spotifyData["key"],                             # overall key of the track
                    'loudness' : spotifyData["loudness"],                   # overall loudness in dB, typically from -60 to 0
                    'mode' : spotifyData["mode"],                           # major = 1, minor = 0
                    'speechiness' : spotifyData["speechiness"],             #presence of spoken words in a track
                    'acousticness' : spotifyData["acousticness"],           # confidence measure of whether track is acoustic
                    'instrumentalness' : spotifyData["instrumentalness"],   #predicts whether a trackc contains no vocals
                    'liveness' : spotifyData["liveness"],                   # detects presence of an audience in recording
                    'valence' : spotifyData["valence"],                     # musical positiveness conveyed (1.0 being highest)
                    'tempo' : spotifyData["tempo"],       
                    'time_signature' : spotifyData["time_signature"],
                    'duration' : spotifyData["duration_ms"],
                    'artist' : artist,
                    'ranking' : ranking,
                    'song_id' : spotifyData["id"], 
                    'song_title' : song_title
                }

                Database.addSongToTable(songData, date)
            except:
                try:
                    spotifyData = spotify_info(artist.split('Featuring', 1)[0].split('&', 1)[0], song_title)

                    songData ={
                        'danceability' : spotifyData["danceability"],           #how suitable for dancing the track is
                        'energy' : spotifyData["energy"],                       #measure of intensity and activity
                        'key' : spotifyData["key"],                             # overall key of the track
                        'loudness' : spotifyData["loudness"],                   # overall loudness in dB, typically from -60 to 0
                        'mode' : spotifyData["mode"],                           # major = 1, minor = 0
                        'speechiness' : spotifyData["speechiness"],             #presence of spoken words in a track
                        'acousticness' : spotifyData["acousticness"],           # confidence measure of whether track is acoustic
                        'instrumentalness' : spotifyData["instrumentalness"],   #predicts whether a trackc contains no vocals
                        'liveness' : spotifyData["liveness"],                   # detects presence of an audience in recording
                        'valence' : spotifyData["valence"],                     # musical positiveness conveyed (1.0 being highest)
                        'tempo' : spotifyData["tempo"],       
                        'time_signature' : spotifyData["time_signature"],
                        'duration' : spotifyData["duration_ms"],
                        'artist' : artist,
                        'ranking' : ranking,
                        'song_id' : spotifyData["id"], 
                        'song_title' : song_title
                    }

                    Database.addSongToTable(songData, date)
                except:
                    Database.rollback()
                    pass
        else:
            try:
                Database.addRanking(ranking, songID, date)
            except:
                Database.rollback()
                pass

    day -= WEEK
    if day < 1:
        month -= 1;
        if month < 1: 
            year -= 1
            month=12
        day = DAYS_IN_MONTH[month-1] + day
    #time.sleep(10)

        
