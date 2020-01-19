import psycopg2
import pyrebase
import sys
import firebase_admin
from firebase_admin import credentials
import csv

ADD_SONG = '''
    INSERT INTO myschema.tracks(spotifyID, title, artist)
    VALUES
        (%s, %s, %s)
'''

ADD_RANKING = '''
    INSERT INTO myschema.charts(spotifyID, chartDate, ranking)
    VALUES
        (%s, %s, %s)
'''

UPDATE_SPOTIFY_SONG_INFO = '''
    UPDATE myschema.tracks
    SET durationMs = %s,
        songKey = %s,
        mode = %s,
        timeSignature = %s,
        acousticness = %s,
        danceability = %s,
        energy = %s,
        instrumentalness = %s,
        liveness = %s,
        loudness = %s,
        speechiness = %s,
        valence = %s,
        tempo = %s
    WHERE spotifyID = %s
'''

CHECK_SONG_EXISTS = '''
    SELECT spotifyID FROM myschema.tracks
    WHERE title = %s
      AND artist = %s
'''

SELECT_SONGS_IN_DATE_RANGE = '''
    SELECT DISTINCT ON (tracks.spotifyID, charts.chartDate)
           tracks.title, tracks.artist, tracks.energy, tracks.loudness, 
           tracks.valence, tracks.tempo, chart.ranking, chart.chartDate
      FROM myschema.tracks as tracks
      JOIN myschema.charts as charts
        ON charts.spotifyID = tracks.spotifyID
    WHERE charts.chartDate <= to_date(%s,'YYYY-MM-DD')
      AND charts.chartDate >= to_date(%s,'YYYY-MM-DD')
    ORDER BY charts.chartDate ASC;
'''

CREATE_SCHEMA = 'CREATE SCHEMA myschema'

CREATE_SONG_TABLE = '''
    CREATE TABLE myschema.tracks(
        spotifyID varchar(100) PRIMARY KEY,
        title varchar(100),
        artist varchar(100),
        durationMs int,
        songKey int,
        mode int,
        timeSignature int,
        acousticness float,
        danceability float,
        energy float,
        instrumentalness float,
        liveness float,
        loudness float,
        speechiness float,
        valence float,
        tempo float
    );
'''

CREATE_RANKING_TABLE = '''
    CREATE TABLE myschema.charts(
        spotifyID varchar(100),
        chartDate date,
        ranking int,
        PRIMARY KEY (spotifyID, chartDate),
        FOREIGN KEY (spotifyID) REFERENCES myschema.tracks(spotifyID)
    );
'''

DELETE_SONG = '''
    DELETE FROM myschema.tracks
    WHERE  spotifyID = \'06AKEBrKUckW0KREUWRnvT\'
'''

DELETE_DUPLICATES = '''
DELETE FROM myschema.charts WHERE spotifyID NOT IN 
(SELECT spotifyID FROM (
    SELECT DISTINCT ON (spotifyID) *
  FROM myschema.charts) as id);
DELETE FROM myschema.tracks WHERE spotifyID NOT IN 
(SELECT spotifyID FROM (
    SELECT DISTINCT ON (spotifyID) *
  FROM myschema.tracks) as id);
'''

class Database:
    # config = {
    #     "apiKey": "AIzaSyA2rO0ev8ZqLxoBmJ8uHiiquOAoMKZVTLo",
    #     "authDomain": "uofthacks7-45645.firebaseapp.com",
    #     "databaseURL": "https://uofthacks7-45645.firebaseio.com",
    #     "storageBucket": "uofthacks7-45645.appspot.com",
    #     "serviceAccount": "../../../uofthacks7-45645-firebase-adminsdk-5ix0d-cc96b3db0a.json"
    # }

    DB_CONNECTION = None

    @staticmethod
    def connect():
        try:
            print("trying")
            Database.DB_CONNECTION = psycopg2.connect(database="songs", user = "postgres", password = "test", host = "35.225.65.195")
            print("success")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    @staticmethod
    def cleanup():
        Database.DB_CONNECTION.close()

    @staticmethod
    def rollback():
        Database.DB_CONNECTION.rollback()

    @staticmethod
    def makeTable():
        cur = Database.DB_CONNECTION.cursor()
        # cur.execute(CREATE_SCHEMA)
        # Database.DB_CONNECTION.commit()
        cur.execute(CREATE_RANKING_TABLE)

        Database.DB_CONNECTION.commit()
    
    @staticmethod
    def deleteSong():
        cur = Database.DB_CONNECTION.cursor()
        cur.execute(DELETE_SONG)
        Database.DB_CONNECTION.commit()


    @staticmethod
    def checkSongExists(song_title, artist):
        cur = Database.DB_CONNECTION.cursor()
        cur.execute(CHECK_SONG_EXISTS, (str(song_title), str(artist)))

        result = cur.fetchone()
        cur.close()

        # returns the spotify ID if the song exists already, or a None type
        print(result)
        return result

    @staticmethod
    def addSongToTable(song, date):
        cur = Database.DB_CONNECTION.cursor()

        cur.execute(ADD_SONG, (song['song_id'], song['song_title'], song['artist']))
        Database.DB_CONNECTION.commit()
        cur.execute(UPDATE_SPOTIFY_SONG_INFO,
                    (song['duration'], song['key'], song['mode'],
                    song['time_signature'], song['acousticness'], song['danceability'],
                    song['energy'], song['instrumentalness'], song['liveness'],
                    song['loudness'], song['speechiness'], song['valence'],
                    song['tempo'], song['song_id']))

        Database.DB_CONNECTION.commit()
        cur.close()
        Database.addRanking(song['ranking'], song['song_id'], date)

    @staticmethod
    def selectSongsInDateRange(startDate, endDate):
        cur = Database.DB_CONNECTION.cursor()

        cur.execute(SELECT_SONGS_IN_DATE_RANGE, (endDate, startDate))
        
        result = cur.fetchall()
        cur.close()

        #writes data to a csv file
        with open('output.csv','w') as out:
            wr=csv.writer(out)
            wr.writerow(["spotifyID", 
                        "title",
                        "artist",
                        "durationMs",
                        "songKey",
                        "mode" ,
                        "timeSignature",
                        "acousticness",
                        "danceability",
                        "energy",
                        "instrumentalness",
                        "liveness",
                        "loudness",
                        "speechiness",
                        "valence",
                        "tempo",
                        "spotifyID",
                        "chart date",
                        "ranking"])
            for row in result:
                wr.writerow(row)
            # wr.writerows(result)

        return result

    @staticmethod
    def addRanking(ranking, songID, date):
        cur = Database.DB_CONNECTION.cursor()

        cur.execute(ADD_RANKING, (songID, date, ranking))
        Database.DB_CONNECTION.commit()

        cur.close()
    
    @staticmethod
    def deleteDuplicates():
        cur = Database.DB_CONNECTION.cursor()

        cur.execute(DELETE_DUPLICATES)
        Database.DB_CONNECTION.commit()

        cur.close()

# Database.connect()
# Database.selectSongsInDateRange("2018-01-01", "2019-11-25")
# Database.makeTable()

# Database.addSongToTable({
#                 'danceability' : 0.735,           #how suitable for dancing the track is
#                 'energy' : 0.578,                       #measure of intensity and activity
#                 'key' : 3,                             # overall key of the track
#                 'loudness' : -11.84,                   # overall loudness in dB, typically from -60 to 0
#                 'mode' : 1,                           # major = 1, minor = 0
#                 'speechiness' : 0.0461,             #presence of spoken words in a track
#                 'acousticness' : 0.514,           # confidence measure of whether track is acoustic
#                 'instrumentalness' : 0.0902,   #predicts whether a trackc contains no vocals
#                 'liveness' : 0.01,                   # detects presence of an audience in recording
#                 'valence' : 0.636,                     # musical positiveness conveyed (1.0 being highest)
#                 'tempo' : 160,       
#                 'time_signature' : 4,
#                 'duration' : 12332,
#                 'artist' : "Ke$ha",
#                 'ranking' : 1,
#                 'song_id' : "06AKEBrKUckW0KREUWRnvT", 
#                 'song_title' : "TiK ToK"
#             })

# Database.deleteSong()

# Database.checkSongExists("TiK ToK", "Ke$ha")