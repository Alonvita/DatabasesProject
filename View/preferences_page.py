import threading
from tkinter import *
from tkinter.ttk import Progressbar

from View import start_menu
import Logic.GameLogic as gL

preferences_dict = ""


# function that get progress bar and play it
def bar(progress, frame):
    global preferences_dict
    import time
    i = 0
    flag = 0
    while True:
        if preferences_dict == "":
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


# get preference dictionary
def getpre():
    global preferences_dict
    preferences_dict = gL.get_all_preferences()


def preference_window(window, name, fileBackground, fileBackground2):
    global preferences_dict

    for widget in window.winfo_children():
        widget.destroy()

    background_label = Label(window, image=fileBackground)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window)
    frame.grid(row=1, column=1)
    background_label2 = Label(frame, image=fileBackground2)
    background_label2.place(x=0, y=0, relwidth=1, relheight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # get preference dictionary in thread
    t = threading.Thread(target=getpre)
    t.start()

    message1 = Label(frame, text='Please Wait...', fg='black', bg="white", font=("Comic Sans MS", 16))
    message1.grid(row=0, column=0, pady=(15, 5), padx=(10, 10))
    progress = Progressbar(frame, orient=HORIZONTAL, length=100, mode='indeterminate')
    progress.grid(row=1, column=0, pady=(5, 15))
    bar(progress, frame)  # start progress bar

    # destroy all the widgets of the frame
    listt = frame.grid_slaves()
    for l in listt:
        l.destroy()

    label = Label(frame, text='Preference menu', fg='black', bg="white", font=("Comic Sans MS", 20))
    label.grid(row=0, columnspan=7, pady=(10, 10))
    note = Label(frame, text='The game will choose artists based on your choices', bg="white", fg='black',
                 font=("Comic Sans MS", 16))
    note2 = Label(frame, text='You can choose the preferred genre only once', bg="white", fg='black',
                  font=("Comic Sans MS", 16))
    note.grid(row=1, columnspan=7, pady=(5, 1))
    note2.grid(row=2, columnspan=7, pady=(1, 5))

    choice_dic = {}
    # create choice dictionary
    for preference in list(preferences_dict.keys()):
        choice_dic[preference] = []
        i = 0
        for choice in preferences_dict[preference]:
            var = IntVar()
            choice_dic[preference].append(var)
            i += 1
    rowindex = 3
    colindex = 0
    # create the preference dictionary of the client
    for preference in list(preferences_dict.keys()):
        i = 0
        for text in preferences_dict[preference]:
            b = Checkbutton(frame, text=text, bg="white", font=("Comic Sans MS", 8),
                            variable=choice_dic[preference][i], offvalue="L")
            b.grid(row=rowindex, column=colindex, pady=(5, 5))
            if colindex < 6:
                colindex += 1
            else:
                colindex = 0
                rowindex += 1
            i += 1
        rowindex += 1
        colindex = 0

    # send preferences
    bottonSend = Button(frame, text='Continue', bg="#10c716", fg="black", font=("Comic Sans MS", 16),
                        command=lambda: preference_button(window, frame, preferences_dict, choice_dic, name, rowindex,
                                                          fileBackground2))
    bottonSend.grid(row=rowindex, columnspan=7, pady=(10, 5))


# function that send the preference dictionary to the logic
def preference_button(window, frame, pre_dictionary, choice_dic, name, rowindex, fileBackground2):
    return_dictionary = {}
    for preference in list(choice_dic.keys()):
        return_dictionary[preference] = []
        i = 0
        for choice in choice_dic[preference]:
            if choice.get() == 1:
                return_dictionary[preference].append(pre_dictionary[preference][i])
            i += 1
    # check if the list is empty
    if len(return_dictionary['Genre']) == 0:
        Need = Label(frame, text='must choose Genre', fg='red', bg="white", font=("Comic Sans MS", 12))
        Need.grid(row=rowindex + 2, columnspan=7, pady=(5, 5))
    else:
        # everything ok
        gL.add_preferences_to_user(name.get(), return_dictionary)
        # go to stare menu
        start_menu.start_menu_window(window, name, fileBackground2)
