from tkinter import *
from View import easy_game_page, challenging_game_page, hard_game_page
from View import start_menu


def game_menu_window(window, Gamer_name, fileBackground2):
    for widget in window.winfo_children():
        widget.destroy()
    background_label = Label(window, image=fileBackground2)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="white")
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='The memory game of a funny name', bg="white", fg='black', font=("Comic Sans MS", 20))
    name.grid(row=0, column=0, pady=(10, 10))

    bottonEasy = Button(frame, text='Easy Game', bg="#3abdef", width= 20, fg="white", font=("Comic Sans MS", 16),
                        command=lambda: easy(window, Gamer_name, fileBackground2))
    bottonEasy.grid(row=1, column=0, pady=(10, 5))

    bottonHard = Button(frame, text='Hard Game', bg="#3abdef", width= 20, fg="white", font=("Comic Sans MS", 16),
                        command=lambda: hard(window, Gamer_name, fileBackground2))
    bottonHard.grid(row=2, column=0, pady=(10, 5))

    bottonChallenging = Button(frame, text='Challenging Game', width= 20, bg="#3abdef", fg="white", font=("Comic Sans MS", 16),
                        command=lambda: challenging(window, Gamer_name, fileBackground2))
    bottonChallenging.grid(row=3, column=0, pady=(10, 5))

    bottonEasy = Button(frame, text='Go back', bg="#10c716", width= 20, fg="white", font=("Comic Sans MS", 16),
                        command=lambda: start(window, Gamer_name, fileBackground2))
    bottonEasy.grid(row=4, column=0, pady=(5, 5))


def start(window, Gamer_name, fileBackground2):
    start_menu.start_menu_window(window, Gamer_name, fileBackground2)


def easy(window, Gamer_name, fileBackground2):
    easy_game_page.easy_game_window(window, Gamer_name, fileBackground2)


def hard(window, Gamer_name, fileBackground2):
    hard_game_page.hard_game_window(window, Gamer_name, fileBackground2)


def challenging(window, Gamer_name, fileBackground2):
    challenging_game_page.challenging_game_window(window, Gamer_name, fileBackground2)
