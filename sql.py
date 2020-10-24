# SQL queries for data modeling of the starshema
# DROP TBALES
songplay__Drop = "DROP TABLE IF EXISTS songplayed" #  FACT TABLE
users__Drop = "DROP TABLE IF EXISTS users"
songs__Drop = "DROP TABLE IF EXISTS songs"
artists__Drop = "DROP TABLE IF EXISTS artists"
time__Drop = "DROP TABLE IF EXISTS time"


# CREATE THE FACT TABLE IN POSTGRESQL
#------------------------------- songplay table or fact table ---------------------------
songplay__create = ("""CREATE TABLE IF NOT EXISTS songplayed(
                       songplay_id SERIAL CONSTRAINT songplay_PK PRIMARY KEY, 
                       start_time TIMESTAMP REFERENCES time (start_time),
                       user_id INT REFERENCES users (user_id),
                       level VARCHAR NOT NULL,
                       song_id VARCHAR REFERENCES songs (song_id),
                       artist_id VARCHAR REFERENCES artists (artist_id),
                       session_id INT NOT NULL,
                       location VARCHAR,
                       user_agent TEXT
        
)""")  
#------------------------------- song table---------------------------------------------
# CONSTRAINT ALLOW YOU TO DEFINE CONSTRAINTS ON COLUMN AND TABLE
# references keyword if only indicate a foreign key    
# text datatype can store unlimited string but varchar(n) not and in that case postgres will cut the strings in n before insrting it in the table       

songs__create  = (""" CREATE TABLE IF NOT EXISTS songs(
                      song_id VARCHAR CONSTRAINT song_PK PRIMARY KEY,
                      title VARCHAR,
                      artist_id VARCHAR REFERENCES artists (artist_id),
                      year INT CHECK (year >= 0),
                      duration FLOAT
        )""")
#-------------------------------- user table ------------------------------------------

users__create = ("""CREATE TABLE IF NOT EXISTS users(
                    user_id INT CONSTRAINT user_PK PRIMARY KEY,
                    first_name VARCHAR,
                    last_name VARCHAR,
                    gender CHAR(1),
                    level VARCHAR NOT NULL
                    
        )""")

#-------------------------------- artist table --------------------------------------
artists__create = ("""CREATE TABLE IF NOT EXISTS artists(
                      artist_id VARCHAR CONSTRAINT artist_PK PRIMARY KEY,
                      name VARCHAR,
                      location VARCHAR,
                      latitude DECIMAL(9,6),
                      longitude DECIMAL(9,6) 
)""")
#-------------------------------- time table ----------------------------------------
time__create = (""" CREATE TABLE IF NOT EXISTS time(
                    start_time TIMESTAMP CONSTRAINT time_PK PRIMARY KEY,
                    hour INT NOT NULL CHECK (year >=0),
                    day INT NOT NULL CHECK (day >=0),
                    week INT NOT NULL CHECK (week >= 0),
	                 month INT NOT NULL CHECK (month >= 0),
	                 year INT NOT NULL CHECK (year >= 0),
	                 weekday VARCHAR NOT NULL
        )""")
song__select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# insert the data into the created tables above
songplayed__insert = ("""INSERT INTO songplayed VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s )
""")

users__insert  = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) 
                     ON CONFLICT (user_id) DO UPDATE SET 
                     level = EXCLUDED.level 
""")
# on conflict is just doing some update of the acual informatin
songs__insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) 
                    ON CONFLICT (song_id) DO NOTHING                        
""")

artists__insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) 
                      ON CONFLICT (artist_id) DO UPDATE SET
                      location = EXCLUDED.location,
                      latitude = EXCLUDED.latitude,
                      longitude = EXCLUDED.longitude
""")
time__insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO NOTHING
""")

song_select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# QUERY LISTS

create__queries = [users__create, artists__create, songs__create, time__create, songplay__create]
drop__queries = [songplay__Drop, users__Drop, songs__Drop, artists__Drop, time__Drop]