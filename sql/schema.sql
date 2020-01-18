CREATE SCHEMA myschema;
GO

CREATE TABLE myschema.tracks(
    spotifyID varchar(100) NOT NULL PRIMARY KEY,
    title varchar(100),
    author varchar(100),
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
GO

CREATE TABLE myschema.charts(
    spotifyID varchar(100) NOT NULL FOREIGN KEY,
    chartDate varchar(10),
    ranking int,
    primary key (spotifyID, chartDate)
);
GO