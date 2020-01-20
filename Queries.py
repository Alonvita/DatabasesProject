import Conventions
import mysql.connector
from sqlite3 import OperationalError

from View.crash import crash_window

mydb = None
mycursor = None
settings_info = None
DEBUGGING = True
USE_MOCK_DB = True


def gat_configurations_from_file(file_name):
    """
    Read config from file
    :param file_name: filenme with path
    :return: dict
    """
    global settings_info
    settings_info = dict()
    f = open(file_name, "r")
    for line in f:
        info, value = line.split(":")
        settings_info[info] = value.replace("\n","")
    return settings_info


def insert_data():
    """
    Insert data to database from csv files.
    Check if database empty. if one sceme empty, insert for all
    :return:
    """
    cmd = """SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM albums)
            THEN "yes"
            WHEN  NOT EXISTS (SELECT 1 FROM albums_genres)
            THEN "yes"
            WHEN NOT EXISTS (SELECT 1 FROM artist)
            THEN "yes"
            WHEN  NOT EXISTS (SELECT 1 FROM artist_genres)
            THEN "yes"
            WHEN NOT EXISTS (SELECT 1 FROM artist_to_credit)
            THEN "yes"
            WHEN NOT EXISTS (SELECT 1 FROM genres)
            THEN "yes"
            WHEN NOT EXISTS (SELECT 1 FROM mediums)
            THEN "yes"
            WHEN NOT EXISTS (SELECT 1 FROM songs)
            THEN "yes"
            ELSE "no"
       END as checking
       """
    is_empty = get_info_by_command(cmd)
    if is_empty[0][0] == "yes":
        cmd =\
            """
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/ARTIST_TO_CREDIT.csv'   INTO TABLE artist_to_credit FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/ARTISTS.csv'  INTO TABLE artist FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/ARTISTS_GENRE.csv'  INTO TABLE artist_genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/GENRES.csv'  INTO TABLE genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/ALBUMS.csv'  INTO TABLE albums FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/ALBUMS_GENRE.csv'  INTO TABLE albums_genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/SONGS.csv'  INTO TABLE songs FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
                LOAD DATA LOCAL INFILE '../DB_FUNNY_NAME/CD_DATA.csv' INTO TABLE mediums FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
            """
        commands = cmd.split(";")
        #insert each csv data file into tables
        for command in commands:
            set_info_by_command(command)


def set_user_config(db_name, user_name):
    """
    Set database and provileges for user.
    :param db_name:  string got from file
    :param user_name: got from file
    """
    try:
        cmd = "GRANT ALL PRIVILEGES ON " + db_name + ".* TO '" + user_name + "'@'localhost' WITH GRANT OPTION;"
        mycursor.execute(cmd)
        cmd = "GRANT FILE ON *.* to '" + user_name + "'@'localhost';"
        mycursor.execute(cmd)
        cmd = "USE " + db_name + ";"
        mycursor.execute(cmd)
    except mysql.connector.Error as err:
        print("set_user_config:Command skipped: " + err.msg)


def run():
    """
    RUN the SQL:
connect to server
    :return:
    """
    global mydb, mycursor
    settings = gat_configurations_from_file("../ServerData.txt")
    try:
        print(settings)
        mydb = mysql.connector.connect(host=settings["ip"], user=settings["user_name"],
                                       password=settings["password"],
                                       port=settings["port"],
                                       allow_local_infile=True)
        print("run:connected")
        mycursor = mydb.cursor()
        # set username and database config
        set_user_config(settings["database"], settings["user_name"])
        execute_scripts_from_file("../build_tables.sql")
        insert_data();
    except mysql.connector.Error as err:
        crash_window()
        print("Something went wrong: {}".format(err))


def execute_scripts_from_file(filename):
    """
    Run sql commands from sql file.
    This commands create the DB
    """
    # Open and read the file as a single buffer
    fd = open(filename, 'r', encoding="utf-8")
    sql_file = fd.read()
    fd.close()

    # all SQL commands (split on ';')- no need for ";"
    sqlCommands = sql_file.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            mycursor.execute(command)
        except mysql.connector.Error as err:
            print(command)
            print(" execute_scripts_from_file:Command skipped: "+err.msg)


def get_info_by_command(command_string):
    """
    run sql command
    :param command_string:
    :return:
    """
    try:
     mycursor.execute(command_string)
     myresult = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("get_info_by_command:Something went wrong: {}"+err.msg)
    return myresult


def set_info_by_command(command_string):
    """
    run sql command for inser
    :param command_string:
    :return:
    """
    try:
     mycursor.execute(command_string)
     mydb.commit()
    except mysql.connector.Error as err:
        print("set_info_by_command:Something went wrong: {}"+err.msg)
    print(command_string)


def try_command():
    cmd = """SELECT songs.name 
    FROM artist 
    JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = 'Adele' 
    GROUP BY songs.name 
    limit 3;"""
    return get_info_by_command(cmd)


"""user data"""


def get_user_id(user_name, password):
    """
    check if user exist by user name and password.
    :param user_name:
    :param password:
    :return:  int   if uer name od password are taken, return Conventions.EMPTY_ANSWERS_LIST_CODE else-return user id-int
    """
    cmd = "SELECT user_id FROM " + settings_info["database"] + ".users WHERE username = '"+user_name+"' AND password = '"+password+"';"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return info[0][0]


def get_user_id_by_name(user_name):
    """
    check if user exist by user name only.
    to prevent two users with same name
    :param user_name:
    :param password:
    :return:     if uer name od password are taken, return Conventions.EMPTY_ANSWERS_LIST_CODE else-return user id
    """
    cmd = "SELECT user_id FROM " + settings_info["database"] + ".users WHERE username = '" + user_name + "';"
    info = get_info_by_command(cmd)

    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    return info[0][0]


def get_preferred_genres(user_id):
    """
    if there is  users ganres
    :param user_id:
    :return:
    # returns ['pop', 'classical', 'dance']
    """
    print(user_id)
    cmd = "SELECT preference  FROM " + settings_info["database"] + ".users_preferences WHERE user_id = "+str(user_id)+" AND type = 'genre';"
    genres = get_info_by_command(cmd)
    if len(genres)==0:
         return False
    return True


def get_similar_artist(artist_name):
    genres = get_genre_by_artist(artist_name)
    artists = list()
    for g in genres:
        cmd = "SELECT name FROM " + settings_info["database"] + \
              ".artist WHERE id IN " \
              "(SELECT artist_id FROM " + settings_info["database"] + ".artist_genres WHERE genre = '"+g+"') LIMIT 5;"
        artists.extend([artist_name[0] for artist_name in get_info_by_command(cmd)])
    return artists


def had_genre_preferred(user_id):
    """
        if there is  users genres
        :param user_id:
        :return:# returns True/False
        """
    cmd = "SELECT preference FROM " + settings_info["database"] + ".users_preferences WHERE user_id = " + str(
        user_id) + " AND type = 'genre';"
    genres = get_info_by_command(cmd)
    if len(genres) == 0:
        return False
    return True


def add_preferences(user_id, genres_list):  # todo: change only to genre
    """
    Add prefered ganres of user
    :param user_id:
    :param genres_list:
    :return
    """
    if len(genres_list) != 0:
        for pref in genres_list["Genre"]:
            insert_pref = """INSERT INTO """ + settings_info["database"] + """.users_preferences(user_id,type,preference) VALUES(""" + str(
                user_id) + ",'" + "genre" + "','" + pref + "');"
            set_info_by_command(insert_pref)
            insert_artist_by_genre = """INSERT INTO users_preferences
                        SELECT distinct """ + str(user_id) + """, "artist",artist.name ,0
                        FROM artist JOIN artist_genres ON artist.id = artist_genres.artist_id
                        WHERE artist_genres.genre = '""" + pref + """'
                        AND artist.name NOT IN (SELECT preference  FROM """ + settings_info["database"] + """.users_preferences WHERE user_id = """\
                        + str(user_id) + """
                        ORDER BY RAND())
                        LIMIT 4;
                        """
            set_info_by_command(insert_artist_by_genre)


def add_user(user_name, password1):
    """
    Add new user to DB
    :param user_name:
    :param password1:
    :return:# return int user_id or -1 if already exist
     -1 if username taken, else return the user id
    """
    user_name = str(user_name)
    password_d = str(password1)
    #check if user name taken
    user_id = get_user_id_by_name(user_name)
    if user_id is not -1:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    if get_user_id(user_name,password_d) is not -1:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    insert_user = """INSERT INTO users(username, password)
                    VALUES ( '""" + user_name+"', '" + password_d + "');"
    set_info_by_command(insert_user)
    user_id = str(get_user_id(user_name,password_d))
    return user_id


def confirm_user(user_name, password):
    """
    check if user exist by user name and password.
    :param user_name:
    :param password:
    :return:# return int user_id or -1 if don't exist
     if uer name od password are taken, return Conventions.EMPTY_ANSWERS_LIST_CODE else-return user id
    """
    cmd = "SELECT user_id FROM " + settings_info["database"] + ".users WHERE username = '"+user_name+"' AND password = "+password+";"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return info[0][0]


def get_all_genres():
    """
    return list of possible genres.
    :return:# returns list of genres ['genre1', 'genre2'...]
    """
    cmd = """
        SELECT name FROM (
        SELECT name, COUNT(*) as sum FROM """ + settings_info["database"] + """.genres join
         artist_genres on artist_genres.genre = genres.name GROUP BY name ORDER BY sum DESC limit 50) AS aa;
         """
    info = get_info_by_command(cmd)

    if len(info) == 0:
        print("Error: info length returned 0 at get_all_genres.\n\t{}".format(info))
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    genres = [genre[0] for genre in info]

    pre_dict= {}
    pre_dict["Genre"] = genres

    return pre_dict


# -------- artist data -------


def get_artist_info(artist_name):
    """
    get data about artist
    :param artist_name:
    :return:# returns list of artist info: ['artist1_name', 'artist1_gender', 'origin_country', 'day/month/year']
    """
    command = "SELECT DISTINCT * FROM artist WHERE artist.name = " + "'" + artist_name + "';"

    if DEBUGGING:
        print(command)
        print(get_info_by_command(command))

    artist_info = list(get_info_by_command(command)[0])

    if DEBUGGING:
        print(artist_info)
    birth_date = str(artist_info[7])+"/"+str(artist_info[6])+"/"+str(artist_info[5])
    artist_data = list([artist_info[i] for i in range(1, 4)])
    artist_data.append(birth_date)
    return artist_data


def get_genre_by_artist(artist_name):
    """
    Get list of ganres
    :param artist_name:
    :return:# returns list of genres: ['genre1',...]
  -1 if no genres, retruen list of genres
    """
    print(artist_name)
    command = """SELECT artist_genres.genre FROM artist JOIN artist_genres 
        ON artist_genres.artist_id = artist.id  
        WHERE artist.name = '""" + artist_name + "' GROUP BY artist_genres.genre;"""
    info = get_info_by_command(command)
    if len(info)==0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return [g[0] for g in info]


def get_artist(artist_name):
    command = "SELECT * FROM artist WHERE artist.name = " + "'" + artist_name + "'"
    artist_info = list(get_info_by_command(command)._getitem_(0))
    birth_date = str(artist_info[7])+"/"+str(artist_info[6])+"/"+str(artist_info[5])
    artist_data = list([artist_info[i] for i in range(1, 4)])
    artist_data.append(birth_date)
    return artist_data


def get_songs(artist_name):
    """
    get 3 songs of artist
    :param artist_name:
    :return:# returns list of songs: ['song1', 'song2',...]
                -1 if no songs, else return the list
    """
    if USE_MOCK_DB:
        return MOCK_SONGS_LIST

    command = """SELECT songs.name FROM artist JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = '""" + artist_name + """' GROUP BY songs.name limit 3;"""
    info = get_info_by_command(command)
    if len(info) is 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    songs_list = [song[0] for song in info]
    print(songs_list[0])
    return songs_list


def get_prefered_artist_easy(user_id):
    """
    Get 1 artist which
    :return:
    """
    cmd = """SELECT * FROM (SELECT preference FROM """ + settings_info["database"] + """.users_preferences WHERE 
            count = 0 AND user_id = """ + str(user_id) + """ AND type = 'artist' ORDER BY RAND() ASC limit 1) as t1
            UNION  
            SELECT* FROM( SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
            WHERE count < 5 AND user_id = """ + str(user_id) + """ AND type = 'artist' ORDER BY RAND() desc limit 4) as t2
            limit 4;
            """
    return cmd


def get_prefered_artist_hard(user_id):
    cmd = cmd = """SELECT * FROM (SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
                WHERE count > 0 AND user_id = """ + str(user_id) + \
                """ AND type = 'artist' ORDER BY count  ASC limit 1 ) as t1
                UNION  
                SELECT* FROM( SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
                    WHERE count < 5 AND user_id = """ + str(user_id) + \
                """ AND type = 'artist' ORDER BY count  desc limit 3) as t2
                UNION 
                SELECT * FROM (SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
                WHERE count < 5 AND user_id = """ + str(user_id) + """ AND type = 'artist' ORDER BY RAND()  ASC limit 4) as t3
                limit 4;
                """
    return cmd


def get_prefered_artist_challenging(user_id):
    cmd = """SELECT * FROM (SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
            WHERE count > 0 AND user_id = """+str(user_id)+""" AND type = 'artist' ORDER BY RAND()  ASC limit 5 ) as t1
            UNION  
            SELECT * FROM( SELECT preference FROM """ + settings_info["database"] + """.users_preferences 
            WHERE user_id = """+str(user_id)+""" AND type = 'artist' ORDER BY RAND() desc limit 5) as t2
            limit 5;
            """
    return cmd


def get_preferred_artists(user_id, game_type):
    """
    return list of 4 artist with their data
    :param user_id:
    :return: dictionary with key = 'Artist'
     { 'Artist': [
                  ['artist1_name', 'artist1_gender', 'origin_country', 'birth_date', [list of songs]],
                  ['artist2_name', 'artist2_gender', ....]
                 ]
     }
     -1 if there is a problem or list is empty.
    """
    if game_type == Conventions.EASY_GAME_CODE:
        cmd = get_prefered_artist_easy(user_id)
    elif game_type == Conventions.HARD_GAME_CODE:
        cmd = get_prefered_artist_hard(user_id)
    else:
        cmd = get_prefered_artist_challenging(user_id)
    info = get_info_by_command(cmd)

    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    artists_names = [a[0] for a in info]
    artists_list = list()

    for a_n in artists_names:
        artist_info = list(get_artist_info(a_n))
        songs = list(get_songs(a_n))
        artist_info.append(songs)
        artists_list.append(artist_info)
    preferred_artists = dict()
    preferred_artists.__setitem__("Artist", artists_list)

    print("List created: {}".format(preferred_artists))
    return preferred_artists


"""old version 
    cmd = "SELECT preference FROM " + settings_info["database"] + ".users_preferences WHERE users_preferences.count < 5 " \
          "AND users_preferences.user_id = " + str(user_id) + " AND users_preferences.type = 'artist' limit 4;"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    artists_names = [a[0] for a in info]
    artists_list = list()
    for a_n in artists_names:
        artist_info = list(get_artist_info(a_n))
        songs = list(get_songs(a_n))
        artist_info.append(songs)
        artists_list.append(artist_info)
    return artists_list

"""

# -------- RATINGS --------


def update_counter(user_name, artists_played):  # TODO: artist is a list - each entry has a name
    for a in artists_played:
        cmd = """UPDATE users_preferences
                SET users_preferences.count = CASE
                WHEN users_preferences.count IS NOT NULL THEN users_preferences.count + 1
                ELSE  users_preferences.count
                END
                WHERE user_id = """ +\
              str(get_user_id_by_name(user_name)) + " AND users_preferences.preference = '" + a + "';"
        set_info_by_command(cmd)


def add_game(typ, score, user_id):
    """
    update score to user
    :param typ:
    :param score:
    :param user_id:
    :return:
    """
    if typ == Conventions.EASY_GAME_CODE:
        typ = "first_game_points"
    elif typ == Conventions.HARD_GAME_CODE:
        typ = "second_game_points"
    else:
        typ = "third_game_points"

    cmd = "UPDATE users "\
        "SET " + settings_info["database"] + ".users." + typ + " = CASE "\
        "WHEN " + settings_info["database"] + ".users." + typ + " IS NULL THEN " + str(score) +\
        " WHEN " + settings_info["database"] + ".users." + typ + " < " + str(score) + " THEN " + str(score) + " "\
        "ELSE  " + settings_info["database"] + ".users." + typ +\
        " END "\
        "WHERE user_id = " + str(user_id) + ";"
    set_info_by_command(cmd)


def get_top_players(game_type):
    """
    return list of top players by type of the game
    :param game_type:
    :return:# return list of players: ['user1', 'user2']
  if no players, return Conventions.EMPTY_ANSWERS_LIST_CODE
    """
    if game_type == Conventions.EASY_GAME_CODE:
        game_type = "first_game_points"
    elif game_type == Conventions.HARD_GAME_CODE:
        game_type = "second_game_point"
    else:
        game_type = "third_game_points"
    cmd = "SELECT username,"+ game_type +\
          " FROM " + settings_info["database"] +".users ORDER BY users." + game_type + " DESC limit 3;"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    top = [[p[0], p[1]] for p in info]
    return top


"""

if __name__ == '__main__':
    run()
    execute_scripts_from_file("build_tables.sql")
    print(get_genre_by_artist("Adele"))
List of commands:
get artist_songs: (adele songs limit list to 3 - no duplicated song names)
    SELECT songs.name 
    FROM artist 
    JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = 'Adele' 
    GROUP BY songs.name 
    limit 3;

"""

MOCK_SONGS_LIST = ['test1', 'test2', 'test3']
MOCK_SONGS_LIST_WITH_NONE_VALS = ['test1', 'test2', None]
