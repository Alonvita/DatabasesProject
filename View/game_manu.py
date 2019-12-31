from tkinter import *
from View import easy_game_page, challenging_game_page, hard_game_page


def game_menu_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='The memory game of a funny name', fg='black', font='Ariel 16 bold')
    name.grid(row=0, column=0, pady=(10, 10))

    bottonEasy = Button(frame, text='Easy Game', bg="blue", fg="white", font='Ariel 12 bold',
                        command=lambda: easy(window))
    bottonEasy.grid(row=1, column=0, pady=(10, 5))

    bottonHard = Button(frame, text='Hard Game', bg="blue", fg="white", font='Ariel 12 bold',
                        command=lambda: hard(window))
    bottonHard.grid(row=2, column=0, pady=(10, 5))

    bottonChallenging = Button(frame, text='Challenging Game', bg="blue", fg="white", font='Ariel 12 bold',
                        command=lambda: challenging(window))
    bottonChallenging.grid(row=3, column=0, pady=(10, 5))


def easy(window):
    easy_game_page.easy_game_window(window)


def hard(window):
    hard_game_page.hard_game_window(window)


def challenging(window):
    challenging_game_page.challenging_game_window(window)
