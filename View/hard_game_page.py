from random import randint
from tkinter import *
from View import start_menu


def hard_game_window(window, Gamer_name):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # GameInfoDict = game.start(Gamer_name, 2)
    GameInfoDict = {
        "artist_name": "Adel",
        "properties": ["Country: UK", "Date: 12.12.1980", "Song1: Alon kaka", "Song2: Sara kaka", "Song3: Yana kaka"],
        "questions": {
            "q1": {
                "text": "Country?",
                "answers": ["Israel", "USA", "Poland", "UK"],
                "true": "UK"
            },
            "q2": {
                "text": "Date?",
                "answers": ["12.12.1984", "12.12.1979", "12.12.1980", "12.12.1981"],
                "true": "12.12.1980"
            },
            "q3": {
                "text": "Song1?",
                "answers": ["song1_a1", "song1_a2", "song1_a3", "Alon kaka"],
                "true": "right_answer"
            },
            "q4": {
                "text": "Song2?",
                "answers": ["song2_a1", "song2_a2", "Sara kaka", "song2_a3"],
                "true": "right_answer"
            },
            "q5": {
                "text": "Song3?",
                "answers": ["Yana kaka", "song3_a1", "song3_a2", "song3_a3"],
                "true": "Yana kaka"
            }
        }
    }

    message1 = Label(frame, text='You will not know which artist you will play .. Try to guess', fg='black', font='Ariel 16 bold')
    message1.grid(row=0, column=0, pady=(5, 5))
    message2 = Label(frame, text='the game will start  in 5 secound', fg='black', font='Ariel 10 bold')
    message2.grid(row=1, column=0, pady=(5, 5))
    frame.after(5000, showAttribute, Gamer_name, window, frame, GameInfoDict, 0)


def showAttribute(Gamer_name, window, frame, GameInfoDict, i):
    list = frame.grid_slaves()
    for l in list:
        l.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)
    for j in range(17):
        for k in range(17):
            message = Label(frame, text="")
            message.grid(row=k, column=j, pady=(5, 5), padx=(5, 5))
    message3 = Label(frame, text=GameInfoDict['properties'][i], fg='black', font='Ariel 16 bold')
    message3.grid(row=randint(0, 16), column=randint(0, 16), pady=(0, 0))
    if i + 1 < len(GameInfoDict['properties']):
        frame.after(2000, showAttribute, Gamer_name, window, frame, GameInfoDict, i + 1)
    else:
        frame.after(2000, showQuestion, Gamer_name, window, frame, GameInfoDict, 0, [], "")


def showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ, answers, get_anwser):
    answers.append(get_anwser)
    if numberOfQ < len(GameInfoDict['questions'].keys()):
        list = frame.grid_slaves()
        for l in list:
            l.destroy()
        frame = Frame(window)
        frame.grid(row=1, column=1)
        list_of_q = []
        for i in GameInfoDict['questions'].keys():
            list_of_q.append(i)
        q = list_of_q[numberOfQ]
        question = Label(frame, text=q, fg='black', font='Ariel 16 bold')
        question.grid(row=0, column=0, pady=(10, 10))
        a1_text = GameInfoDict['questions'][q]['answers'][0]
        a1 = Button(frame, text=a1_text, bg="blue", fg="white", font='Ariel 12 bold',
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a1_text))
        a1.grid(row=1, column=0, pady=(5, 5))
        a2_text = GameInfoDict['questions'][q]['answers'][1]
        a2 = Button(frame, text=a2_text, bg="blue", fg="white", font='Ariel 12 bold',
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a2_text))
        a2.grid(row=2, column=0, pady=(5, 5))
        a3_text = GameInfoDict['questions'][q]['answers'][2]
        a3 = Button(frame, text=a3_text, bg="blue", fg="white", font='Ariel 12 bold',
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a3_text))
        a3.grid(row=3, column=0, pady=(5, 5))

        a4_text = GameInfoDict['questions'][q]['answers'][3]
        a4 = Button(frame, text=a4_text, bg="blue", fg="white", font='Ariel 12 bold',
                    command=lambda: showQuestion(Gamer_name, window, frame, GameInfoDict, numberOfQ + 1,
                                                 answers, a4_text))
        a4.grid(row=4, column=0, pady=(5, 5))
        right_answer = Label(frame, text=GameInfoDict['questions'][q]['true'], fg='black', font='Ariel 8')
        right_answer.grid(row=5, column=0, pady=(10, 10))
    else:
        del answers[0]
        # grade = game.end(answers, GameInfoDict, 2)
        grade = 90
        list = frame.grid_slaves()
        for l in list:
            l.destroy()
        frame = Frame(window)
        frame.grid(row=1, column=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        message1 = Label(frame, text='you played on: ' + GameInfoDict['artist_name'], fg='black', font='Ariel 16 bold')
        message1.grid(row=0, column=0, pady=(5, 5))
        message2 = Label(frame, text='you grade: ' + str(grade), fg='black', font='Ariel 16 bold')
        message2.grid(row=1, column=0, pady=(5, 5))
        bottonEasy = Button(frame, text='Back to menu', bg="blue", fg="white", font='Ariel 12 bold',
                            command=lambda: start(window, Gamer_name))
        bottonEasy.grid(row=2, column=0, pady=(5, 5))


def start(window, Gamer_name):
    start_menu.start_menu_window(window, Gamer_name)
