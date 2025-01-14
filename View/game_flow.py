import threading
from tkinter import *
from tkinter.ttk import Progressbar

import Queries
from View import login_page

serverRun = 0


# function that get progress bar and play it
def bar(progress, frame):
    global serverRun
    import time
    i = 0
    flag = 0
    # while the progress bar need to work
    while True:
        if serverRun == 0:
            progress['value'] = i
            if i < 100 and flag == 0:
                i += 20
            else:
                flag = 1
                i -= 20
            if i == 0:
                flag = 0
            frame.update()
            time.sleep(1)
        else:
            break

# the main function- run the game
def run():
    # initialize window
    window = Tk()
    window.title("The memory game of a funny name")
    window.geometry("800x600")
    window.minsize(width=800, height=600)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)

    backgroundName = sys.path[0] + '\\View\\background.png'

    fileBackground = PhotoImage(file=backgroundName)

    backgroundName2 = sys.path[0] + '\\View\\bg2.png'
    fileBackground2 = PhotoImage(file=backgroundName2)

    # initialize frame
    frame = Frame(window)
    frame.grid(row=1, column=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    message1 = Label(frame, text='Please Wait...', fg='black', font='Ariel 16 bold')
    message1.grid(row=0, column=0, pady=(5, 5))
    progress = Progressbar(frame, orient=HORIZONTAL, length=100, mode='indeterminate')
    progress.grid(row=1, column=0, pady=(5, 5))
    bar(progress, frame)  # start progress bar

    # login page- the first page that the user see
    login_page.login_window(window, fileBackground, fileBackground2)
    window.mainloop()


# get the database
def getQueries():
    global serverRun
    Queries.run()
    serverRun = 1
