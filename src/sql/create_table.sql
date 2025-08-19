DROP TABLE IF EXISTS de_2506_a.ruben_capstone;

CREATE TABLE de_2506_a.ruben_capstone (
    id VARCHAR(1000) PRIMARY KEY,
    name VARCHAR(1000) NOT NULL,
    album VARCHAR(1000) NOT NULL,
    album_id VARCHAR(1000) NOT NULL,
    artists VARCHAR(1000) NOT NULL,
    artist_ids VARCHAR(1000),
    track_number INT,
    disc_number INT,
    explicit BOOLEAN,
    danceability DECIMAL,
    energy DECIMAL,
    key INT,
    loudness DECIMAL,
    mode INT,
    speechiness DECIMAL,
    acousticness DECIMAL,
    instrumentalness DECIMAL,
    liveness DECIMAL,
    valence DECIMAL,
    tempo DECIMAL,
    duration_ms INT,
    time_signature INT,
    year INT,
    release_date DATE
);