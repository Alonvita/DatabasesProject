from tkinter import *
from View import game_manu, leaderboard_page


def start_menu_window(window, Gamer_name, fileBackground2):
    for widget in window.winfo_children():
        widget.destroy()
    background_label = Label(window, image=fileBackground2)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="white")
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='The memory game of a funny name', fg='black', bg="white", font=("Comic Sans MS", 20))
    name.grid(row=0, column=0, pady=(10, 10))

    bottonEasy = Button(frame, text='Start Game', bg="#3abdef", width= 20, fg="white", font=("Comic Sans MS", 16),
                        command=lambda: start(window, Gamer_name, fileBackground2))
    bottonEasy.grid(row=1, column=0, pady=(10, 5))

    bottonHard = Button(frame, text='Leaderboard', bg="#3abdef", width= 20, fg="white", font=("Comic Sans MS", 16),
                        command=lambda: leaderboard(window, Gamer_name, fileBackground2))
    bottonHard.grid(row=2, column=0, pady=(10, 5))


def start(window, Gamer_name, fileBackground2):
    game_manu.game_menu_window(window, Gamer_name, fileBackground2)


def leaderboard(window, Gamer_name, fileBackground2):
    leaderboard_page.leaderboard_window(window, Gamer_name, fileBackground2)

