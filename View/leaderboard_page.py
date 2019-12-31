from tkinter import *
from View import start_menu


def leaderboard_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='Leaderboard', fg='black', font='Ariel 16 bold')
    name.grid(row=0, column=0, pady=(10, 10))

    bottonEasy = Button(frame, text='Go back', bg="blue", fg="white", font='Ariel 12 bold',
                        command=lambda: start(window))
    bottonEasy.grid(row=1, column=0, pady=(10, 5))


def start(window):
    start_menu.start_menu_window(window)

