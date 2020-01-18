import psycopg2

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
    SELECT spotifyID FROM myschema.charts
    WHERE title = %s
      AND artist = %s
'''

def connect():
    conn = None
    try:
        print "trying"
        conn = psycopg2.connect(database="songs", user = "postgres", password = "test", host = "35.225.65.195")
        print "success"
    except:
        print "failed"
    return conn

def checkSongExists(song_title, artist):
    conn = connect()
    cur = conn.cursor()

    cur.execute(CHECK_SONG_EXISTS, (song_title, artist))

    # returns the spotify ID if the song exists already, or a None type
    return cur.fetchone()

def addSongToTable(song):
    conn = connect()
    cur = conn.cursor()

    cur.execute(ADD_SONG, (song['song_id'], song['song_title'], song['artist']))
    cur.execute(UPDATE_SPOTIFY_SONG_INFO,
                (song['duration'], song['key'], song['mode'],
                 song['time_signature'], song['acousticness'], song['danceability'],
                 song['enenrgy'], song['instrumentalness'], song['liveness'],
                 song['loudness'], song['speechiness'], song['valence'],
                 song['tempo'], song['song_id']))
    cur.excute(ADD_SONG, (song['song_id'], song['chartDate'], song['ranking']))

    cur.commit()
    cur.close()
    conn.close()
