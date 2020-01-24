# QUERIES
import random
import Conventions
import mysql.connector
from Server import Server

mydb = None
mycursor = None
settings_info = None
DEBUGGING = False
USE_MOCK_DB = False
CHOOSE_RANDOM_SONGS_LIST = False
DEBUGGING_EMPTY_SONGS_LIST = False

sql_server = Server()


def run():
    """
    RUN the SQL:
    connect to server
    If connection failed return error
    """
    status = None
    message = None
    try:
        sql_server.connect()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


"""user data"""


def get_user_id(user_name, password):
    """
    Check if user exist by user name and password.
    :param user_name: str
    :param password: str of integers
    :return:int: if user name and password are taken - return Conventions.EMPTY_ANSWERS_LIST_CODE
                else-return user id
    """
    cmd = "SELECT user_id FROM " + sql_server.settings_info["database"] +\
          ".users WHERE username = '"+user_name+"' AND password = '"+password+"';"
    info = sql_server.get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return info[0][0]


def get_user_id_by_name(user_name):
    """
    Check if user exist by user name only.
    to prevent two users with same name
    :param user_name: str
    :param password: str of integers
    :return: if user name is taken - return Conventions.EMPTY_ANSWERS_LIST_CODE else-return user id
    """
    cmd = "SELECT user_id FROM " + sql_server.settings_info["database"] + ".users WHERE username = '" + user_name + "';"
    info = sql_server.get_info_by_command(cmd)

    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    return info[0][0]


def get_preferred_genres(user_id):
    """
    If there are preferred genres chosen by user
    :param user_id: int
    :return: True if user has preferred genres, else False
    """
    cmd = "SELECT preference  FROM " + sql_server.settings_info["database"] + \
          ".users_preferences WHERE user_id = "+str(user_id)+" AND type = 'genre';"
    genres = sql_server.get_info_by_command(cmd)
    if len(genres) == 0:
        return False
    return True


def get_user_genres(user_id):
    """
    Get user preferred genres
    :param user_id: int
    :return:list of genres chosen by user. example: ['pop', 'classical', 'dance']
            if list is empty return Conventions.EMPTY_ANSWERS_LIST_CODE
    """
    cmd = "SELECT preference  FROM " + sql_server.settings_info["database"] +\
          ".users_preferences WHERE user_id = "+str(user_id)+" AND type = 'genre';"
    genres = sql_server.get_info_by_command(cmd)
    if len(genres) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return [genre[0] for genre in genres]


def get_similar_and_different_artists_list(artist_name):
    """
    Get list of artists names which first artist in list is  in same genre
    of artist and the rest are not from same genre
    :param artist_name: str
    :return: list of artist one from the same genre and the rest aren't
    """
    genres = get_genre_by_artist(artist_name)
    artists = list()
    for g in genres:
        cmd = "SELECT name FROM "+sql_server.settings_info["database"] + \
              ".artist WHERE id IN " \
              "(SELECT artist_id FROM "+sql_server.settings_info["database"]+".artist_genres WHERE genre = '"+g+"');"
        artists.extend([artist_name for artist_name in sql_server.get_info_by_command(cmd)])
    return artists


def add_preferences(user_id, preference_dict):
    """
    Add preferred genres and artist of user to DB. Artists are chosen automatically from genre user chose.
    first command add genres to DB, second command add 4 artist from each preferred genre.
    :param user_id: int
    :param preference_dict: dict {'Genre': [list of genres preferred on user]}
    """
    if len(preference_dict) != 0:
        for pref in preference_dict["Genre"]:
            insert_pref = """INSERT INTO """ + sql_server.settings_info["database"] + \
                        """.users_preferences(user_id,type,preference) VALUES(""" + str(user_id) +\
                        ",'" + "genre" + "','" + pref + "');"
            sql_server.set_info_by_command(insert_pref)
            insert_artist_by_genre = """INSERT INTO users_preferences
                        SELECT distinct """ + str(user_id) + """, "artist",artist.name ,0
                        FROM artist JOIN artist_genres ON artist.id = artist_genres.artist_id
                        WHERE artist_genres.genre = '""" + pref + """'
                        AND artist.name NOT IN (SELECT preference 
                        FROM """ + sql_server.settings_info["database"] + """.users_preferences 
                        WHERE user_id = """\
                        + str(user_id) + """
                        ORDER BY RAND())
                        LIMIT 4;
                        """
            sql_server.set_info_by_command(insert_artist_by_genre)


def add_user(user_name, password1):
    """
    Add new user to DB - check if user_name is not taken and user isn't already exist
    :param user_name: int
    :param password1: int
    :return: int Conventions.EMPTY_ANSWERS_LIST_CODE if username taken or exist already, else return the user id
    """
    user_name = str(user_name)
    password_d = str(password1)
    # check if user name taken
    user_id = get_user_id_by_name(user_name)
    if user_id != -1:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    # check if user already exist
    if get_user_id(user_name,password_d) != -1:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    insert_user = """INSERT INTO users(username, password)
                    VALUES ( '""" + user_name+"', '" + password_d + "');"
    sql_server.set_info_by_command(insert_user)
    user_id = str(get_user_id(user_name,password_d))
    return user_id


def get_all_genres():
    """
    Get list of possible genres.
    :return: list of genres ['genre1', 'genre2'...] or Conventions.EMPTY_ANSWERS_LIST_CODE if there are no genres
    """
    cmd = """
        SELECT name FROM (
        SELECT name, COUNT(*) as sum FROM """ + sql_server.settings_info["database"] + """.genres join
         artist_genres on artist_genres.genre = genres.name GROUP BY name ORDER BY sum DESC limit 50) AS aa;
         """
    info = sql_server.get_info_by_command(cmd)

    if len(info) == 0:
        print("Error: info length returned 0 at get_all_genres.\n\t{}".format(info))
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    genres = [genre[0] for genre in info]

    pre_dict = dict()
    pre_dict["Genre"] = genres

    return pre_dict


# -------- artist data -------


def get_artist_info(artist_name):
    """
    Get data about artist
    :param artist_name: str
    :return:list of artist info: ['artist1_name', 'artist1_gender', 'origin_country', 'day/month/year']
    """
    command = "SELECT DISTINCT * FROM artist WHERE artist.name = " + "'" + artist_name + "';"

    if DEBUGGING:
        print(command)
        print(sql_server.get_info_by_command(command))

    artist_info = list(sql_server.get_info_by_command(command)[0])

    if DEBUGGING:
        print(artist_info)
    birth_date = str(artist_info[7])+"/"+str(artist_info[6])+"/"+str(artist_info[5])
    artist_data = list([artist_info[i] for i in range(1, 4)])
    artist_data.append(birth_date)
    return artist_data


def get_genre_by_artist(artist_name):
    """
    Get list of genres artist preforms
    :param artist_name: str
    :return:list of genres: ['genre1',...]
            Conventions.EMPTY_ANSWERS_LIST_CODE if artist has no genres
    """
    command = """SELECT artist_genres.genre FROM artist JOIN artist_genres 
        ON artist_genres.artist_id = artist.id  
        WHERE artist.name = '""" + artist_name + "' GROUP BY artist_genres.genre;"""
    info = sql_server.get_info_by_command(command)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    return [g[0] for g in info]


def get_songs(artist_name):
    """
    Get a list with 3 songs of artist
    :param artist_name: str
    :return:list of songs: ['song1', 'song2',...]
            Conventions.EMPTY_ANSWERS_LIST_CODE if no songs
    """
    if USE_MOCK_DB:
        if CHOOSE_RANDOM_SONGS_LIST:
            return MOCK_SONGS_LIST_LIST[random.randint(Conventions.ZERO, len(MOCK_SONGS_LIST_LIST) - 1)]
        else:
            return MOCK_SONGS_LIST_1 if not DEBUGGING_EMPTY_SONGS_LIST else MOCK_FOR_EMPTY_SONGS_LIST

    command = """SELECT songs.name FROM artist JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = '""" + artist_name + """' GROUP BY songs.name limit 3;"""
    info = sql_server.get_info_by_command(command)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    songs_list = [song[0] for song in info]
    return songs_list


def get_preferred_artist_easy(user_id):
    cmd = """SELECT * FROM (SELECT preference FROM """ + sql_server.settings_info["database"] +\
          """.users_preferences WHERE count = 0 AND user_id = """ + str(user_id) + \
          """ AND type = 'artist' ORDER BY RAND() ASC limit 1) as t1
            UNION  
            SELECT* FROM( SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
            WHERE count < 5 AND user_id = """ + str(user_id) + """ AND type = 'artist' ORDER BY RAND() desc limit 4) as t2
            limit 4;
            """
    return cmd


def get_preferred_artist_hard(user_id):
    cmd = """SELECT * FROM (SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
                WHERE count > 0 AND user_id = """ + str(user_id) + \
                """ AND type = 'artist' ORDER BY count  ASC limit 1) as t1
                UNION  
                SELECT* FROM (SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
                    WHERE count < 5 AND user_id = """ + str(user_id) + \
                """ AND type = 'artist' ORDER BY count  desc limit 3) as t2
                UNION 
                SELECT * FROM (SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
                WHERE count < 5 AND user_id = """ + str(user_id) + """ AND type = 'artist' ORDER BY RAND()
                 ASC limit 4) as t3
                limit 4;
                """
    return cmd


def get_preferred_artist_challenging(user_id):
    cmd = """SELECT * FROM (SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
            WHERE count > 0 AND user_id = """+str(user_id)+""" AND type = 'artist' ORDER BY RAND()  ASC limit 5 ) as t1
            UNION  
            SELECT * FROM( SELECT preference FROM """ + sql_server.settings_info["database"] + """.users_preferences 
            WHERE user_id = """+str(user_id)+""" AND type = 'artist' ORDER BY RAND() desc limit 5) as t2
            limit 5;
            """
    return cmd


def get_preferred_artists(user_id, game_type):
    """
    recursive functions return list of 4 artist with their data (if list of artists is not full call it again)
    :param user_id:
    :return: dictionary with key = 'Artist' and value for that key is list with names off artists. example:
     { 'Artist': [
                  ['artist1_name', 'artist1_gender', 'origin_country', 'birth_date', [list of songs]],
                  ['artist2_name', 'artist2_gender', ....]
                 ]
     }
     Conventions.EMPTY_ANSWERS_LIST_CODE if there is a problem or list is empty.
    """
    if game_type == Conventions.EASY_GAME_CODE:
        cmd = get_preferred_artist_easy(user_id)
    elif game_type == Conventions.HARD_GAME_CODE:
        cmd = get_preferred_artist_hard(user_id)
    else:
        cmd = get_preferred_artist_challenging(user_id)
    info = sql_server.get_info_by_command(cmd)

    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE

    artists_names = [a[0] for a in info]
    artists_list = list()

    for a_n in artists_names:
        artist_info = list(get_artist_info(a_n))
        songs_ = get_songs(a_n)
        if songs_ != Conventions.EMPTY_ANSWERS_LIST_CODE:
            songs = list(songs_)
            artist_info.append(songs)
        artists_list.append(artist_info)

    # if their is less artist then needed, add more artist to user study and make query again
    if (len(artists_list) < 5 and game_type == Conventions.CHALLENGING_GAME_CODE) or (len(artists_list) < 4):
        add_preferences(user_id, {"Genre": get_user_genres(user_id)})
        return get_preferred_artists(user_id, game_type)

    preferred_artists = dict()
    preferred_artists.__setitem__("Artist", artists_list)

    update_counter(user_id,artists_names,game_type)
    if DEBUGGING:
        print("List created: {}".format(preferred_artists))
    return preferred_artists

# -------- RATINGS --------


def update_counter(user_id, artists_played,game_type):
    """
    Update counter of artists in DB. Used when user is questioned about artists in list
    :param user_id: int
    :param artists_played: list of artists names
    :param game_type: str
    """
    if game_type != Conventions.CHALLENGING_GAME_CODE:
        cmd = """UPDATE users_preferences
                SET users_preferences.count = CASE
                WHEN users_preferences.count IS NOT NULL THEN users_preferences.count + 1
                ELSE users_preferences.count
                END
                WHERE user_id = """ +\
              str(user_id) + " AND users_preferences.preference = '" + artists_played[0] + "';"
        sql_server.set_info_by_command(cmd)
    else:
        for artist in artists_played:
            cmd = """UPDATE users_preferences
                   SET users_preferences.count = CASE
                   WHEN users_preferences.count IS NOT NULL THEN users_preferences.count + 1
                   ELSE  users_preferences.count
                   END
                   WHERE user_id = """ + \
                  str(user_id) + " AND users_preferences.preference = '" + artist + "';"
            sql_server.set_info_by_command(cmd)


def add_game(typ, score, user_id):
    """
    Update score to user if score in current game is higher than user score recorded.
    :param typ: str - type of game played
    :param score: int
    :param user_id: int
    """
    # change typ to string represent DB column of game type
    if typ == Conventions.EASY_GAME_CODE:
        typ = "first_game_points"
    elif typ == Conventions.HARD_GAME_CODE:
        typ = "second_game_point"
    else:
        typ = "third_game_points"

    cmd = "UPDATE users "\
        "SET " + sql_server.settings_info["database"] + ".users." + typ + " = CASE "\
        "WHEN " + sql_server.settings_info["database"] + ".users." + typ + " IS NULL THEN " + str(score) +\
        " WHEN " + sql_server.settings_info["database"] + ".users." + typ + " < " + str(score) + " THEN " + str(score) + " "\
        "ELSE  " + sql_server.settings_info["database"] + ".users." + typ +\
        " END "\
        "WHERE user_id = " + str(user_id) + ";"
    sql_server.set_info_by_command(cmd)


def get_top_players(game_type):
    """
    return list of top players by type of the game given
    :param game_type: str
    :return:list of top players and score in same type.
            example: [['user1','score'], ['user2','score'],['user3','score']]
            if no players, return Conventions.EMPTY_ANSWERS_LIST_CODE
    """
    # change typ to string represent DB column of game type
    if game_type == Conventions.EASY_GAME_CODE:
        game_type = "first_game_points"
    elif game_type == Conventions.HARD_GAME_CODE:
        game_type = "second_game_point"
    else:
        game_type = "third_game_points"
    cmd = "SELECT username,"+ game_type +\
          " FROM " + sql_server.settings_info["database"] +\
          ".users WHERE " + game_type+" is not null ORDER BY users." + game_type + " DESC limit 3;"
    info = sql_server.get_info_by_command(cmd)
    if len(info) == 0:
        return Conventions.EMPTY_ANSWERS_LIST_CODE
    top = [[p[0], p[1]] for p in info]
    return top

#-------- TESTING ------------
MOCK_SONGS_LIST_1 = ['test1', 'test2', 'test3']
MOCK_FOR_EMPTY_SONGS_LIST = []
MOCK_SONGS_LIST_3 = ['test4', 'test5']
MOCK_SONGS_LIST_WITH_NONE_VALS = ['test1', 'test2', None]

MOCK_SONGS_LIST_LIST = [
    MOCK_SONGS_LIST_1,
    MOCK_SONGS_LIST_3
]
