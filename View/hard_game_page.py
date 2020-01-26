import threading
from random import randint
from tkinter import *
from tkinter.ttk import Progressbar

from View import start_menu
from Logic import GameLogic as gL
import Conventions

GameInfoDict = ""


# function that get progress bar and play it
def bar(progress, frame):
    global GameInfoDict
    import time
    i = 0
    flag = 0
    while True:
        if GameInfoDict == "":
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


# get game
def getGameInfoDict(Gamer_name):
    global GameInfoDict
    GameInfoDict = gL.start(Gamer_name.get(), Conventions.HARD_GAME_CODE)


# hard game
def hard_game_window(window, Gamer_name, fileBackground2):
    # destroy the old widgets
    global GameInfoDict
    for widget in window.winfo_children():
        widget.destroy()
    background_label = Label(window, image=fileBackground2)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="white")
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # get game in thread
    t = threading.Thread(target=getGameInfoDict, args=(Gamer_name,))
    t.start()

    message1 = Label(frame, text='You will see facts about an artist', fg='black', bg="white",
                     font=("Comic Sans MS", 14))
    message1.grid(row=0, column=0, pady=(15, 5), padx=(10, 10))
    message1 = Label(frame, text="Try memorized all of them because you will be asked about them", fg='black',
                     bg="white",
                     font=("Comic Sans MS", 14))
    message1.grid(row=1, column=0, pady=(0, 5), padx=(10, 10))
    message1 = Label(frame, text='Prepare yourself...', fg='black', bg="white", font=("Comic Sans MS", 16))
    message1.grid(row=2, column=0, pady=(15, 5), padx=(10, 10))
    progress = Progressbar(frame, orient=HORIZONTAL, length=100, mode='indeterminate')
    progress.grid(row=3, column=0, pady=(5, 5))
    bar(progress, frame)  # start progress bar

    listt = frame.grid_slaves()
    for l in listt:
        l.destroy()

    message1 = Label(frame, text='You will not know which artist you will play .. Try to guess', fg='black', bg="white",
                     font=("Comic Sans MS", 16))
    message1.grid(row=0, column=0, pady=(5, 5))
    message2 = Label(frame, text='the game will start  in 5 second', fg='black', bg="white",
                     font=("Comic Sans MS", 14))
    message2.grid(row=1, column=0, pady=(5, 5))
    frame.after(5000, showAttribute, Gamer_name, window, frame, GameInfoDict, 0, fileBackground2)


# show attribute function
def showAttribute(Gamer_name, window, frame, GameInfoDict, i, fileBackground2):
    list = frame.grid_slaves()
    for l in list:
        l.destroy()
    background_label = Label(window, bg="white")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="white")
    frame.grid(row=1, column=1)
    for j in range(17):
        for k in range(17):
            message = Label(frame, text="", bg="white")
            message.grid(row=k, column=j, pady=(5, 5), padx=(5, 5))
    message3 = Label(frame, text=GameInfoDict['properties'][i], fg='black', bg="white", font=("Comic Sans MS", 16))
    message3.grid(row=randint(0, 16), column=randint(0, 16), pady=(0, 0))
    if i + 1 < len(GameInfoDict['properties']):
        frame.after(2000, showAttribute, Gamer_name, window, frame, GameInfoDict, i + 1, fileBackground2)
    else:
        frame.after(2000, showQuestion, Gamer_name, window, frame, GameInfoDict, 0, [], "", fileBackground2)


# show question function
def showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ, answers, get_anwser, fileBackground2):
    answers.append(get_anwser)
    if numberOfQ < len(GameInfoDict['questions'].keys()):
        list = frame.grid_slaves()
        for l in list:
            l.destroy()
        frame = Frame(window, bg="white")
        frame.grid(row=1, column=1)
        list_of_q = []
        for i in GameInfoDict['questions'].keys():
            list_of_q.append(i)
        q = list_of_q[numberOfQ]
        question = Label(frame, text=q, fg='black', bg="white", font=("Comic Sans MS", 14))
        question.grid(row=0, column=0, pady=(10, 10))
        a1_text = GameInfoDict['questions'][q]['answers'][0]
        a1 = Button(frame, text=a1_text, bg="#3abdef", fg="white", width=30, font=("Comic Sans MS", 14),
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a1_text, fileBackground2))
        a1.grid(row=1, column=0, pady=(5, 5))

        a2_text = GameInfoDict['questions'][q]['answers'][1]
        a2 = Button(frame, text=a2_text, bg="#3abdef", fg="white", width=30, font=("Comic Sans MS", 14),
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a2_text, fileBackground2))
        a2.grid(row=2, column=0, pady=(5, 5))

        a3_text = GameInfoDict['questions'][q]['answers'][2]
        a3 = Button(frame, text=a3_text, bg="#3abdef", fg="white", width=30, font=("Comic Sans MS", 14),
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a3_text, fileBackground2))
        a3.grid(row=3, column=0, pady=(5, 5))

        a4_text = GameInfoDict['questions'][q]['answers'][3]
        a4 = Button(frame, text=a4_text, bg="#3abdef", fg="white", width=30, font=("Comic Sans MS", 14),
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a4_text, fileBackground2))
        a4.grid(row=4, column=0, pady=(5, 5))
        right_answer = Label(frame, text=GameInfoDict['questions'][q]['true'], bg="white", fg='black',
                             font=("Comic Sans MS", 10))
        right_answer.grid(row=5, column=0, pady=(10, 10))
    else:  # the last question
        del answers[0]
        # get grade
        grade = gL.end(Gamer_name.get(), answers, GameInfoDict, 2)
        list = frame.grid_slaves()
        for l in list:
            l.destroy()
        background_label = Label(window, image=fileBackground2)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        frame = Frame(window, bg="white")
        frame.grid(row=1, column=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        message1 = Label(frame, text='your artist was: ' + GameInfoDict['artist_name'], fg='black', bg="white",
                         font=("Comic Sans MS", 16))
        message1.grid(row=0, column=0, pady=(5, 5))
        message1 = Label(frame, text='you grade: ' + str(grade), fg='black', bg="white", font=("Comic Sans MS", 16))
        message1.grid(row=1, column=0, pady=(5, 5))

        bottonEasy = Button(frame, text='Back to menu', bg="#10c716", fg="white", font=("Comic Sans MS", 16),
                            command=lambda: start(window, Gamer_name, fileBackground2))
        bottonEasy.grid(row=2, column=0, pady=(5, 5))


# go to start menu
def start(window, Gamer_name, fileBackground2):
    start_menu.start_menu_window(window, Gamer_name, fileBackground2)
