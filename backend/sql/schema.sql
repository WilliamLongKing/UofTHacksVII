CREATE SCHEMA myschema;

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

CREATE TABLE myschema.charts(
    spotifyID varchar(100),
    chartDate date,
    ranking int,
    PRIMARY KEY (spotifyID, chartDate),
    FOREIGN KEY (spotifyID) REFERENCES myschema.tracks(spotifyID)
);