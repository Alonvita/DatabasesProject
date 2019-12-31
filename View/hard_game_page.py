from tkinter import *


def hard_game_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='hard manu', fg='black', font='Ariel 16 bold')
    name.grid(row=0, columnspan=2, pady=(10, 10))
