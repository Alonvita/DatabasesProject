import mysql.connector
from sqlite3 import OperationalError

mydb = None
mycursor = None


def run():
    global mydb, mycursor

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Aa123456",
        allow_local_infile=True
    )

    mycursor = mydb.cursor()


def execute_scripts_from_file(filename):
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
        except OperationalError as msg:
            print("Command skipped: " + msg)


def get_info_by_command(command_string):
    mycursor.execute(command_string)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult


def get_songs(artist_name):
    command = """SELECT songs.name 
    FROM artist 
    JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = '""" + artist_name + """'
    GROUP BY songs.name 
    limit 3;"""
    songs_list = [song[0] for song in get_info_by_command(command)]
    return songs_list


def get_genre_by_artist(artist_name):
    command = """SELECT artist_genres.genre FROM artist JOIN artist_genres 
        ON artist_genres.artist_id = artist.id  
        WHERE artist.name = '""" + artist_name + "' GROUP BY artist_genres.genre;"""
    return [g[0] for g in get_info_by_command(command)]


def get_preferred_artists(user_id):
    cmd = "SELECT preference FROM funny_name.users_preferences WHERE users_preferences.count < 5 " \
          "AND users_preferences.user_id = " + str(user_id) + " AND users_preferences.type = 'artist' limit 4;"
    artists_names = [a[0] for a in get_info_by_command(cmd)]
    artists_list = list()
    for a_n in artists_names:
        artists_list.append(get_artist_info(a_n))
    return artists_list


def get_preferred_genres(user_id):
    cmd = "SELECT preference  FROM funny_name.users_preferences WHERE user_id = "+str(user_id)+" AND type = 'genre';"
    genres = get_info_by_command(cmd)
    return genres


def get_artist_info(artist_name):
    command = "SELECT * FROM artist WHERE artist.name = " + "'" + artist_name + "'"
    artist_info = list(get_info_by_command(command).__getitem__(0))
    birth_date = str(artist_info[7])+"/"+str(artist_info[6])+"/"+str(artist_info[5])
    artist_data = list([artist_info[i] for i in range(1, 4)])
    artist_data.append(birth_date)
    return artist_data


def get_user_id(user_name):
    command = "SELECT user_id FROM funny_name.users WHERE username = '" + user_name + ";"
    return get_info_by_command(command)


def add_user(user_name, password):
    if get_user_id(user_name) is not None:
        return -1
    insert_user = """INSERT INTO users(username,password)
                    VALUES ( """ + user_name+", " + password + ");"
    get_info_by_command(insert_user)

    user_id = str(get_user_id(user_name))
    return user_id


def add_preferences(user_id, properties_list):
    if properties_list is not None and len(properties_list) != 0:
        for prop in properties_list:
            for pref in properties_list[prop]:
                insert_pref = """INSERT INTO users_preferences(""" + user_id + "," + prop + "," + pref+")"
                get_info_by_command(insert_pref)
                if prop is "Genre":
                    cmd = """INSERT INTO users_preferences
                        SELECT distinct""" + user_id + """, "artist",artist.name ,0
                        FROM artist JOIN artist_genres ON artist.id = artist_genres.artist_id
                        WHERE artist_genres.genre = """ + prop + """" 
                        AND artist.name NOT IN (SELECT preference  FROM funny_name.users_preferences WHERE user_id = """\
                        + user_id +""")
                        LIMIT 4;
                        """
                    get_info_by_command(cmd)


def confirm_user(user_name, password):
    cmd = "SELECT user_id FROM funny_name.users WHERE username = '"+user_name+"' AND password = "+password+";"
    user_id = get_info_by_command(cmd)
    if user_id is not None:
        return user_id
    return -1


def get_all_genres():
    cmd = """
        SELECT name FROM (
        SELECT name, COUNT(*) as sum FROM funny_name.genres join
         artist_genres on artist_genres.genre = genres.name GROUP BY name ORDER BY sum DESC limit 50) AS aa;
         """
    genres = [genre[0] for genre in get_info_by_command(cmd)]
    return genres


def update_counter(user_name, artists_played):
    for a in artists_played:
        cmd = """UPDATE users_preferences
                SET users_preferences.count = CASE
                WHEN users_preferences.count IS NOT NULL THEN users_preferences.count + 1
                ELSE  users_preferences.count
                END
                WHERE user_id = """ + get_user_id(user_name) + " AND users_preferences.preference = "+a+";"
        get_info_by_command(cmd)


def add_game(typ, score, user_id):
    cmd = "UPDATE users SET users."+typ+" = CASE WHEN users." + typ + " IS NULL THEN " + str(score) + """
    WHEN users.first_game_points < 16 THEN 50 ELSE users.""" + typ + " END WHERE user_id = " + str(user_id) + ";"
    get_info_by_command(cmd)


def get_top_players(game_type):  # todo: parse info
    cmd = "SELECT username,first_game_points  FROM users ORDER BY users." + game_type + " DESC limit 3;"
    top = get_info_by_command(cmd)
    return top


if __name__ == '__main__':
    run()
    execute_scripts_from_file("build_tables.sql")
    print(get_genre_by_artist("Adele"))

"""
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