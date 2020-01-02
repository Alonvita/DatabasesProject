import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Aa123456",
    database="funny_name"
)
mycursor = mydb.cursor()


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