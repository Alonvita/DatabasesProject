from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview

from View import start_menu


def leaderboard_window(window, Gamer_name):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='Leaderboard', fg='black', font='Ariel 16 bold')
    name.grid(row=0, column=0, pady=(10, 10))

    leaderboard={
        "EASY": [['Player name', 'score'], ['baba', 100], ['gaga', 98], ['jaja', 90]],
        "HARD": [['Player name', 'score'], ['nana', 100], ['mama', 96], ['haha', 95]],
        "CHALLENGING": [['Player name', 'score'], ['lala', 99], ['tata', 95], ['rara', 90]]
    }

    i = 1
    for key in leaderboard.keys():
        i += 1
        name1 = Label(frame, text=key, fg='black', font='Ariel 10 bold')
        name1.grid(row=i, column=0, pady=(5, 5))
        tv = Treeview(frame, height=len(leaderboard[key])-1)
        tv['columns'] = (leaderboard[key][0][1])
        tv.heading("#0", text=leaderboard[key][0][0])
        tv.column("#0", anchor="center", width=100)
        tv.heading(leaderboard[key][0][1], text=leaderboard[key][0][1])
        tv.column(leaderboard[key][0][1], anchor='center', width=100)
        tv.grid(sticky=(N, S))
        treeview = tv
        for j in range(len(leaderboard[key])-1):
            j += 1
            treeview.insert('', 'end', text=leaderboard[key][j][0], values=(leaderboard[key][j][1]))
        i += 1
        treeview.grid(row=i, column=0, pady=(10, 10))

    bottonEasy = Button(frame, text='Go back', bg="green", fg="white", font='Ariel 12 bold',
                        command=lambda: start(window, Gamer_name))
    bottonEasy.grid(row=i+1, column=0, pady=(5, 5))


def start(window, Gamer_name):
    start_menu.start_menu_window(window, Gamer_name)

