import mysql.connector
from sqlite3 import OperationalError

mydb = None
mycursor = None


def run():
    """
    RUN the SQL:
connect to server
    :return:
    """
    global mydb, mycursor
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Aa123456",
        allow_local_infile=True
        )
        mycursor = mydb.cursor()
        execute_scripts_from_file("../build_tables.sql")
    except mysql.connector.Error as err:
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
    :return:     if uer name od password are taken, return -1 else-return user id
    """
    cmd = "SELECT user_id FROM funny_name.users WHERE username = '"+user_name+"' AND password = '"+password+"';"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    return info[0][0]

def get_user_id_by_name(user_name):
    """
    check if user exist by user name only.
    to prevent two users with same name
    :param user_name:
    :param password:
    :return:     if uer name od password are taken, return -1 else-return user id
    """
    cmd = "SELECT user_id FROM funny_name.users WHERE username = '"+user_name+"';"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    return info[0][0]

def get_preferred_genres(user_id):
    """
    if there is  users ganres
    :param user_id:
    :return:
    """
    print(user_id)
    cmd = "SELECT preference  FROM funny_name.users_preferences WHERE user_id = "+str(user_id)+" AND type = 'genre';"
    genres = get_info_by_command(cmd)
    if len(genres)==0:
         return False
    return True


def add_preferences(user_id, genres_list):  # todo: change only to genre
    """
    Add prefered ganres of user
    :param user_id:
    :param genres_list:
    :return:
    """
    if len(genres_list) != 0:
        for pref in genres_list:
            insert_pref = """INSERT INTO funny_name.users_preferences(user_id,type,preference) VALUES(""" + str(
                user_id) + ",'" + "genre" + "','" + pref + "');"
            set_info_by_command(insert_pref)
            insert_artist_by_genre = """INSERT INTO users_preferences
                        SELECT distinct """ + str(user_id) + """, "artist",artist.name ,0
                        FROM artist JOIN artist_genres ON artist.id = artist_genres.artist_id
                        WHERE artist_genres.genre = '""" + pref + """'
                        AND artist.name NOT IN (SELECT preference  FROM funny_name.users_preferences WHERE user_id = """\
                        + str(user_id) + """)
                        LIMIT 4;
                        """
            set_info_by_command(insert_artist_by_genre)


def add_user(user_name, password1):
    """
    Add new user to DB
    :param user_name:
    :param password1:
    :return: -1 if username taken, else return the user id
    """
    user_name = str(user_name)
    password_d = str(password1)
    #check if user name taken
    user_id = get_user_id_by_name(user_name)
    if user_id is not -1:
        return -1

    if get_user_id(user_name,password_d) is not -1:
        return -1

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
    :return:     if uer name od password are taken, return -1 else-return user id
    """
    cmd = "SELECT user_id FROM funny_name.users WHERE username = '"+user_name+"' AND password = "+password+";"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    return info


def get_all_genres():
    """
    return list of possible genres.
    :return:
    """
    cmd = """
        SELECT name FROM (
        SELECT name, COUNT(*) as sum FROM funny_name.genres join
         artist_genres on artist_genres.genre = genres.name GROUP BY name ORDER BY sum DESC limit 50) AS aa;
         """
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    genres = [genre[0] for genre in info]
    return genres

"""artist data"""

def get_artist_info(artist_name):
    """
    get data about artist
    :param artist_name:
    :return:
    """
    command = "SELECT * FROM artist WHERE artist.name = " + "'" + artist_name + "';"
    artist_info = list(get_info_by_command(command)._getitem_(0))
    birth_date = str(artist_info[7])+"/"+str(artist_info[6])+"/"+str(artist_info[5])
    artist_data = list([artist_info[i] for i in range(1, 4)])
    artist_data.append(birth_date)
    return artist_data


def get_genre_by_artist(artist_name):
    """
    Get list of ganres
    :param artist_name:
    :return:  -1 if no genres, retruen list of genres
    """
    print(artist_name)
    command = """SELECT artist_genres.genre FROM artist JOIN artist_genres 
        ON artist_genres.artist_id = artist.id  
        WHERE artist.name = '""" + artist_name + "' GROUP BY artist_genres.genre;"""
    info = get_info_by_command(command)
    if len(info)==0:
        return -1
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
    :return: -1 if no songs, else return the list
    """
    command = """SELECT songs.name FROM artist JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = '""" + artist_name + """' GROUP BY songs.name limit 3;"""
    info = get_info_by_command(command)
    if len(info) is 0:
        return -1
    songs_list = [song[0] for song in info]
    print(songs_list[0])
    return songs_list


def get_preferred_artists(user_id):
    """
    return list of 4 artist with their data
    :param user_id:
    :return: -1 if there is a problem or list is empty.
    """
    cmd = "SELECT preference FROM funny_name.users_preferences WHERE users_preferences.count < 5 " \
          "AND users_preferences.user_id = " + str(user_id) + " AND users_preferences.type = 'artist' limit 4;"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    artists_names = [a[0] for a in info]
    artists_list = list()
    for a_n in artists_names:
        artist_info = list(get_artist_info(a_n))
        songs = list(get_songs(a_n))
        artist_info.append(songs)
        artists_list.append(artist_info)
    return artists_list


"""Ratings"""


def update_counter(user_name, password, artists_played):
    for a in artists_played:
        cmd = """UPDATE users_preferences
                SET users_preferences.count = CASE
                WHEN users_preferences.count IS NOT NULL THEN users_preferences.count + 1
                ELSE  users_preferences.count
                END
                WHERE user_id = """+get_user_id(user_name, password)+ " AND users_preferences.preference = "+a+";"
        get_info_by_command(cmd)


def add_game(typ, score, user_id):
    """
    update score to user
    :param typ:
    :param score:
    :param user_id:
    :return:
    """
    cmd = "UPDATE users SET users."+typ+" = CASE WHEN users." + typ + " IS NULL THEN " + str(score) + """
    WHEN users.first_game_points < 16 THEN 50 ELSE users.""" + typ + " END WHERE user_id = " + str(user_id) + ";"
    get_info_by_command(cmd)


def get_top_players(game_type):  # todo: parse info
    """
    return list of top players by type of the game
    :param game_type:
    :return: if no players, return -1
    """
    if game_type == "EASY":
        game_type = "first_game_points"
    elif game_type == "HARD":
        game_type = "second_game_points"
    else:
        game_type = "third_game_points"
    cmd = "SELECT username,first_game_points  FROM users ORDER BY users." + game_type + " DESC limit 3;"
    info = get_info_by_command(cmd)
    if len(info) == 0:
        return -1
    top = [p for p in info]
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