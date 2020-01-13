
 BEGIN;

CREATE USER IF NOT EXISTS 'funny_name'@'localhost' IDENTIFIED BY 'funny_name';
CREATE DATABASE IF NOT EXISTS funny_name;
GRANT ALL PRIVILEGES ON funny_name.* TO 'funny_name'@'localhost' WITH GRANT OPTION;
GRANT FILE ON *.* to 'funny_name'@'localhost';
USE funny_name;
SET GLOBAL local_infile = ON;
CREATE TABLE IF NOT EXISTS albums ( -- replicate
    id                      BIGINT UNSIGNED, -- PK
    name                    VARCHAR(255),
    artist_credit           INTEGER,
    platform                VARCHAR(64) NOT NULL,
    type                VARCHAR(255) NOT NULL,
    first_release_date_year   SMALLINT
) CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE IF NOT EXISTS artist_to_credit ( -- replicate (verbose)
    artist              INTEGER NOT NULL, -- references
    artist_credit       INTEGER NOT NULL -- PK
) CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE IF NOT EXISTS artist ( -- replicate (verbose)
    id                  BIGINT UNSIGNED,
    name                VARCHAR(255) NOT NULL,
	gender              VARCHAR(255) NOT NULL,
    area                VARCHAR(255) NOT NULL,
    type                VARCHAR(255) NOT NULL,
    begin_date_year     SMALLINT,
    begin_date_month    SMALLINT,
    begin_date_day      SMALLINT
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS songs ( -- replicate (verbose)
    id                  BIGINT UNSIGNED, -- PK 
    name                VARCHAR(255) NOT NULL,
    artist_credit       INTEGER NOT NULL, 
    medium              INTEGER NOT NULL 
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS genres ( -- replicate (verbose)
    name                VARCHAR(255) NOT NULL
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS albums_genres ( -- replicate (verbose)
    album_id       INTEGER,
    genre          VARCHAR(255) NOT NULL
) CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE IF NOT EXISTS artist_genres ( -- replicate (verbose)
    artist_id                  BIGINT UNSIGNED,
    genre              		   VARCHAR(255) NOT NULL,
	count         			   INTEGER 
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS mediums ( -- replicate (verbose)
    id                  BIGINT UNSIGNED,
    `release`               INTEGER NOT NULL,
    format               VARCHAR(255) NOT NULL,
    artist_credit		 INTEGER NOT NULL,
    release_group		INTEGER NOT NULL,
    language			 VARCHAR(255) NOT NULL
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS users ( -- replicate (verbose)
    user_id                   INT NOT NULL AUTO_INCREMENT,
    username              		   VARCHAR(255) NOT NULL,
	password         			   VARCHAR(255) NOT NULL ,
    first_game_points					INT,
    second_game_point					INT,
    third_game_points					INT,
	PRIMARY KEY (user_id)
) CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS users_preferences ( -- replicate (verbose)
    user_id                  INT,
	type  					 VARCHAR(255) NOT NULL,
    preference               VARCHAR(255) NOT NULL,
    count                    INT
) CHARACTER SET utf8 COLLATE utf8_general_ci;


LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\ARTIST_TO_CREDIT.csv' IGNORE  INTO TABLE artist_to_credit FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\ARTISTS.csv' INTO TABLE artist FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\CD_DATA.csv' INTO TABLE mediums FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\ARTISTS_GENRE.csv' INTO TABLE artist_genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\GENRES.csv' INTO TABLE genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\ALBUMS.csv' INTO TABLE albums FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\ALBUMS_GENRE.csv' INTO TABLE albums_genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE '.\\DB_FUNNY_NAME\\SONGS.csv' INTO TABLE songs FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

COMMIT;

-- vi: set ts=4 sw=4 et :