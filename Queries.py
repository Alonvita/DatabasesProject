import mysql.connector
from sqlite3 import OperationalError

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



def get_artist(artist_name):
    command = "SELECT * FROM artist WHERE artist.name = " + "'" + artist_name + "'"
    return get_info_by_command(command)

def try_command():
    cmd = """SELECT songs.name 
    FROM artist 
    JOIN artist_to_credit ON artist_to_credit.artist = artist.id 
    JOIN songs ON songs.artist_credit = artist_to_credit.artist 
    WHERE artist.name = 'Adele' 
    GROUP BY songs.name 
    limit 3;"""
    return get_info_by_command(cmd)

def main():
    execute_scripts_from_file("build_tables.sql")
   # get_artist("Adele")
    res = try_command()
    print(res)


main()

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