import threading

from View.game_flow import getQueries, run

if __name__ == "__main__":
    # get the database in thread-conncect
    t = threading.Thread(target=getQueries)
    t.start()
    # run the game
    run()