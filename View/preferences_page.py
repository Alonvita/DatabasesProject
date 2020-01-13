from tkinter import *
from View import start_menu


def preference_window(window, name):
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    label = Label(frame, text='Preference manu', fg='black', font='Ariel 16 bold')
    label.grid(row=0, columnspan=7, pady=(10, 10))

    # get from alon the preference dictionary
    preferences_dict = {
        "a": ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        "b": ['h', 'i', 'j', 'k', 'l', 'm', 'n'],
        "c": ['o', 'p', 'q', 'r', 's', 't', 'u'],
    }

    choice_dic = {}
    for preference in list(preferences_dict.keys()):
        choice_dic[preference] = []
        i = 0
        for choice in preferences_dict[preference]:
            var = IntVar()
            choice_dic[preference].append(var)
            i += 1
    rowindex = 1
    colindex = 0
    for preference in list(preferences_dict.keys()):
        pre_name = Label(frame, text='choose: ' + preference, fg='black', font='Ariel 16 bold')
        pre_name.grid(row=rowindex, columnspan=7, pady=(10, 10))
        rowindex += 1
        i = 0
        for text in preferences_dict[preference]:
            b = Checkbutton(frame, text=text,
                            variable=choice_dic[preference][i], offvalue="L")
            b.grid(row=rowindex, column=colindex, pady=(10, 10))
            if colindex < 7:
                colindex += 1
            else:
                colindex = 0
                rowindex += 1
            i += 1
        rowindex += 1
        colindex = 0

    bottonSend = Button(frame, text='Continue', bg="green", fg="black", font='Ariel 8 bold',
                        command=lambda: preference_button(window, preferences_dict, choice_dic, name))
    bottonSend.grid(row=rowindex, columnspan=7, pady=(10, 5))


def preference_button(window, pre_dictionary, choice_dic, name):
    return_dictionary = {}
    for preference in list(choice_dic.keys()):
        return_dictionary[preference] = []
        i = 0
        for choice in choice_dic[preference]:
            if choice.get() == 1:
                return_dictionary[preference].append(pre_dictionary[preference][i])
            i += 1
    # send to alon the return_dictionary
    start_menu.start_menu_window(window, name)
